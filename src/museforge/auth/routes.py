"""MCP OAuth routes + Bearer-auth ASGI wrapper for the Streamable HTTP transport.

Implements the authorization-code flow with Google as the upstream IdP:

    MCP client ──► /authorize ──► Google ──► /callback ──► MCP client (code)
                                              │
                                              ▼
                                         /token ──► access_token
                                              │
                                              ▼
                                      /mcp (Bearer)

Plus the discovery endpoints required by the MCP OAuth spec and a Bearer-auth ASGI wrapper
that protects the MCP transport.
"""

from __future__ import annotations

import json
import os
import secrets
import time
from typing import Any
from urllib.parse import urlencode

from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse, Response
from starlette.routing import Route

from museforge.auth.errors import GoogleOAuthError
from museforge.auth.google import build_auth_url, exchange_code, verify_id_token
from museforge.auth.store import AccessToken, InMemoryAuthStore

# Public base URL of this server (what the MCP client sees). Override in production.
PUBLIC_BASE_URL = os.environ.get("MUSEFORGE_PUBLIC_BASE_URL", "http://localhost:8000")
# Redirect URI registered with Google for THIS server's /callback. Must match exactly.
GOOGLE_REDIRECT_URI = os.environ.get(
    "MUSEFORGE_GOOGLE_REDIRECT_URI", f"{PUBLIC_BASE_URL}/callback"
)
# Path mounted as the MCP transport (Streamable HTTP).
MCP_MOUNT_PATH = "/mcp"

# Comma-separated list of email domains allowed to authenticate (default: feedmob.com).
# Example:  MUSEFORGE_ALLOWED_EMAIL_DOMAINS=feedmob.com,feedmob.cn
_DEFAULT_ALLOWED_DOMAINS = ("feedmob.com",)


def allowed_email_domains() -> set[str]:
    """Return the set of email domains allowed to authenticate (lowercased)."""
    raw = os.environ.get("MUSEFORGE_ALLOWED_EMAIL_DOMAINS")
    if not raw:
        return set(_DEFAULT_ALLOWED_DOMAINS)
    return {d.strip().lower() for d in raw.split(",") if d.strip()}


def _is_email_allowed(email: str | None, claims: dict[str, Any]) -> bool:
    """Check that the user's email/hd is in the configured feedmob (org) allowlist."""
    allowed = allowed_email_domains()
    if not allowed:
        return True  # no allowlist configured -> open (misconfiguration warning)
    if email and "@" in email:
        domain = email.split("@", 1)[1].strip().lower()
        if domain in allowed:
            return True
    # Google Workspace hosted-domain claim (only present for Workspace users).
    hd = str(claims.get("hd", "")).strip().lower()
    return bool(hd and hd in allowed)


def _resource_metadata() -> dict[str, Any]:
    return {
        "resource": PUBLIC_BASE_URL,
        "authorization_servers": [PUBLIC_BASE_URL],
        "bearer_methods_supported": ["header"],
        "scopes_supported": ["museforge"],
    }


def _authorization_server_metadata() -> dict[str, Any]:
    return {
        "issuer": PUBLIC_BASE_URL,
        "authorization_endpoint": f"{PUBLIC_BASE_URL}/authorize",
        "token_endpoint": f"{PUBLIC_BASE_URL}/token",
        "registration_endpoint": f"{PUBLIC_BASE_URL}/register",
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code"],
        "code_challenge_methods_supported": ["S256", "plain"],
        "token_endpoint_auth_methods_supported": ["none"],
        "scopes_supported": ["museforge"],
    }


# -- discovery -----------------------------------------------------------


async def protected_resource_metadata(request: Request) -> JSONResponse:
    return JSONResponse(_resource_metadata())


async def authorization_server_metadata(request: Request) -> JSONResponse:
    return JSONResponse(_authorization_server_metadata())


# -- dynamic client registration -----------------------------------------


async def register_client(request: Request) -> JSONResponse:
    store: InMemoryAuthStore = request.app.state.auth_store
    client = store.register_client()
    return JSONResponse(
        {
            "client_id": client.client_id,
            "client_id_issued_at": int(client.created_at),
            # Public client (no secret) — typical for MCP clients in browsers/native apps.
        },
        status_code=201,
    )


# -- /authorize: redirect to Google --------------------------------------


async def authorize(request: Request) -> Response:
    store: InMemoryAuthStore = request.app.state.auth_store
    pending: dict[str, dict[str, Any]] = request.app.state.pending
    params = request.query_params
    client_id = params.get("client_id")
    redirect_uri = params.get("redirect_uri")
    state = params.get("state", "")
    scope = params.get("scope", "museforge")
    if not client_id or not redirect_uri:
        return JSONResponse({"error": "invalid_request"}, status_code=400)
    if not store.get_client(client_id):
        return JSONResponse({"error": "unknown_client"}, status_code=400)
    google_state = secrets.token_urlsafe(16)
    pending[google_state] = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
    }
    try:
        url = build_auth_url(google_state, GOOGLE_REDIRECT_URI)
    except GoogleOAuthError as exc:
        return JSONResponse({"error": "google_not_configured", "detail": str(exc)}, status_code=500)
    return RedirectResponse(url)


# -- /callback: handle Google redirect, issue MCP auth code ---------------


async def google_callback(request: Request) -> Response:
    pending: dict[str, dict[str, Any]] = request.app.state.pending
    google_state = request.query_params.get("state")
    code = request.query_params.get("code")
    error = request.query_params.get("error")
    if error:
        return JSONResponse({"error": "google_denied", "detail": error}, status_code=400)
    if not google_state or not code:
        return JSONResponse({"error": "invalid_request"}, status_code=400)
    mcp_request = pending.pop(google_state, None)
    if not mcp_request:
        return JSONResponse({"error": "invalid_state"}, status_code=400)

    try:
        tokens = exchange_code(code, GOOGLE_REDIRECT_URI)
    except GoogleOAuthError as exc:
        return JSONResponse({"error": "google_exchange_failed", "detail": str(exc)}, status_code=400)

    id_token = tokens.get("id_token")
    if not id_token:
        return JSONResponse({"error": "no_id_token"}, status_code=400)
    try:
        claims = verify_id_token(id_token)
    except Exception as exc:  # noqa: BLE001 - PyJWT raises many types
        return JSONResponse({"error": "id_token_invalid", "detail": str(exc)}, status_code=400)

    subject = claims.get("sub")
    email = claims.get("email")
    if not subject:
        return JSONResponse({"error": "no_subject"}, status_code=400)
    if not _is_email_allowed(email, claims):
        return JSONResponse(
            {
                "error": "email_domain_not_allowed",
                "detail": (
                    f"Only email domains in {sorted(allowed_email_domains())} are "
                    "permitted to use this MCP server."
                ),
            },
            status_code=403,
        )

    store: InMemoryAuthStore = request.app.state.auth_store
    mcp_code = store.create_auth_code(
        subject=subject,
        email=email,
        client_id=mcp_request["client_id"],
        redirect_uri=mcp_request["redirect_uri"],
        scope=mcp_request["scope"],
    )
    qs = urlencode({"code": mcp_code.code, "state": mcp_request["state"]})
    return RedirectResponse(f"{mcp_request['redirect_uri']}?{qs}")


# -- /token: exchange MCP code for access token ---------------------------


async def token(request: Request) -> JSONResponse:
    store: InMemoryAuthStore = request.app.state.auth_store
    form = await request.form()
    grant_type = str(form.get("grant_type") or "")
    code = str(form.get("code") or "")
    client_id = str(form.get("client_id") or "")
    redirect_uri = str(form.get("redirect_uri") or "")
    if grant_type != "authorization_code":
        return JSONResponse({"error": "unsupported_grant_type"}, status_code=400)
    if not code or not client_id or not redirect_uri:
        return JSONResponse({"error": "invalid_request"}, status_code=400)
    auth_code = store.take_auth_code(
        code, client_id=client_id, redirect_uri=redirect_uri
    )
    if not auth_code:
        return JSONResponse({"error": "invalid_grant"}, status_code=400)
    access = store.issue_access_token(
        subject=auth_code.subject,
        email=auth_code.email,
        scope=auth_code.scope,
        client_id=auth_code.client_id,
    )
    return JSONResponse(
        {
            "access_token": access.token,
            "token_type": "Bearer",
            "expires_in": max(1, int(access.expires_at - time.time())),
            "scope": access.scope,
        }
    )


# -- Bearer-auth ASGI wrapper for the MCP transport -----------------------


def _extract_bearer(headers: list[tuple[bytes, bytes]]) -> str | None:
    for name, value in headers:
        if name.lower() == b"authorization":
            v = value.decode("latin-1", errors="replace")
            if v.lower().startswith("bearer "):
                return v.split(" ", 1)[1].strip()
    return None


def bearer_auth_asgi(inner_app: Any) -> Any:
    """Wrap an ASGI app (the MCP Streamable HTTP transport) with Bearer-token auth.

    Every request to a path under ``MCP_MOUNT_PATH`` must carry a valid ``Authorization:
    Bearer <token>`` header. Unauthenticated requests get a 401 with the MCP-required
    ``WWW-Authenticate`` header pointing at the resource metadata.
    """

    async def app(scope: Any, receive: Any, send: Any) -> None:
        if scope["type"] != "http":
            await inner_app(scope, receive, send)
            return
        path = scope.get("path", "")
        if not path.startswith(MCP_MOUNT_PATH):
            await inner_app(scope, receive, send)
            return
        token_str = _extract_bearer(scope.get("headers", []))
        store: InMemoryAuthStore = scope["app"].state.auth_store
        info: AccessToken | None = (
            store.validate_access_token(token_str) if token_str else None
        )
        if info is None:
            body = json.dumps({"error": "invalid_token"}).encode("utf-8")
            headers = [
                (b"content-type", b"application/json"),
                (
                    b"www-authenticate",
                    f'Bearer resource_metadata="{PUBLIC_BASE_URL}'
                    f'/.well-known/oauth-protected-resource"'.encode("ascii"),
                ),
            ]
            await send({"type": "http.response.start", "status": 401, "headers": headers})
            await send({"type": "http.response.body", "body": body, "more_body": False})
            return
        # Stash the token info on the scope for the inner app / observability.
        scope["state"] = {"museforge_token": info}
        await inner_app(scope, receive, send)

    return app


# -- Starlette route list -------------------------------------------------

OAUTH_ROUTES = [
    Route(
        "/.well-known/oauth-protected-resource",
        protected_resource_metadata,
        methods=["GET"],
    ),
    Route(
        "/.well-known/oauth-authorization-server",
        authorization_server_metadata,
        methods=["GET"],
    ),
    Route("/register", register_client, methods=["POST"]),
    Route("/authorize", authorize, methods=["GET"]),
    Route("/callback", google_callback, methods=["GET"]),
    Route("/token", token, methods=["POST"]),
]

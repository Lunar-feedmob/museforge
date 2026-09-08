"""Google OAuth helpers — used by the MCP HTTP server's authorization flow.

Google is the upstream identity provider. The MCP server acts as a delegated authorization
server: it exchanges the user's Google credentials for opaque MCP access tokens bound to the
Google user identity (sub + email).
"""

from __future__ import annotations

import os
from typing import Any, cast
from urllib.parse import urlencode

import httpx
import jwt
from jwt import PyJWKClient

from museforge.auth.errors import GoogleOAuthError

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"
GOOGLE_ISSUERS = ("https://accounts.google.com", "accounts.google.com")
DEFAULT_SCOPES = ("openid", "email", "profile")


def require_google_config() -> tuple[str, str]:
    """Return (client_id, client_secret) or raise a clear error."""
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise GoogleOAuthError(
            "GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set for Google OAuth. "
            "Create OAuth 2.0 credentials in Google Cloud Console and set both env vars."
        )
    return client_id, client_secret


def build_auth_url(state: str, redirect_uri: str, *, scopes: list[str] | None = None) -> str:
    """Build the Google consent-screen URL for the authorization-code flow."""
    client_id, _ = require_google_config()
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(scopes or list(DEFAULT_SCOPES)),
        "state": state,
        "access_type": "online",
        "prompt": "select_account",
    }
    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"


def exchange_code(code: str, redirect_uri: str) -> dict[str, Any]:
    """Exchange a Google authorization code for tokens."""
    client_id, client_secret = require_google_config()
    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    resp = httpx.post(GOOGLE_TOKEN_URL, data=data, timeout=10.0)
    if resp.status_code != 200:
        raise GoogleOAuthError(
            f"Google token exchange failed ({resp.status_code}): {resp.text[:200]}"
        )
    return cast(dict[str, Any], resp.json())


_jwks_client: PyJWKClient | None = None


def _get_jwks_client() -> PyJWKClient:
    global _jwks_client
    if _jwks_client is None:
        _jwks_client = PyJWKClient(GOOGLE_JWKS_URL)
    return _jwks_client


def verify_id_token(id_token: str, *, audience: str | None = None) -> dict[str, Any]:
    """Verify a Google ID token (JWT) against Google's JWKS and return its claims.

    Validates the signature (RS256), issuer, audience, and expiry.
    """
    client_id, _ = require_google_config()
    signing_key = _get_jwks_client().get_signing_key_from_jwt(id_token)
    return jwt.decode(
        id_token,
        signing_key.key,
        algorithms=["RS256"],
        audience=audience or client_id,
        issuer=list(GOOGLE_ISSUERS),
    )

"""Tests for the HTTP MCP server + Google OAuth + Bearer auth."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from museforge.auth import (
    InMemoryAuthStore,
    allowed_email_domains,
)
from museforge.auth.errors import GoogleOAuthError
from museforge.auth.google import (
    build_auth_url,
    exchange_code,
    require_google_config,
)

# ---- Token store -----------------------------------------------------------


def test_token_store_issue_and_validate() -> None:
    store = InMemoryAuthStore()
    t = store.issue_access_token(subject="u1", email="u1@feedmob.com", scope="museforge", client_id="c1")
    assert store.validate_access_token(t.token) is not None
    assert store.validate_access_token(t.token).subject == "u1"
    assert store.validate_access_token("bogus") is None


def test_token_store_expired() -> None:
    store = InMemoryAuthStore(access_token_ttl=0)
    t = store.issue_access_token(subject="u1", email=None, scope="museforge", client_id=None)
    assert store.validate_access_token(t.token) is None


def test_auth_code_single_use() -> None:
    store = InMemoryAuthStore()
    code = store.create_auth_code(
        subject="u1", email="u1@feedmob.com",
        client_id="c1", redirect_uri="https://client/cb", scope="museforge",
    )
    ac = store.take_auth_code(code.code, client_id="c1", redirect_uri="https://client/cb")
    assert ac is not None and ac.subject == "u1"
    # second take must fail (single-use)
    assert store.take_auth_code(code.code, client_id="c1", redirect_uri="https://client/cb") is None


def test_dcr() -> None:
    store = InMemoryAuthStore()
    c = store.register_client()
    assert store.get_client(c.client_id) is not None
    assert store.get_client("does-not-exist") is None


# ---- Google OAuth helpers --------------------------------------------------


def test_require_google_config_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GOOGLE_CLIENT_ID", raising=False)
    monkeypatch.delenv("GOOGLE_CLIENT_SECRET", raising=False)
    with pytest.raises(GoogleOAuthError):
        require_google_config()


def test_build_auth_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GOOGLE_CLIENT_ID", "test-client")
    monkeypatch.setenv("GOOGLE_CLIENT_SECRET", "test-secret")
    url = build_auth_url("nonce123", "https://example.com/callback")
    assert "accounts.google.com" in url
    assert "client_id=test-client" in url
    assert "state=nonce123" in url
    assert "scope=openid" in url


def test_exchange_code_calls_google(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GOOGLE_CLIENT_ID", "cid")
    monkeypatch.setenv("GOOGLE_CLIENT_SECRET", "csec")

    class _Resp:
        status_code = 200
        text = "{}"

        def json(self):
            return {"id_token": "fake.jwt.token", "access_token": "x"}

    def _post(url, data, timeout):  # noqa: ARG001
        assert "oauth2.googleapis.com" in url
        return _Resp()

    with patch("museforge.auth.google.httpx.post", _post):
        result = exchange_code("the-code", "https://example.com/callback")
    assert result["id_token"] == "fake.jwt.token"


# ---- Allowed email domains (feedmob restriction) --------------------------


def test_default_allowed_domains_is_feedmob(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MUSEFORGE_ALLOWED_EMAIL_DOMAINS", raising=False)
    assert allowed_email_domains() == {"feedmob.com"}


def test_custom_allowed_domains(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MUSEFORGE_ALLOWED_EMAIL_DOMAINS", "feedmob.com, feedmob.cn")
    assert allowed_email_domains() == {"feedmob.com", "feedmob.cn"}


def test_allowed_domains_parses(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MUSEFORGE_ALLOWED_EMAIL_DOMAINS", "feedmob.com,feedmob.cn")
    assert allowed_email_domains() == {"feedmob.com", "feedmob.cn"}


# ---- HTTP routes + Bearer auth --------------------------------------------


def _build_app_for_test(monkeypatch: pytest.MonkeyPatch):
    """Build the Starlette app with a real InMemoryAuthStore, skipping the MCP transport
    (which requires the real MCP SDK and FastMCP). The auth routes are exercised directly."""
    # Provide dummy Google config so auth helpers don't error if any code path hits them.
    monkeypatch.setenv("GOOGLE_CLIENT_ID", "cid")
    monkeypatch.setenv("GOOGLE_CLIENT_SECRET", "csec")
    # PUBLIC_BASE_URL is captured at module import — patch the module constant directly.
    from museforge.auth import routes as auth_routes

    monkeypatch.setattr(auth_routes, "PUBLIC_BASE_URL", "http://testserver")
    monkeypatch.setattr(
        auth_routes, "GOOGLE_REDIRECT_URI", "http://testserver/callback"
    )

    from starlette.applications import Starlette

    from museforge.auth import OAUTH_ROUTES, InMemoryAuthStore

    app = Starlette(routes=list(OAUTH_ROUTES))
    app.state.auth_store = InMemoryAuthStore()
    app.state.pending = {}
    return app


def test_protected_resource_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    from starlette.testclient import TestClient

    app = _build_app_for_test(monkeypatch)
    client = TestClient(app)
    r = client.get("/.well-known/oauth-protected-resource")
    assert r.status_code == 200
    assert "authorization_servers" in r.json()


def test_authorization_server_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    from starlette.testclient import TestClient

    app = _build_app_for_test(monkeypatch)
    client = TestClient(app)
    r = client.get("/.well-known/oauth-authorization-server")
    assert r.status_code == 200
    body = r.json()
    assert body["issuer"] == "http://testserver"
    assert body["authorization_endpoint"].endswith("/authorize")
    assert body["token_endpoint"].endswith("/token")
    assert "code" in body["response_types_supported"]


def test_register_client_returns_client_id(monkeypatch: pytest.MonkeyPatch) -> None:
    from starlette.testclient import TestClient

    app = _build_app_for_test(monkeypatch)
    client = TestClient(app)
    r = client.post("/register")
    assert r.status_code == 201
    assert "client_id" in r.json()


def test_authorize_unknown_client(monkeypatch: pytest.MonkeyPatch) -> None:
    from starlette.testclient import TestClient

    app = _build_app_for_test(monkeypatch)
    client = TestClient(app)
    r = client.get(
        "/authorize",
        params={
            "client_id": "nope",
            "redirect_uri": "https://client/cb",
            "state": "s",
            "scope": "museforge",
        },
    )
    assert r.status_code == 400
    assert r.json()["error"] == "unknown_client"


def test_authorize_redirects_to_google(monkeypatch: pytest.MonkeyPatch) -> None:
    from starlette.testclient import TestClient

    app = _build_app_for_test(monkeypatch)
    client = TestClient(app)
    reg = client.post("/register").json()
    client_id = reg["client_id"]
    r = client.get(
        "/authorize",
        params={
            "client_id": client_id,
            "redirect_uri": "https://client/cb",
            "state": "s",
            "scope": "museforge",
        },
        follow_redirects=False,
    )
    assert r.status_code == 307
    assert "accounts.google.com" in r.headers["location"]


def test_callback_rejects_disallowed_domain(monkeypatch: pytest.MonkeyPatch) -> None:
    """If Google returns an ID token for a non-feedmob email, /callback must reject it."""
    from starlette.testclient import TestClient

    app = _build_app_for_test(monkeypatch)
    client = TestClient(app)

    # Simulate the /authorize flow to populate pending state.
    reg = client.post("/register").json()
    client_id = reg["client_id"]
    auth = client.get(
        "/authorize",
        params={
            "client_id": client_id,
            "redirect_uri": "https://client/cb",
            "state": "s",
            "scope": "museforge",
        },
        follow_redirects=False,
    )
    google_state = auth.headers["location"].split("state=", 1)[1].split("&", 1)[0]

    # Stub the Google helpers: exchange returns a fake id_token; verify decodes it to claims.
    fake_claims = {"sub": "abc", "email": "evil@external.com", "aud": "cid", "iss": "https://accounts.google.com"}
    with patch("museforge.auth.routes.exchange_code", return_value={"id_token": "x"}), \
         patch("museforge.auth.routes.verify_id_token", return_value=fake_claims):
        r = client.get(
            "/callback",
            params={"state": google_state, "code": "google-code"},
        )
    assert r.status_code == 403
    assert r.json()["error"] == "email_domain_not_allowed"


def test_callback_accepts_allowed_domain(monkeypatch: pytest.MonkeyPatch) -> None:
    from starlette.testclient import TestClient

    app = _build_app_for_test(monkeypatch)
    client = TestClient(app)
    reg = client.post("/register").json()
    client_id = reg["client_id"]
    auth = client.get(
        "/authorize",
        params={
            "client_id": client_id,
            "redirect_uri": "https://client/cb",
            "state": "s",
            "scope": "museforge",
        },
        follow_redirects=False,
    )
    google_state = auth.headers["location"].split("state=", 1)[1].split("&", 1)[0]

    fake_claims = {
        "sub": "abc",
        "email": "alice@feedmob.com",
        "hd": "feedmob.com",
        "aud": "cid",
        "iss": "https://accounts.google.com",
    }
    with patch("museforge.auth.routes.exchange_code", return_value={"id_token": "x"}), \
         patch("museforge.auth.routes.verify_id_token", return_value=fake_claims):
        r = client.get(
            "/callback",
            params={"state": google_state, "code": "google-code"},
            follow_redirects=False,
        )
    assert r.status_code == 307
    # The redirect goes to the client's redirect_uri with a code.
    assert "code=" in r.headers["location"]
    assert r.headers["location"].startswith("https://client/cb")


def test_token_endpoint_exchanges_code(monkeypatch: pytest.MonkeyPatch) -> None:
    """Full happy path: authorize -> callback -> token -> access_token."""
    from starlette.testclient import TestClient

    app = _build_app_for_test(monkeypatch)
    client = TestClient(app)
    reg = client.post("/register").json()
    client_id = reg["client_id"]
    redirect_uri = "https://client/cb"

    auth = client.get(
        "/authorize",
        params={"client_id": client_id, "redirect_uri": redirect_uri, "state": "s", "scope": "museforge"},
        follow_redirects=False,
    )
    google_state = auth.headers["location"].split("state=", 1)[1].split("&", 1)[0]

    claims = {"sub": "u1", "email": "u1@feedmob.com", "hd": "feedmob.com", "aud": "cid", "iss": "https://accounts.google.com"}
    with patch("museforge.auth.routes.exchange_code", return_value={"id_token": "x"}), \
         patch("museforge.auth.routes.verify_id_token", return_value=claims):
        cb = client.get(
            "/callback",
            params={"state": google_state, "code": "gc"},
            follow_redirects=False,
        )
    mcp_code = cb.headers["location"].split("code=", 1)[1].split("&", 1)[0]

    r = client.post(
        "/token",
        data={"grant_type": "authorization_code", "code": mcp_code, "client_id": client_id, "redirect_uri": redirect_uri},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["token_type"] == "Bearer"
    assert body["access_token"]
    assert body["scope"] == "museforge"


# ---- Bearer-auth ASGI wrapper ---------------------------------------------


def test_bearer_auth_rejects_missing_token() -> None:
    """An unauthenticated request to a Bearer-protected path gets 401 + WWW-Authenticate."""
    import asyncio
    from typing import Any

    from museforge.auth import InMemoryAuthStore, bearer_auth_asgi

    store = InMemoryAuthStore()

    async def inner_app(scope: Any, receive: Any, send: Any) -> None:
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"should not reach"})

    sent: list[dict] = []

    async def send(msg: dict) -> None:
        sent.append(msg)

    async def receive() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def call_no_auth() -> None:
        scope = {
            "type": "http",
            "method": "POST",
            "path": "/mcp",
            "headers": [],
            "app": type("A", (), {"state": type("S", (), {"auth_store": store})()})(),
        }
        await bearer_auth_asgi(inner_app)(scope, receive, send)

    asyncio.run(call_no_auth())
    assert sent[0]["status"] == 401
    assert any(b"www-authenticate" in k[0].lower() for k in sent[0]["headers"])


def test_bearer_auth_accepts_valid_token() -> None:
    import asyncio
    from typing import Any

    from museforge.auth import InMemoryAuthStore, bearer_auth_asgi

    store = InMemoryAuthStore()
    t = store.issue_access_token(subject="u", email="u@feedmob.com", scope="museforge", client_id="c")
    received: list[dict] = []

    async def inner_app(scope: Any, receive: Any, send: Any) -> None:
        received.append({"path": scope.get("path"), "token": scope["state"]["museforge_token"].subject})
        await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", b"text/plain")]})
        await send({"type": "http.response.body", "body": b"ok"})

    sent: list[dict] = []

    async def send(msg: dict) -> None:
        sent.append(msg)

    async def receive() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def call_with_auth() -> None:
        scope = {
            "type": "http",
            "method": "POST",
            "path": "/mcp",
            "headers": [(b"authorization", f"Bearer {t.token}".encode())],
            "app": type("A", (), {"state": type("S", (), {"auth_store": store})()})(),
        }
        wrapped = bearer_auth_asgi(inner_app)
        await wrapped(scope, receive, send)

    asyncio.run(call_with_auth())
    assert sent[0]["status"] == 200
    assert received[0]["token"] == "u"


def test_bearer_auth_rejects_bad_token() -> None:
    import asyncio
    from typing import Any

    from museforge.auth import InMemoryAuthStore, bearer_auth_asgi

    store = InMemoryAuthStore()

    async def inner_app(scope: Any, receive: Any, send: Any) -> None:
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"should not reach"})

    sent: list[dict] = []

    async def send(msg: dict) -> None:
        sent.append(msg)

    async def receive() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def call() -> None:
        scope = {
            "type": "http",
            "method": "POST",
            "path": "/mcp",
            "headers": [(b"authorization", b"Bearer wrong-token")],
            "app": type("A", (), {"state": type("S", (), {"auth_store": store})()})(),
        }
        await bearer_auth_asgi(inner_app)(scope, receive, send)

    asyncio.run(call())
    assert sent[0]["status"] == 401


def test_full_http_app_builds() -> None:
    """Smoke test: the full Starlette app (OAuth routes + /mcp mount) builds cleanly."""
    from museforge.mcp_http import _build_app

    app = _build_app()
    # 6 OAuth routes + 1 Mount for /mcp.
    assert len(app.router.routes) >= 7
    # The MCP mount is present.
    paths = [getattr(r, "path", "") for r in app.router.routes]
    assert any(p == "/mcp" for p in paths)

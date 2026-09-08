"""OAuth + authentication for the MCP HTTP server.

Public surface (used by ``museforge.mcp_http``):

- ``InMemoryAuthStore`` — clients, auth codes, access tokens.
- ``OAUTH_ROUTES`` — Starlette routes for /.well-known, /register, /authorize, /callback, /token.
- ``bearer_auth_asgi`` — ASGI middleware that protects the MCP transport with Bearer auth.
- ``MCP_MOUNT_PATH`` — the path the MCP transport is mounted at (``/mcp``).
"""

from museforge.auth.errors import AuthError, GoogleOAuthError, InvalidTokenError
from museforge.auth.google import (
    DEFAULT_SCOPES,
    build_auth_url,
    exchange_code,
    require_google_config,
    verify_id_token,
)
from museforge.auth.routes import (
    MCP_MOUNT_PATH,
    OAUTH_ROUTES,
    allowed_email_domains,
    bearer_auth_asgi,
)
from museforge.auth.store import (
    AccessToken,
    AuthCode,
    InMemoryAuthStore,
    RegisteredClient,
)

__all__ = [
    "AccessToken",
    "AuthCode",
    "AuthError",
    "DEFAULT_SCOPES",
    "GoogleOAuthError",
    "InMemoryAuthStore",
    "InvalidTokenError",
    "MCP_MOUNT_PATH",
    "OAUTH_ROUTES",
    "RegisteredClient",
    "allowed_email_domains",
    "bearer_auth_asgi",
    "build_auth_url",
    "exchange_code",
    "require_google_config",
    "verify_id_token",
]

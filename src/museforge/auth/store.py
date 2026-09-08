"""In-memory stores for MCP OAuth: registered clients, pending auth codes, and access tokens.

This is sufficient for V0 / single-instance / development. Production deployments should
swap this for a persistent store (Redis, PostgreSQL, etc.) so tokens survive restarts and
are shared across instances.
"""

from __future__ import annotations

import secrets
import time
from dataclasses import dataclass, field


@dataclass(frozen=True)
class RegisteredClient:
    client_id: str
    created_at: float = field(default_factory=time.time)


@dataclass(frozen=True)
class AuthCode:
    code: str
    subject: str
    email: str | None
    client_id: str
    redirect_uri: str
    scope: str
    expires_at: float


@dataclass(frozen=True)
class AccessToken:
    token: str
    subject: str
    email: str | None
    scope: str
    client_id: str | None
    expires_at: float


class InMemoryAuthStore:
    """Single-instance stores for OAuth clients, codes, and tokens."""

    def __init__(self, *, access_token_ttl: int = 3600, auth_code_ttl: int = 300) -> None:
        self.access_token_ttl = access_token_ttl
        self.auth_code_ttl = auth_code_ttl
        self._clients: dict[str, RegisteredClient] = {}
        self._codes: dict[str, AuthCode] = {}
        self._tokens: dict[str, AccessToken] = {}

    # -- Dynamic client registration (RFC 7591, public clients) -----------------

    def register_client(self) -> RegisteredClient:
        client = RegisteredClient(client_id=secrets.token_urlsafe(24))
        self._clients[client.client_id] = client
        return client

    def get_client(self, client_id: str) -> RegisteredClient | None:
        return self._clients.get(client_id)

    # -- MCP auth codes (server → client, exchanged at /token) ------------------

    def create_auth_code(
        self,
        *,
        subject: str,
        email: str | None,
        client_id: str,
        redirect_uri: str,
        scope: str,
    ) -> AuthCode:
        code = AuthCode(
            code=secrets.token_urlsafe(24),
            subject=subject,
            email=email,
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=scope,
            expires_at=time.time() + self.auth_code_ttl,
        )
        self._codes[code.code] = code
        return code

    def take_auth_code(self, code: str, *, client_id: str, redirect_uri: str) -> AuthCode | None:
        ac = self._codes.pop(code, None)
        if ac is None or ac.expires_at < time.time():
            return None
        if ac.client_id != client_id or ac.redirect_uri != redirect_uri:
            return None
        return ac

    # -- Opaque access tokens -------------------------------------------------

    def issue_access_token(
        self, *, subject: str, email: str | None, scope: str, client_id: str | None
    ) -> AccessToken:
        token = AccessToken(
            token=secrets.token_urlsafe(32),
            subject=subject,
            email=email,
            scope=scope,
            client_id=client_id,
            expires_at=time.time() + self.access_token_ttl,
        )
        self._tokens[token.token] = token
        return token

    def validate_access_token(self, token: str) -> AccessToken | None:
        info = self._tokens.get(token)
        if info is None or info.expires_at < time.time():
            return None
        return info

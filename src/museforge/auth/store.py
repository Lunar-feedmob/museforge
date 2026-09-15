"""Auth stores for MCP OAuth: registered clients, pending auth codes, access tokens,
and OAuth state pending exchange.

This module defines:

- ``BaseAuthStore`` — a Protocol for OAuth state storage (clients, auth codes, access
  tokens) plus OAuth state pending exchange (the ``pending`` map). The same store
  holds both kinds of state so a single backend (in-memory, Redis, ...) covers
  every piece of OAuth state that needs to survive a cold start.

- ``InMemoryAuthStore`` — single-instance, in-process storage. Default for local
  development.

- ``RedisAuthStore`` — persistent storage backed by Upstash Redis (REST). Selected
  by setting ``MUSEFORGE_AUTH_STORE=redis`` (and providing ``UPSTASH_REDIS_REST_URL``
  / ``UPSTASH_REDIS_REST_TOKEN``). Survives Vercel Function cold starts so OAuth
  users don't get kicked out mid-session.

The ``auth_store_from_env`` factory chooses between them based on env. ``memory``
is the default.
"""

from __future__ import annotations

import json
import os
import secrets
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Protocol


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


class BaseAuthStore(Protocol):
    """Contract every auth store must satisfy.

    All methods are synchronous. Upstash Redis (used by ``RedisAuthStore``) is a
    sync REST client — one HTTPS request per call, no socket management. This works
    inside async Starlette handlers because each call returns immediately.
    """

    # -- Dynamic client registration (RFC 7591, public clients) ----------------

    def register_client(self) -> RegisteredClient: ...
    def get_client(self, client_id: str) -> RegisteredClient | None: ...

    # -- MCP auth codes (server → client, exchanged at /token) -----------------

    def create_auth_code(
        self,
        *,
        subject: str,
        email: str | None,
        client_id: str,
        redirect_uri: str,
        scope: str,
    ) -> AuthCode: ...

    def take_auth_code(
        self, code: str, *, client_id: str, redirect_uri: str
    ) -> AuthCode | None: ...

    # -- Opaque access tokens --------------------------------------------------

    def issue_access_token(
        self,
        *,
        subject: str,
        email: str | None,
        scope: str,
        client_id: str | None,
    ) -> AccessToken: ...

    def validate_access_token(self, token: str) -> AccessToken | None: ...

    # -- OAuth state pending Google's callback ---------------------------------

    def set_pending(
        self, key: str, value: dict[str, Any], *, ttl: int = 300
    ) -> None: ...

    def take_pending(self, key: str) -> dict[str, Any] | None: ...


class InMemoryAuthStore:
    """Single-instance stores for OAuth clients, codes, tokens, and pending."""

    def __init__(self, *, access_token_ttl: int = 3600, auth_code_ttl: int = 300) -> None:
        self.access_token_ttl = access_token_ttl
        self.auth_code_ttl = auth_code_ttl
        self._clients: dict[str, RegisteredClient] = {}
        self._codes: dict[str, AuthCode] = {}
        self._tokens: dict[str, AccessToken] = {}
        self._pending: dict[str, tuple[dict[str, Any], float]] = {}

    # -- Dynamic client registration (RFC 7591, public clients) -----------------

    def register_client(self) -> RegisteredClient:
        client = RegisteredClient(client_id=secrets.token_urlsafe(24))
        self._clients[client.client_id] = client
        return client

    def get_client(self, client_id: str) -> RegisteredClient | None:
        return self._clients.get(client_id)

    # -- MCP auth codes (server → client, exchanged at /token) -----------------

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

    def take_auth_code(
        self, code: str, *, client_id: str, redirect_uri: str
    ) -> AuthCode | None:
        ac = self._codes.pop(code, None)
        if ac is None or ac.expires_at < time.time():
            return None
        if ac.client_id != client_id or ac.redirect_uri != redirect_uri:
            return None
        return ac

    # -- Opaque access tokens --------------------------------------------------

    def issue_access_token(
        self,
        *,
        subject: str,
        email: str | None,
        scope: str,
        client_id: str | None,
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

    # -- OAuth state pending Google's callback ---------------------------------

    def set_pending(
        self, key: str, value: dict[str, Any], *, ttl: int = 300
    ) -> None:
        self._pending[key] = (value, time.time() + ttl)

    def take_pending(self, key: str) -> dict[str, Any] | None:
        entry = self._pending.pop(key, None)
        if entry is None:
            return None
        value, expires_at = entry
        if expires_at < time.time():
            return None
        return value


class RedisAuthStore:
    """OAuth state stored in Upstash Redis (REST). Survives Function cold starts.

    Selected via ``MUSEFORGE_AUTH_STORE=redis``. Requires ``UPSTASH_REDIS_REST_URL``
    and ``UPSTASH_REDIS_REST_TOKEN`` (Vercel auto-injects these when you install the
    Upstash Redis integration from the Marketplace).
    """

    _PREFIX_CLIENT = "museforge:client:"
    _PREFIX_CODE = "museforge:code:"
    _PREFIX_TOKEN = "museforge:token:"
    _PREFIX_PENDING = "museforge:pending:"
    # 10 years — registered clients are not deleted by the protocol.
    _CLIENT_TTL_SECONDS = 10 * 365 * 24 * 3600

    def __init__(
        self,
        *,
        url: str,
        token: str,
        access_token_ttl: int = 3600,
        auth_code_ttl: int = 300,
    ) -> None:
        try:
            from upstash_redis import Redis
        except ImportError as exc:  # pragma: no cover
            raise ImportError(
                "RedisAuthStore requires the upstash-redis package. "
                "Install museforge with the mcp-http extra: "
                "pip install museforge[mcp-http]"
            ) from exc
        self._redis = Redis(url=url, token=token)
        self.access_token_ttl = access_token_ttl
        self.auth_code_ttl = auth_code_ttl

    @classmethod
    def from_env(cls) -> RedisAuthStore:
        url = os.environ.get("UPSTASH_REDIS_REST_URL", "")
        token = os.environ.get("UPSTASH_REDIS_REST_TOKEN", "")
        if not url or not token:
            raise RuntimeError(
                "MUSEFORGE_AUTH_STORE=redis requires UPSTASH_REDIS_REST_URL and "
                "UPSTASH_REDIS_REST_TOKEN env vars. Install the Upstash Redis "
                "integration from the Vercel Marketplace, or set them manually."
            )
        return cls(url=url, token=token)

    # -- helpers --------------------------------------------------------------

    def _set(self, key: str, value: str, ttl: int) -> None:
        self._redis.set(key, value, ex=ttl)

    def _get(self, key: str) -> str | None:
        result = self._redis.get(key)
        if result is None:
            return None
        return str(result)

    def _get_delete(self, key: str) -> str | None:
        """GET-then-DEL in a single round-trip. Returns the value or None.

        Used for single-use semantics on auth codes and pending OAuth state.
        """
        pipe = self._redis.pipeline()
        pipe.get(key)
        pipe.delete(key)
        results = pipe.exec()
        if not results:
            return None
        value = results[0]
        if value is None:
            return None
        return str(value)

    # -- Dynamic client registration (RFC 7591, public clients) -----------------

    def register_client(self) -> RegisteredClient:
        client = RegisteredClient(client_id=secrets.token_urlsafe(24))
        self._set(
            self._PREFIX_CLIENT + client.client_id,
            json.dumps(asdict(client)),
            ttl=self._CLIENT_TTL_SECONDS,
        )
        return client

    def get_client(self, client_id: str) -> RegisteredClient | None:
        raw = self._get(self._PREFIX_CLIENT + client_id)
        if raw is None:
            return None
        data = json.loads(raw)
        return RegisteredClient(**data)

    # -- MCP auth codes (server → client, exchanged at /token) -----------------

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
        self._set(
            self._PREFIX_CODE + code.code,
            json.dumps(asdict(code)),
            ttl=self.auth_code_ttl,
        )
        return code

    def take_auth_code(
        self, code: str, *, client_id: str, redirect_uri: str
    ) -> AuthCode | None:
        raw = self._get_delete(self._PREFIX_CODE + code)
        if raw is None:
            return None
        data = json.loads(raw)
        ac = AuthCode(**data)
        if ac.expires_at < time.time():
            return None
        if ac.client_id != client_id or ac.redirect_uri != redirect_uri:
            return None
        return ac

    # -- Opaque access tokens --------------------------------------------------

    def issue_access_token(
        self,
        *,
        subject: str,
        email: str | None,
        scope: str,
        client_id: str | None,
    ) -> AccessToken:
        token = AccessToken(
            token=secrets.token_urlsafe(32),
            subject=subject,
            email=email,
            scope=scope,
            client_id=client_id,
            expires_at=time.time() + self.access_token_ttl,
        )
        self._set(
            self._PREFIX_TOKEN + token.token,
            json.dumps(asdict(token)),
            ttl=self.access_token_ttl,
        )
        return token

    def validate_access_token(self, token: str) -> AccessToken | None:
        raw = self._get(self._PREFIX_TOKEN + token)
        if raw is None:
            return None
        data = json.loads(raw)
        info = AccessToken(**data)
        if info.expires_at < time.time():
            return None
        return info

    # -- OAuth state pending Google's callback ---------------------------------

    def set_pending(
        self, key: str, value: dict[str, Any], *, ttl: int = 300
    ) -> None:
        self._set(
            self._PREFIX_PENDING + key,
            json.dumps(value, ensure_ascii=False),
            ttl=ttl,
        )

    def take_pending(self, key: str) -> dict[str, Any] | None:
        raw = self._get_delete(self._PREFIX_PENDING + key)
        if raw is None:
            return None
        result: dict[str, Any] = json.loads(raw)
        return result


def auth_store_from_env() -> BaseAuthStore:
    """Build the auth store configured by ``MUSEFORGE_AUTH_STORE``.

    Defaults to ``InMemoryAuthStore`` (single-instance, no extra deps).
    Set ``MUSEFORGE_AUTH_STORE=redis`` to use ``RedisAuthStore`` (Upstash REST).
    """
    backend = os.environ.get("MUSEFORGE_AUTH_STORE", "memory").lower()
    if backend == "redis":
        return RedisAuthStore.from_env()
    return InMemoryAuthStore()
"""Tests for ``RedisAuthStore`` — the Upstash-backed OAuth state store.

Uses an in-memory stand-in for the Upstash Redis client (same method surface:
``set(key, value, ex=ttl)``, ``get(key)``, ``delete(key)``, ``pipeline()``).
This lets us exercise cross-instance survival — the property that protects OAuth
sessions from Vercel Function cold starts — without needing live Upstash.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict
from typing import Any

import pytest

from museforge.auth.store import (
    AccessToken,
    AuthCode,
    InMemoryAuthStore,
    RedisAuthStore,
    RegisteredClient,
    auth_store_from_env,
)


class _FakeUpstash:
    """In-memory shim for ``upstash_redis.Redis`` with the same method surface.

    Two ``RedisAuthStore`` instances constructed against the same ``_FakeUpstash``
    share state — the regression test for Vercel Function cold starts (a new
    serverless invocation rebuilds ``RedisAuthStore`` but its data must survive).
    """

    def __init__(self) -> None:
        self._data: dict[str, str] = {}
        self._expiry: dict[str, float] = {}

    def set(self, key: str, value: str, ex: int | None = None) -> str:
        self._data[key] = value
        if ex is not None:
            self._expiry[key] = time.time() + ex
        elif key in self._expiry:
            del self._expiry[key]
        return "OK"

    def get(self, key: str) -> str | None:
        self._maybe_expire(key)
        return self._data.get(key)

    def delete(self, *keys: str) -> int:
        count = 0
        for k in keys:
            if k in self._data:
                del self._data[k]
                self._expiry.pop(k, None)
                count += 1
        return count

    def pipeline(self) -> _FakePipeline:
        return _FakePipeline(self)

    def _maybe_expire(self, key: str) -> None:
        exp = self._expiry.get(key)
        if exp is not None and exp < time.time():
            self._data.pop(key, None)
            self._expiry.pop(key, None)


class _FakePipeline:
    def __init__(self, parent: _FakeUpstash) -> None:
        self._parent = parent
        self._ops: list[tuple[str, tuple[Any, ...]]] = []

    def get(self, key: str) -> _FakePipeline:
        self._ops.append(("get", (key,)))
        return self

    def delete(self, key: str) -> _FakePipeline:
        self._ops.append(("delete", (key,)))
        return self

    def execute(self) -> list[Any]:  # pragma: no cover - kept for older clients
        return [getattr(self._parent, name)(*args) for name, args in self._ops]

    def exec(self) -> list[Any]:
        return [getattr(self._parent, name)(*args) for name, args in self._ops]


@pytest.fixture
def fake_redis() -> _FakeUpstash:
    return _FakeUpstash()


@pytest.fixture
def store(fake_redis: _FakeUpstash) -> RedisAuthStore:
    # Inject the fake redis via the constructor (bypass from_env).
    s = RedisAuthStore.__new__(RedisAuthStore)
    s._redis = fake_redis  # type: ignore[attr-defined]
    s.access_token_ttl = 3600
    s.auth_code_ttl = 300
    return s


# -- direct-store tests, mirroring tests/test_mcp_http.py ------------------------


def test_register_client(store: RedisAuthStore) -> None:
    c1 = store.register_client()
    c2 = store.register_client()
    assert isinstance(c1, RegisteredClient)
    assert c1.client_id != c2.client_id
    assert store.get_client(c1.client_id) == c1
    assert store.get_client("does-not-exist") is None


def test_issue_and_validate_token(store: RedisAuthStore) -> None:
    tok = store.issue_access_token(
        subject="user-1", email="u@feedmob.com", scope="museforge", client_id="c1"
    )
    assert isinstance(tok, AccessToken)
    validated = store.validate_access_token(tok.token)
    assert validated is not None
    assert validated.subject == "user-1"
    assert validated.email == "u@feedmob.com"
    assert validated.scope == "museforge"
    assert validated.client_id == "c1"


def test_validate_token_expired(fake_redis: _FakeUpstash) -> None:
    s = RedisAuthStore.__new__(RedisAuthStore)
    s._redis = fake_redis  # type: ignore[attr-defined]
    s.access_token_ttl = 0
    s.auth_code_ttl = 300
    tok = s.issue_access_token(
        subject="x", email=None, scope="museforge", client_id=None
    )
    # access_token_ttl=0 means expires_at == time.time(); after one tick it's expired.
    time.sleep(0.01)
    assert s.validate_access_token(tok.token) is None


def test_auth_code_single_use(store: RedisAuthStore) -> None:
    code = store.create_auth_code(
        subject="sub",
        email="a@b.com",
        client_id="cid",
        redirect_uri="https://x/cb",
        scope="museforge",
    )
    assert isinstance(code, AuthCode)
    got = store.take_auth_code(
        code.code, client_id="cid", redirect_uri="https://x/cb"
    )
    assert got is not None
    assert got.subject == "sub"
    # Second take must fail (single-use semantics).
    assert store.take_auth_code(
        code.code, client_id="cid", redirect_uri="https://x/cb"
    ) is None


def test_pending_state_round_trip(store: RedisAuthStore) -> None:
    store.set_pending(
        "google-state-1",
        {"client_id": "c1", "redirect_uri": "https://x/cb", "scope": "museforge", "state": "s"},
    )
    got = store.take_pending("google-state-1")
    assert got == {
        "client_id": "c1",
        "redirect_uri": "https://x/cb",
        "scope": "museforge",
        "state": "s",
    }
    # Single-use.
    assert store.take_pending("google-state-1") is None


# -- the regression test: cross-instance survival (Vercel cold start) -------------


def test_token_survives_new_store_instance(fake_redis: _FakeUpstash) -> None:
    """Two ``RedisAuthStore`` instances against the same Redis share state.

    Simulates the Vercel cold-start case: the new Function invocation builds a
    fresh ``RedisAuthStore`` from env, but the access token issued by the previous
    invocation must still validate.
    """
    s1 = RedisAuthStore.__new__(RedisAuthStore)
    s1._redis = fake_redis  # type: ignore[attr-defined]
    s1.access_token_ttl = 3600
    s1.auth_code_ttl = 300

    tok = s1.issue_access_token(
        subject="user-x", email="x@feedmob.com", scope="museforge", client_id=None
    )

    # A brand-new instance (different Python object, same backing store).
    s2 = RedisAuthStore.__new__(RedisAuthStore)
    s2._redis = fake_redis  # type: ignore[attr-defined]
    s2.access_token_ttl = 3600
    s2.auth_code_ttl = 300

    validated = s2.validate_access_token(tok.token)
    assert validated is not None
    assert validated.subject == "user-x"
    assert validated.email == "x@feedmob.com"


def test_pending_survives_new_store_instance(fake_redis: _FakeUpstash) -> None:
    """OAuth state pending Google's callback survives Function cold starts."""
    s1 = RedisAuthStore.__new__(RedisAuthStore)
    s1._redis = fake_redis  # type: ignore[attr-defined]
    s1.access_token_ttl = 3600
    s1.auth_code_ttl = 300

    s1.set_pending(
        "g-state",
        {"client_id": "c1", "redirect_uri": "https://x/cb", "scope": "museforge", "state": ""},
    )

    s2 = RedisAuthStore.__new__(RedisAuthStore)
    s2._redis = fake_redis  # type: ignore[attr-defined]
    s2.access_token_ttl = 3600
    s2.auth_code_ttl = 300

    assert s2.take_pending("g-state") is not None


# -- the factory -----------------------------------------------------------------


def test_factory_default_is_in_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MUSEFORGE_AUTH_STORE", raising=False)
    monkeypatch.delenv("UPSTASH_REDIS_REST_URL", raising=False)
    monkeypatch.delenv("UPSTASH_REDIS_REST_TOKEN", raising=False)
    s = auth_store_from_env()
    assert isinstance(s, InMemoryAuthStore)


def test_factory_redis_requires_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MUSEFORGE_AUTH_STORE", "redis")
    monkeypatch.delenv("UPSTASH_REDIS_REST_URL", raising=False)
    monkeypatch.delenv("UPSTASH_REDIS_REST_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="UPSTASH_REDIS_REST_URL"):
        auth_store_from_env()


# -- protocol conformance --------------------------------------------------------


def test_redis_store_satisfies_protocol(store: RedisAuthStore) -> None:
    """``RedisAuthStore`` exposes the same 8 methods as ``BaseAuthStore``."""
    expected = {
        "register_client",
        "get_client",
        "create_auth_code",
        "take_auth_code",
        "issue_access_token",
        "validate_access_token",
        "set_pending",
        "take_pending",
    }
    assert expected.issubset(set(dir(store)))


def test_in_memory_store_satisfies_protocol() -> None:
    """``InMemoryAuthStore`` still implements the Protocol after the refactor."""
    expected = {
        "register_client",
        "get_client",
        "create_auth_code",
        "take_auth_code",
        "issue_access_token",
        "validate_access_token",
        "set_pending",
        "take_pending",
    }
    assert expected.issubset(set(dir(InMemoryAuthStore())))


# -- serialization shape (defensive) --------------------------------------------


def test_serialization_includes_all_fields(store: RedisAuthStore) -> None:
    """Verify the JSON round-trip preserves every dataclass field.

    A regression here would break the cross-instance test silently because
    ``AccessToken(**data)`` would fail or drop a field.
    """
    tok = store.issue_access_token(
        subject="sub",
        email="a@b.com",
        scope="museforge",
        client_id="cid",
    )
    # Pull the raw JSON out of Redis via the fake and confirm every key is present.
    raw = store._get(RedisAuthStore._PREFIX_TOKEN + tok.token)  # type: ignore[attr-defined]
    assert raw is not None
    data = json.loads(raw)
    for field_name in asdict(tok):
        assert field_name in data, f"field {field_name} dropped"
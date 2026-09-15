#!/usr/bin/env python3
"""Smoke-test a deployed MuseForge MCP server.

Usage::

    python scripts/verify_deploy.py https://museforge-abc123.vercel.app

Checks (in order):

1. OAuth discovery endpoints return valid metadata with the deployed URL.
2. Dynamic client registration returns a 201 with a client_id.
3. The /authorize endpoint rejects unknown clients (basic sanity).
4. The /mcp endpoint requires a Bearer token (returns 401 with WWW-Authenticate
   pointing at the protected-resource metadata).

Exits 0 if every check passes, 1 otherwise. Prints a summary line per check.
"""

from __future__ import annotations

import json
import sys
from urllib.parse import urljoin

import httpx


def _check(name: str, ok: bool, detail: str = "") -> bool:
    mark = "✅" if ok else "❌"
    suffix = f" — {detail}" if detail else ""
    print(f"{mark} {name}{suffix}")
    return ok


def main(base_url: str) -> int:
    base = base_url.rstrip("/")
    results: list[bool] = []

    with httpx.Client(timeout=10.0) as client:
        # 1. OAuth authorization-server metadata.
        r = client.get(urljoin(base + "/", ".well-known/oauth-authorization-server"))
        try:
            meta = r.json()
            ok = (
                r.status_code == 200
                and meta.get("issuer") == base
                and meta.get("authorization_endpoint", "").startswith(base)
                and meta.get("token_endpoint", "").startswith(base)
                and meta.get("registration_endpoint", "").startswith(base)
            )
            detail = f"issuer={meta.get('issuer')!r}"
        except Exception as exc:  # noqa: BLE001
            ok = False
            detail = f"parse failed: {exc}"
        results.append(_check("OAuth authorization-server metadata", ok, detail))

        # 2. Protected-resource metadata.
        r = client.get(urljoin(base + "/", ".well-known/oauth-protected-resource"))
        try:
            meta = r.json()
            ok = (
                r.status_code == 200
                and meta.get("resource") == base
                and base in (meta.get("authorization_servers") or [])
            )
            detail = f"resource={meta.get('resource')!r}"
        except Exception as exc:  # noqa: BLE001
            ok = False
            detail = f"parse failed: {exc}"
        results.append(_check("OAuth protected-resource metadata", ok, detail))

        # 3. Dynamic client registration.
        r = client.post(urljoin(base + "/", "register"))
        try:
            data = r.json()
            ok = r.status_code == 201 and isinstance(data.get("client_id"), str) and data["client_id"]
            detail = f"client_id={data.get('client_id', '')[:8]}..."
        except Exception as exc:  # noqa: BLE001
            ok = False
            detail = f"parse failed: {exc}"
        results.append(_check("Dynamic client registration", ok, detail))

        # 4. /authorize rejects unknown client.
        r = client.get(
            urljoin(base + "/", "authorize"),
            params={
                "client_id": "this-client-does-not-exist",
                "redirect_uri": "https://example.com/cb",
                "scope": "museforge",
                "state": "x",
            },
        )
        ok = r.status_code == 400 and r.json().get("error") == "unknown_client"
        detail = f"status={r.status_code}"
        results.append(_check("/authorize rejects unknown client", ok, detail))

        # 5. /mcp requires Bearer auth.
        r = client.post(urljoin(base + "/", "mcp"))
        ok = r.status_code == 401
        wa = r.headers.get("www-authenticate", "")
        ok = ok and "Bearer" in wa and "resource_metadata" in wa
        detail = f"status={r.status_code}, www-authenticate={wa[:60]!r}"
        results.append(_check("/mcp requires Bearer auth", ok, detail))

        # 6. /mcp rejects invalid Bearer.
        r = client.post(
            urljoin(base + "/", "mcp"),
            headers={"Authorization": "Bearer this-token-does-not-exist"},
        )
        ok = r.status_code == 401 and r.json().get("error") == "invalid_token"
        detail = f"status={r.status_code}"
        results.append(_check("/mcp rejects invalid Bearer", ok, detail))

    passed = sum(results)
    total = len(results)
    print()
    print(f"Summary: {passed}/{total} checks passed.")
    return 0 if all(results) else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <base-url>", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
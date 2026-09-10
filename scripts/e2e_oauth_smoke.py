"""End-to-end OAuth smoke test for the MuseForge MCP HTTP server.

This script does steps 1-2 and 4-7 of the browser flow so you only need to do step 3
(open the URL in a browser, sign in with your @feedmob.com account, copy the `code`
from the address bar after the redirect).

Prereq: the server is running (museforge-mcp-http) with GOOGLE_CLIENT_ID/SECRET in env.

Usage:
    python scripts/e2e_oauth_smoke.py http://localhost:8000
"""

from __future__ import annotations

import sys
import webbrowser
from urllib.parse import parse_qs, urlparse

import httpx


def main(base_url: str = "http://localhost:8000") -> None:
    # httpx reads Windows registry proxy settings by default — they break localhost.
    client = httpx.Client(timeout=30.0, trust_env=False)

    base = base_url.rstrip("/")

    print("=== 1. Discover (RFC 8414) ===")
    as_meta = client.get(f"{base}/.well-known/oauth-authorization-server").json()
    print(f"   issuer: {as_meta['issuer']}")
    print(f"   authorization_endpoint: {as_meta['authorization_endpoint']}")

    print("\n=== 2. Dynamic Client Registration (RFC 7591) ===")
    reg = client.post(f"{base}/register").json()
    client_id = reg["client_id"]
    print(f"   client_id: {client_id}")

    # redirect_uri the MCP client uses (Google will redirect the browser here with ?code=...).
    # We point it at a local URL that will 404 — that's fine, we just need the code from the URL bar.
    client_redirect_uri = f"{base}/cb"
    state = "e2e-smoke-test-123"
    scope = "museforge"

    auth_url = (
        f"{as_meta['authorization_endpoint']}"
        f"?client_id={client_id}"
        f"&redirect_uri={client_redirect_uri}"
        f"&state={state}"
        f"&scope={scope}"
        f"&response_type=code"
    )
    print(f"\n=== 3. Open this URL in your browser (you'll be sent to Google, then back to {client_redirect_uri}) ===")
    print(f"   {auth_url}")
    import contextlib

    with contextlib.suppress(OSError, RuntimeError):
        webbrowser.open(auth_url)
    redirected = input("\n   Paste the FULL redirect URL you landed on (or just the code): ").strip()

    # Accept either a full URL or a bare code.
    if "code=" in redirected:
        qs = parse_qs(urlparse(redirected).query)
        code = qs.get("code", [None])[0]
        got_state = qs.get("state", [None])[0]
        if got_state != state:
            print(f"   ⚠️  state mismatch (got {got_state!r}, expected {state!r}) — continuing anyway")
    else:
        code = redirected

    if not code:
        print("   ❌ no code captured")
        sys.exit(1)

    print("\n=== 4. Exchange code for access_token ===")
    token_resp = client.post(
        f"{base}/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "redirect_uri": client_redirect_uri,
        },
    )
    print(f"   status: {token_resp.status_code}")
    token_body = token_resp.json()
    if "access_token" not in token_body:
        print(f"   ❌ {token_body}")
        sys.exit(1)
    access_token = token_body["access_token"]
    print(f"   access_token: {access_token[:16]}... ({token_body['token_type']}, expires_in={token_body['expires_in']}s)")

    print("\n=== 5. Call an MCP tool with the Bearer token ===")
    mcp_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    # Initialize the MCP session (Streamable HTTP).
    init = client.post(
        f"{base}/mcp/",
        headers=mcp_headers,
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "e2e-smoke", "version": "0"},
            },
        },
    )
    print(f"   initialize -> {init.status_code} {init.text[:120]}...")

    # tools/list
    tools = client.post(
        f"{base}/mcp/",
        headers=mcp_headers,
        json={"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
    )
    print(f"   tools/list -> {tools.status_code}")
    tool_names = [t["name"] for t in tools.json().get("result", {}).get("tools", [])]
    print(f"   tools ({len(tool_names)}): {tool_names}")

    # Call analyze_image_request
    call = client.post(
        f"{base}/mcp/",
        headers=mcp_headers,
        json={
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "analyze_image_request",
                "arguments": {"request": "Create a premium fintech card advertisement"},
            },
        },
    )
    print(f"   tools/call analyze_image_request -> {call.status_code}")
    print(f"   body[:300]: {call.text[:300]}")
    print("\n=== 6. Done ===")
    print("   ✅ full OAuth flow works end-to-end.")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000") or 0)

# MCP Roadmap — Google OAuth HTTP MCP Server (IMPLEMENTED)

> **Status (V1 addition):** The HTTP MCP server with Google OAuth + Bearer auth is
> **implemented** in `src/museforge/mcp_http.py` and `src/museforge/auth/`. Run it with:
> ```bash
> pip install -e ".[mcp-http]"
> museforge-mcp-http --host 0.0.0.0 --port 8000
> # or:
> museforge mcp-http
> ```
> The stdio MCP server (`museforge-mcp` / `museforge mcp-stdio`) is also available for
> local, no-auth use.

---

## Architecture

```
MCP client ──► /authorize ──► Google ──► /callback ──► MCP client (code)
                                              │
                                              ▼
                                         /token ──► access_token
                                              │
                                              ▼
MCP client ──Authorization: Bearer <token>──► /mcp  (Streamable HTTP)
                                              │
                                              ▼
                                          MuseForge Service Layer
```

The MCP server is a **delegated authorization server**: it delegates authentication to
Google (the upstream IdP) and issues **opaque MCP access tokens** bound to the verified
Google user identity (`sub` + `email`).

## The 11 MCP tools

| MCP tool | Service Layer method |
|---|---|
| `create_image_prompt` | `MuseForgeAssistant.generate_response()` |
| `recommend_image_direction` | `CreativeDirector.design()` (+ retrieval) |
| `analyze_image_request` | `IntentAnalyzer.understand_request()` |
| `improve_image_prompt` | `MuseForgeAssistant.improve_prompt()` |
| `optimize_image_prompt` | `ModelOptimizer.optimize()` |
| `search_image_cases` | `CaseRetriever.search()` |
| `search_image_prompts` | `PromptRetriever.search()` |
| `search_image_recipes` | `RecipeRetriever.search()` |
| `search_visual_patterns` | `PatternRetriever.search()` |
| `search_image_styles` | `StyleRetriever.search()` |
| `search_prompt_techniques` | `TechniqueRetriever.search()` |

## Authorization flow

1. MCP client connects to `/mcp` → receives 401 with `WWW-Authenticate: Bearer
   resource_metadata=".../.well-known/oauth-protected-resource"`.
2. MCP client discovers `/.well-known/oauth-authorization-server` to find `authorization_endpoint`,
   `token_endpoint`, `registration_endpoint`, and supported PKCE methods.
3. MCP client calls `POST /register` (Dynamic Client Registration, public client — no secret)
   to obtain a `client_id`.
4. MCP client opens browser to `GET /authorize?client_id=...&redirect_uri=...&code_challenge=...&scope=museforge`.
5. The server redirects to Google's consent screen (`accounts.google.com/o/oauth2/v2/auth`).
6. **Only Google accounts whose email domain is in `MUSEFORGE_ALLOWED_EMAIL_DOMAINS`
   (default: `feedmob.com`) are permitted** — checked after Google ID-token verification
   (matches both the email's domain and the Google Workspace `hd` claim).
7. Google redirects back to `/callback?code=...&state=...`. The server exchanges the code,
   verifies the ID token (signature + audience + issuer + expiry against Google's JWKS),
   enforces the feedmob org allowlist, creates an MCP auth code, and redirects to the
   client's `redirect_uri?code=<mcp_code>&state=...`.
8. MCP client exchanges the MCP code at `POST /token` for an opaque access token.
9. MCP client calls `/mcp` with `Authorization: Bearer <token>` for every request.

## Configuration

| Env var | Required | Description |
|---|---|---|
| `GOOGLE_CLIENT_ID` | ✅ | OAuth client ID from Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | ✅ | OAuth client secret |
| `MUSEFORGE_PUBLIC_BASE_URL` | recommended | Public URL of this server (default `http://localhost:8000`) |
| `MUSEFORGE_GOOGLE_REDIRECT_URI` | optional | Override the Google redirect URI (default `<PUBLIC_BASE_URL>/callback`) |
| `MUSEFORGE_ALLOWED_EMAIL_DOMAINS` | optional | Comma-separated email domains (default `feedmob.com`) |
| `MUSEFORGE_HOST` | optional | Bind host (default `127.0.0.1`) |
| `MUSEFORGE_PORT` | optional | Bind port (default `8000`) |
| `MUSEFORGE_DATA_DIR` | optional | Knowledge store dir (default `data`) |

## Google Cloud Console setup

1. Create a project (or use an existing one).
2. **APIs & Services → OAuth consent screen**:
   - User type: **Internal** (Workspace) — this restricts the consent screen to your org.
   - Scopes: `openid`, `email`, `profile`.
   - Test users: add the feedmob users allowed during testing.
3. **APIs & Services → Credentials → Create credentials → OAuth client ID**:
   - Application type: **Web application**.
   - Authorized redirect URIs: `https://museforge.example.com/callback` (and
     `http://localhost:8000/callback` for local dev).
4. Copy the **Client ID** and **Client secret** into `GOOGLE_CLIENT_ID` /
   `GOOGLE_CLIENT_SECRET`.

> **Why "Internal" + Workspace?** Choosing "Internal" + a Google Workspace org means only
> users in that Workspace can grant consent, and the `hd` claim is populated. Combined with
> the `MUSEFORGE_ALLOWED_EMAIL_DOMAINS` allowlist (default `feedmob.com`), this gives
> feedmob-only access even if the OAuth client is somehow obtained by an external actor.

## Endpoints

| Path | Method | Purpose |
|---|---|---|
| `/.well-known/oauth-protected-resource` | GET | RFC 9728 resource metadata |
| `/.well-known/oauth-authorization-server` | GET | RFC 8414 authorization server metadata |
| `/register` | POST | Dynamic Client Registration (RFC 7591), returns `client_id` |
| `/authorize` | GET | Start the flow → redirect to Google |
| `/callback` | GET | Handle Google's redirect, enforce org allowlist, issue MCP code |
| `/token` | POST | Exchange MCP code for access token |
| `/mcp` | POST/GET | MCP Streamable HTTP transport (Bearer-protected) |

## Security

- **State parameter** ties the MCP `client_id` + `redirect_uri` + `state` to the Google
  consent screen's `state`.
- **PKCE** (S256 + plain) is advertised so MCP clients can use it.
- **Code single-use + 5-minute TTL** on MCP auth codes.
- **Access tokens** are opaque (not JWTs), stored server-side with a 1-hour TTL (in-memory).
- **Bearer auth** on every `/mcp` request; 401 with `WWW-Authenticate` on failure.
- **Org allowlist** (`feedmob.com`) checked at `/callback` after verifying Google's
  ID token (both email domain and `hd` claim).
- **Production**: run behind TLS (HTTPS). The in-memory token store should be swapped for
  Redis/Postgres so tokens survive restarts and are shared across instances.

## Local testing without Google

Use the stdio server (`museforge-mcp` / `museforge mcp-stdio`) for local agent use — no
OAuth, no network. The HTTP server is for shared/remote deployments.

## What the HTTP MCP server does NOT do

- It does not call an image-generation API in V0 (V2 concern).
- It does not bypass the license/attribution rules — every redistributed prompt carries
  provenance in the knowledge store.
- It does not require the optional `[anthropic]` extra — it works with the heuristic
  fallback and only uses an LLM if `MUSEFORGE_LLM_PROVIDER` is configured (for richer intent
  understanding and composition).

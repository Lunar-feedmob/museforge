"""Vercel entrypoint for the MuseForge MCP HTTP server.

Vercel's Python runtime auto-detects this file via the top-level ``app`` symbol
(see https://vercel.com/docs/functions/runtimes/python). Build with
``vercel deploy`` from the repo root.

Required env vars (set in Vercel project settings):

  - ``MUSEFORGE_AUTH_STORE``: ``memory`` (default, single-instance only) or
    ``redis`` (persistent; survives Function cold starts).
  - ``UPSTASH_REDIS_REST_URL`` and ``UPSTASH_REDIS_REST_TOKEN``: required when
    ``MUSEFORGE_AUTH_STORE=redis``. Vercel auto-injects these when you install
    the Upstash Redis integration from the Marketplace.
  - ``GOOGLE_CLIENT_ID`` and ``GOOGLE_CLIENT_SECRET``: from Google Cloud Console
    > OAuth credentials (Web application client).
  - ``MUSEFORGE_PUBLIC_BASE_URL``: e.g. ``https://museforge-<hash>.vercel.app``.
  - ``MUSEFORGE_GOOGLE_REDIRECT_URI``: e.g.
    ``https://museforge-<hash>.vercel.app/callback``. Add this URL to the
    Google OAuth client's "Authorized redirect URIs".
  - ``MUSEFORGE_ALLOWED_EMAIL_DOMAINS``: comma-separated email-domain allowlist
    (default ``feedmob.com``).
  - ``MUSEFORGE_DATA_DIR``: defaults to ``data``. Vercel includes the repo's
    ``data/`` directory in the deploy (it is not gitignored).
  - ``MUSEFORGE_LLM_PROVIDER`` + provider API key (optional): enables the LLM
    path. The deterministic heuristic path works with no key.

The 11 MCP tools are exposed at ``/mcp`` (Streamable HTTP, Bearer-protected).
OAuth discovery endpoints are at ``/.well-known/oauth-authorization-server`` and
``/.well-known/oauth-protected-resource``. The MCP authorization-code flow runs
on ``/authorize``, ``/callback``, and ``/token``.
"""

from museforge.mcp_http import _build_app

# Vercel auto-detects this top-level ``app`` symbol as the ASGI entrypoint.
app = _build_app()
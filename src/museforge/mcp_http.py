"""MuseForge MCP server over Streamable HTTP, protected by Google OAuth + Bearer auth.

Run with:  museforge-mcp-http   (or:  python -m museforge.mcp_http)

Architecture (see ``docs/mcp-roadmap.md``):

    MCP client ──► /authorize ──► Google ──► /callback ──► MCP client (code)
                                                  │
                                                  ▼
                                             /token ──► access_token
                                                  │
                                                  ▼
    MCP client ──Authorization: Bearer <token>──► /mcp  (Streamable HTTP)

The 11 MCP tools map 1:1 onto Service Layer methods (see ``museforge.mcp_server`` for the
stdio variant and ``docs/mcp-roadmap.md`` for the mapping).

Setup (see ``docs/mcp-roadmap.md`` for details):

    export GOOGLE_CLIENT_ID=...           # from Google Cloud Console > OAuth credentials
    export GOOGLE_CLIENT_SECRET=...
    export MUSEFORGE_PUBLIC_BASE_URL=https://museforge.example.com
    export MUSEFORGE_GOOGLE_REDIRECT_URI=https://museforge.example.com/callback
    # Add the redirect URI above to the Google OAuth client's "Authorized redirect URIs".
    museforge-mcp-http --host 0.0.0.0 --port 8000

Production notes:

- The default token store is in-memory; tokens do not survive restarts and are not shared
  across instances. Swap ``InMemoryAuthStore`` for a persistent backend (Redis, Postgres) for
  production.
- HTTPS is required in production (set behind a TLS-terminating reverse proxy or use uvicorn
  with `--ssl-keyfile` / `--ssl-certfile`).
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, is_dataclass
from typing import Any

from museforge.knowledge.store import KnowledgeStore
from museforge.providers.llm import provider_from_env
from museforge.services.assistant import MuseForgeAssistant


# Lazy MCP imports — the core package doesn't require the MCP SDK.
def _import_mcp() -> tuple[Any, Any, Any]:
    try:
        import uvicorn
        from mcp.server.fastmcp import FastMCP
        from starlette.applications import Starlette
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "The HTTP MCP server requires optional deps. Install with: "
            "pip install museforge[mcp-http]"
        ) from exc
    return FastMCP, Starlette, uvicorn


def _store() -> KnowledgeStore:
    return KnowledgeStore(os.environ.get("MUSEFORGE_DATA_DIR", "data"))


def _assistant() -> MuseForgeAssistant:
    return MuseForgeAssistant(_store(), llm=provider_from_env())


def _serialize(obj: Any) -> str:
    """Serialize a result to JSON text for MCP tool output."""
    from pydantic import BaseModel

    if isinstance(obj, BaseModel):
        return obj.model_dump_json(indent=2, ensure_ascii=False)
    if is_dataclass(obj) and not isinstance(obj, type):
        return json.dumps(asdict(obj), indent=2, ensure_ascii=False, default=str)
    return json.dumps(obj, indent=2, ensure_ascii=False, default=str)


def _search(retriever: Any, query: str, top_k: int) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item, score in retriever.search(query, top_k):
        out.append(
            {
                "id": getattr(item, "id", None),
                "name": getattr(item, "name", None) or getattr(item, "title", None),
                "score": round(float(score), 4),
                "description": getattr(item, "description", "")
                or getattr(item, "goal", ""),
            }
        )
    return out


def _build_mcp_server() -> Any:
    """Build the FastMCP server with all 11 tools registered."""
    FastMCP, *_ = _import_mcp()
    mcp = FastMCP("museforge")

    @mcp.tool()  # type: ignore[untyped-decorator]
    def create_image_prompt(
        request: str, model: str = "universal", prompt_only: bool = False
    ) -> str:
        """Turn an image idea into a structured Creative Direction + Super Prompt."""
        resp = _assistant().generate_response(
            request, model=model, prompt_only=prompt_only
        )
        return _serialize(resp)

    @mcp.tool()  # type: ignore[untyped-decorator]
    def recommend_image_direction(request: str) -> str:
        """Design a Creative Direction (concept, composition, lighting, color, typography)
        without composing the final prompt."""
        intent = _assistant().understand_request(request)
        # Run the full retrieval+design path but stop before compose.
        from museforge.services.assistant import MuseForgeAssistant as _A

        a: _A = _assistant()
        query = _A._query(intent, request)
        recipes = a.retrieve_recipes(query)
        patterns = a.retrieve_patterns(query)
        styles = a.retrieve_styles(query)
        techniques = a.retrieve_techniques(query)
        recipe = recipes[0] if recipes else None
        pattern = a._pick_pattern(intent, patterns, recipe)
        style = a._pick_style(intent, styles, recipe)
        direction = a.recommend_direction(
            intent, recipe=recipe, pattern=pattern, style=style, techniques=techniques
        )
        return _serialize(direction)

    @mcp.tool()  # type: ignore[untyped-decorator]
    def analyze_image_request(request: str) -> str:
        """Analyze a request into a structured Intent (use case, platform, aspect ratio, …)."""
        return _serialize(_assistant().understand_request(request))

    @mcp.tool()  # type: ignore[untyped-decorator]
    def improve_image_prompt(prompt: str, feedback: str = "") -> str:
        """Improve an existing prompt: strip low-info adjectives + append feedback."""
        return _assistant().improve_prompt(prompt, feedback)

    @mcp.tool()  # type: ignore[untyped-decorator]
    def optimize_image_prompt(prompt: str, model: str) -> str:
        """Produce a model-specific variant of a prompt (carries an optimization_basis label)."""
        return _serialize(_assistant().optimize_for_model(prompt, model))

    @mcp.tool()  # type: ignore[untyped-decorator]
    def search_image_cases(query: str, top_k: int = 5) -> str:
        """Search the Case knowledge base."""
        return _serialize(_search(_assistant().cases, query, top_k))

    @mcp.tool()  # type: ignore[untyped-decorator]
    def search_image_prompts(query: str, top_k: int = 5) -> str:
        """Search the Prompt knowledge base (attributed, redistributable prompts)."""
        return _serialize(_search(_assistant().prompts, query, top_k))

    @mcp.tool()  # type: ignore[untyped-decorator]
    def search_image_recipes(query: str, top_k: int = 5) -> str:
        """Search the Recipe knowledge base (methods for image tasks)."""
        return _serialize(_search(_assistant().recipes, query, top_k))

    @mcp.tool()  # type: ignore[untyped-decorator]
    def search_visual_patterns(query: str, top_k: int = 5) -> str:
        """Search the Visual Pattern knowledge base (reusable visual structures)."""
        return _serialize(_search(_assistant().patterns, query, top_k))

    @mcp.tool()  # type: ignore[untyped-decorator]
    def search_image_styles(query: str, top_k: int = 5) -> str:
        """Search the Style knowledge base (reusable visual systems)."""
        return _serialize(_search(_assistant().styles, query, top_k))

    @mcp.tool()  # type: ignore[untyped-decorator]
    def search_prompt_techniques(query: str, top_k: int = 5) -> str:
        """Search the Technique knowledge base (prompt-engineering levers)."""
        return _serialize(_search(_assistant().techniques, query, top_k))

    return mcp


def _build_app() -> Any:
    """Build the ASGI app: OAuth routes + Bearer-protected MCP transport at /mcp.

    Architecture:
      - The Starlette app handles OAuth routes and its own lifespan.
      - A middleware dispatches /mcp requests to the FastMCP transport ASGI app,
        preserving the full "/mcp" path (Mount would strip it and 404 the transport).
      - Lifespans of the OAuth app and the transport are composed so the transport's
        session manager initializes alongside the OAuth routes.
    """
    from museforge.auth import (
        MCP_MOUNT_PATH,
        OAUTH_ROUTES,
        InMemoryAuthStore,
        bearer_auth_asgi,
    )

    _FastMCP, Starlette, _uvicorn = _import_mcp()
    mcp = _build_mcp_server()

    # The transport: a Starlette sub-app whose internal Route is "/mcp". We extract
    # the underlying ASGI app (the StreamableHTTPASGIApp endpoint) so we can call it
    # from a middleware with the path preserved.
    transport_starlette = mcp.streamable_http_app()
    transport_asgi = transport_starlette.router.routes[0].endpoint

    # The OAuth app (routes only — we control lifespan separately).
    oauth_app = Starlette(routes=list(OAUTH_ROUTES))
    oauth_app.state.auth_store = InMemoryAuthStore()
    oauth_app.state.pending = {}

    # Compose lifespans so the transport's session manager initializes.
    oauth_lifespan = oauth_app.router.lifespan_context
    transport_lifespan = transport_starlette.router.lifespan_context
    if oauth_lifespan is not None and transport_lifespan is not None:
        from contextlib import asynccontextmanager

        @asynccontextmanager
        async def combined_lifespan(scope: Any) -> Any:
            async with oauth_lifespan(scope), transport_lifespan(scope):
                yield

        oauth_app.router.lifespan_context = combined_lifespan

    # Middleware that dispatches /mcp to the bearer-protected transport, preserving the path.
    class _McpDispatch:
        def __init__(self, app: Any, transport: Any) -> None:
            self.app = app
            self.transport = transport
            self._protected = bearer_auth_asgi(transport)

        async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
            # Starlette's Request reads scope["app"]; the Bearer wrapper reads
            # scope["app"].state.auth_store. Set it on every http/lifespan request
            # before delegating so the downstream app sees it.
            scope["app"] = self.app
            if scope["type"] == "http":
                path = scope.get("path", "")
                if path == MCP_MOUNT_PATH or path.startswith(MCP_MOUNT_PATH + "/"):
                    await self._protected(scope, receive, send)
                    return
            await self.app(scope, receive, send)

    return _McpDispatch(oauth_app, transport_asgi)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="museforge-mcp-http",
        description="Run the MuseForge MCP server over HTTP with Google OAuth.",
    )
    parser.add_argument("--host", default=os.environ.get("MUSEFORGE_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("MUSEFORGE_PORT", "8000")))
    parser.add_argument(
        "--reload", action="store_true", help="Reload on code changes (dev only)."
    )
    return parser.parse_args()


def serve(host: str | None = None, port: int | None = None) -> None:
    """Run the HTTP MCP server. ``host``/``port`` default to env (MUSEFORGE_HOST/MUSEFORGE_PORT
    or 127.0.0.1:8000). Used by both the console script and the CLI subcommand."""
    FastMCP, Starlette, uvicorn = _import_mcp()
    app = _build_app()
    uvicorn.run(
        app,
        host=host or os.environ.get("MUSEFORGE_HOST", "127.0.0.1"),
        port=port if port is not None else int(os.environ.get("MUSEFORGE_PORT", "8000")),
    )


def main() -> None:
    """Console-script entry point: parse argv and serve."""
    args = _parse_args()
    serve(host=args.host, port=args.port)


if __name__ == "__main__":
    main()

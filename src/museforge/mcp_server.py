"""MuseForge MCP server over stdio (no auth, for local use).

Spawned by stdio MCP clients (Claude Code, Cursor, …) configured with:

    {
      "mcpServers": {
        "museforge": { "command": "museforge-mcp" }
      }
    }

Or run directly: ``python -m museforge.mcp_server``.

This reuses the same tool definitions as the HTTP server (``museforge.mcp_http``)
so the two transports stay in lockstep.
"""

from __future__ import annotations

from museforge.mcp_http import _build_mcp_server


def main() -> None:
    """Run the MCP server over stdio."""
    _build_mcp_server().run(transport="stdio")


if __name__ == "__main__":
    main()

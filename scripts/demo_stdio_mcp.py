"""Local stdio MCP demo — spawn museforge-mcp, list all 11 tools, run a few.

Usage:
    python scripts/demo_stdio_mcp.py

This uses the stdio MCP transport (no Google OAuth, no HTTP). It is the same binary
the stdio MCP clients (Claude Code, Cursor, etc.) would spawn when configured with:

    {
      "mcpServers": {
        "museforge": { "command": "museforge-mcp" }
      }
    }
"""

from __future__ import annotations

import anyio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

CONSOLE_SCRIPT = ""  # empty = use `python -m museforge.mcp_server` via StdioServerParameters


def _build_command() -> list[str]:
    """Use python -m so we bypass any stale .exe shims and find the installed package."""
    import sys

    return [sys.executable, "-m", "museforge.mcp_server"]


async def main() -> None:
    cmd = _build_command()
    print(f"(spawning: {' '.join(cmd)})\n")
    params = StdioServerParameters(command=cmd[0], args=cmd[1:], env=None)
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            print("=" * 70)
            print("1) initialize")
            print("=" * 70)
            init = await session.initialize()
            print(f"   server:   {init.serverInfo.name} v{init.serverInfo.version}")
            print(f"   protocol: {init.protocolVersion}")
            print(f"   caps:     {list(init.capabilities.model_dump(exclude_none=True).keys())}")

            print()
            print("=" * 70)
            print(f"2) tools/list  ({len((await session.list_tools()).tools)} tools)")
            print("=" * 70)
            tools_resp = await session.list_tools()
            for i, t in enumerate(tools_resp.tools, 1):
                desc_first_line = (t.description or "").splitlines()[0] if t.description else ""
                print(f"   [{i:2d}] {t.name}")
                print(f"        {desc_first_line}")

            print()
            print("=" * 70)
            print("3) tools/call analyze_image_request")
            print('   request: "Create a premium fintech card advertisement"')
            print("=" * 70)
            r1 = await session.call_tool(
                "analyze_image_request",
                {"request": "Create a premium fintech card advertisement"},
            )
            for block in r1.content:
                if hasattr(block, "text"):
                    import json as _json

                    try:
                        obj = _json.loads(block.text)
                        print(_json.dumps(obj, indent=2, ensure_ascii=False))
                    except Exception:
                        print(block.text)

            print()
            print("=" * 70)
            print("4) tools/call create_image_prompt (full pipeline, no model)")
            print('   request: "帮我做一张小红书图文，主题是 3 个 AI 习惯，3:4 极简"')
            print("=" * 70)
            r2 = await session.call_tool(
                "create_image_prompt",
                {
                    "request": "帮我做一张小红书图文，主题是 3 个让效率翻倍的 AI 习惯，3:4，极简，专业",
                    "model": "universal",
                    "prompt_only": False,
                },
            )
            for block in r2.content:
                if hasattr(block, "text"):
                    import json as _json

                    try:
                        obj = _json.loads(block.text)
                        # Show a compact summary
                        intent = obj.get("intent", {})
                        cd = obj.get("creative_direction", {})
                        rec = obj.get("recommended_recipe")
                        pat = obj.get("recommended_pattern")
                        sty = obj.get("recommended_style")
                        techs = [t["name"] if isinstance(t, dict) else getattr(t, "name", "")
                                 for t in (obj.get("key_techniques") or [])]
                        sp = obj.get("super_prompt", "")
                        print(f"   Intent       : {intent.get('use_case')} / {intent.get('category')}")
                        print(f"   Platform     : {intent.get('platform')}  Aspect: {intent.get('aspect_ratio')}")
                        print(f"   Recipe       : {(rec or {}).get('name') if isinstance(rec, dict) else getattr(rec, 'name', None)}")
                        print(f"   Pattern      : {(pat or {}).get('name') if isinstance(pat, dict) else getattr(pat, 'name', None)}")
                        print(f"   Style        : {(sty or {}).get('name') if isinstance(sty, dict) else getattr(sty, 'name', None)}")
                        print(f"   Techniques   : {', '.join(techs[:5])}")
                        print(f"   Concept      : {cd.get('concept', '')[:90]}")
                        print()
                        print("   ---- Super Prompt ----")
                        for line in sp.splitlines():
                            print(f"   {line}")
                        if obj.get("alternative_direction"):
                            print()
                            print(f"   Alternative: {obj['alternative_direction']}")
                        if obj.get("notes"):
                            print()
                            for n in (obj.get("notes") or [])[:3]:
                                print(f"   Note: {n}")
                    except Exception:
                        print(block.text[:1000])

            print()
            print("=" * 70)
            print("[done]")
            print("=" * 70)


anyio.run(main)

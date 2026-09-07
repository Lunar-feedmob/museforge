"""Generate the six demo outputs into examples/.

Run from the repo root:  python scripts/generate_demos.py

Each demo shows the full path: User Request -> Intent -> Retrieved Knowledge -> Recipe ->
Pattern -> Creative Direction -> Techniques -> Super Prompt.
"""

from __future__ import annotations

from pathlib import Path

from museforge.cli.render import render_response
from museforge.knowledge.store import KnowledgeStore
from museforge.services.assistant import MuseForgeAssistant

DEMOS = [
    ("demo-1-xiaohongshu-recruitment", "帮我做一张 AI 公司招聘小红书封面，3:4，极简，专业，有一点编辑感。", "universal"),
    ("demo-2-fintech-card-ad", "Create a premium fintech card advertisement.", "nano-banana-pro"),
    ("demo-3-saas-hero", "Create a clean SaaS / AI product hero visual.", "gpt-image-2"),
    ("demo-4-cinematic-portrait", "Create a realistic cinematic character portrait.", "gpt-image-2"),
    ("demo-5-chinese-infographic", "Create a Chinese infographic about 2026 AI trends.", "gpt-image-2"),
    ("demo-6-multi-panel-comic", "Create a multi-panel comic.", "nano-banana-pro"),
]


def main() -> None:
    out_dir = Path("examples")
    out_dir.mkdir(parents=True, exist_ok=True)
    assistant = MuseForgeAssistant(KnowledgeStore("data"))
    for slug, request, model in DEMOS:
        resp = assistant.generate_response(request, model=model)
        body = render_response(resp)
        text = f"# Demo: {slug}\n\n**User request:** {request}\n\n---\n\n{body}\n"
        (out_dir / f"{slug}.md").write_text(text, encoding="utf-8")
        print(f"wrote examples/{slug}.md")


if __name__ == "__main__":
    main()

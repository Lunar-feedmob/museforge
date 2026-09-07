"""MuseForge CLI.

The primary entry point is ``museforge ask``. Search subcommands expose the knowledge base;
backend commands (ingest/normalize/dedup/extract) are for maintainers, not the README's first
selling point.
"""

from __future__ import annotations

import os
from typing import Annotated

import typer
from rich.console import Console

from museforge.cli.render import render_response
from museforge.knowledge.store import KnowledgeStore
from museforge.providers.llm import provider_from_env
from museforge.services.assistant import MuseForgeAssistant

app = typer.Typer(help="MuseForge — distill image-generation knowledge into better visual prompts.")
console = Console()


def _store() -> KnowledgeStore:
    return KnowledgeStore(os.environ.get("MUSEFORGE_DATA_DIR", "data"))


def _assistant() -> MuseForgeAssistant:
    return MuseForgeAssistant(_store(), llm=provider_from_env())


@app.command()
def ask(
    request: Annotated[str, typer.Argument(help="What image do you want to create?")],
    model: Annotated[str, typer.Option("--model", "-m", help="Target model for a variant.")] = "universal",
    prompt_only: Annotated[bool, typer.Option("--prompt-only", help="Output only the prompt.")] = False,
) -> None:
    """Turn an image idea into a production-ready prompt."""
    resp = _assistant().generate_response(request, model=model, prompt_only=prompt_only)
    console.print(render_response(resp, prompt_only=prompt_only))


def _make_search_group(entity: str, label: str) -> typer.Typer:
    """Build a Typer group with a ``search`` subcommand for one entity type."""
    group = typer.Typer(help=f"Search {label}.")

    @group.command("search")
    def search(
        query: Annotated[str, typer.Argument(help="Search query.")],
        top_k: Annotated[int, typer.Option("--top", "-k", help="Number of results.")] = 5,
    ) -> None:
        """Search the knowledge base."""
        retriever = getattr(_assistant(), entity + "s")
        for item, score in retriever.search(query, top_k):
            name = getattr(item, "name", None) or getattr(item, "title", None) or getattr(item, "id", "?")
            console.print(f"[bold]{name}[/bold]  (score {score:.2f})")
            desc = getattr(item, "description", "") or getattr(item, "goal", "")
            if desc:
                console.print(f"  {desc[:160]}")

    return group


app.add_typer(_make_search_group("case", "cases"), name="cases")
app.add_typer(_make_search_group("prompt", "prompts"), name="prompts")
app.add_typer(_make_search_group("recipe", "recipes"), name="recipes")
app.add_typer(_make_search_group("pattern", "patterns"), name="patterns")
app.add_typer(_make_search_group("style", "styles"), name="styles")
app.add_typer(_make_search_group("technique", "techniques"), name="techniques")


@app.command()
def analyze(
    request: Annotated[str, typer.Argument(help="The request to analyze.")],
) -> None:
    """Analyze a request into a structured intent."""
    intent = _assistant().understand_request(request)
    console.print(intent.model_dump_json(indent=2))


@app.command()
def improve(
    prompt: Annotated[str, typer.Argument(help="The prompt to improve.")],
    feedback: Annotated[str, typer.Option("--feedback", "-f", help="Optional guidance.")] = "",
) -> None:
    """Improve an existing prompt."""
    console.print(_assistant().improve_prompt(prompt, feedback))


@app.command()
def optimize(
    prompt: Annotated[str, typer.Argument(help="The prompt to optimize.")],
    model: Annotated[str, typer.Option("--model", "-m", help="Target model.")] = "nano-banana-pro",
) -> None:
    """Produce a model-specific variant of a prompt."""
    result = _assistant().optimize_for_model(prompt, model)
    console.print(f"[bold]Model:[/bold] {result.model}  [bold]basis:[/bold] {result.optimization_basis}")
    console.print(result.prompt)


@app.command()
def sources() -> None:
    """List registered sources."""
    store = _store()
    for src in store.load("source"):
        console.print(f"[bold]{getattr(src, 'id', '?')}[/bold]  {getattr(src, 'license', '') or 'no license'}")


@app.command()
def stats() -> None:
    """Show knowledge-base statistics."""
    store = _store()
    for entity, count in store.stats().items():
        console.print(f"{entity:>18}: {count}")


# -- backend commands (maintainers) -------------------------------------

@app.command()
def ingest(
    source_id: Annotated[str, typer.Argument(help="Source id.")],
    source_url: Annotated[str, typer.Argument(help="Local directory or URL.")],
    license: Annotated[str, typer.Option("--license", "-l", help="Source license.")] = "",
) -> None:
    """Ingest a source repository into the knowledge store (background)."""
    from museforge.pipeline import IngestionPipeline

    report = IngestionPipeline(_store()).ingest(source_id, source_url, license=license or None)
    console.print(report)


@app.command()
def normalize(
    text: Annotated[str, typer.Argument(help="Text to normalize.")],
) -> None:
    """Normalize text (strip markdown/URLs/whitespace)."""
    from museforge.normalizers.text import normalize as _normalize

    console.print(_normalize(text))


@app.command()
def dedup(
    level: Annotated[str, typer.Argument(help="exact | normalized | near | semantic | visual-intent")],
    text: Annotated[str, typer.Argument(help="Comma-separated texts to deduplicate.")],
) -> None:
    """Deduplicate a list of texts at a given level."""
    from museforge.dedup.dedup import Deduplicator

    items = [t.strip() for t in text.split("|") if t.strip()]
    result = Deduplicator().dedup(items, level=level)
    console.print(f"kept {len(result.kept)} of {len(items)} (removed {result.removed})")
    for item in result.kept:
        console.print(f"  - {str(item)[:120]}")


def main() -> None:
    _force_utf8()
    app()


def _force_utf8() -> None:
    """Reconfigure stdout/stderr to UTF-8 so CJK output is not mangled on Windows."""
    import contextlib
    import sys

    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            with contextlib.suppress(Exception):
                stream.reconfigure(encoding="utf-8")


if __name__ == "__main__":
    main()

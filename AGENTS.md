# AGENTS.md — MuseForge agent guidance

This file guides AI agents (Claude Code, Cursor, Codex, etc.) working on MuseForge.

## What MuseForge is

MuseForge turns a natural-language image idea into a production-ready image-generation prompt,
by retrieving and applying distilled knowledge (recipes, visual patterns, styles, techniques,
prompt DNA) from high-quality image-generation repositories.

## What MuseForge is NOT

- Not a prompt collection / awesome list.
- Not a prompt cleaner.
- Not a prompt database frontend.
- Not an image-generation API client (V0).

## Core principles

1. **Knowledge > Collection** — store abstractions, not raw dumps.
2. **Patterns > Prompt Dumps** — a pattern is reusable; a prompt is one-off.
3. **Recipes > Random Examples** — a recipe is a method; an example is a data point.
4. **Quality > Quantity** — a few hundred curated entities beat ten thousand prompts.
5. **Reusable Systems > Viral Prompts** — systems transfer; viral prompts don't.
6. **Creative Direction > Prompt Expansion** — design first, compose second.
7. **Attribution > Copying** — provenance is a schema field.

## Architecture

```
Knowledge Layer (JSON/JSONL + schemas)
  → Retrieval Layer (metadata + BM25/fuzzy + embedding interface)
  → Service Layer (Assistant → IntentAnalyzer → CreativeDirector → PromptComposer → ModelOptimizer)
  → Delivery Layer (CLI; MCP as a future adapter)
```

Ingestion (Collector → Parser → Normalizer → LicenseCheck → Dedup → Analyzer → Extractor →
KnowledgeLinker → Store) is a **background** capability, not the user-facing product.

## Rules

- Never copy a prompt whose license is unclear. Store metadata + source URL + derived analysis.
- Never claim a model "performs best" without a labeled, reliable source.
- Keep the core path working with no API key (heuristic fallback).
- Keep schemas and Pydantic models in sync.
- Run `pytest`, `ruff`, and `mypy` before committing.

## Layout

- `schemas/` — JSON Schema for every knowledge entity.
- `src/museforge/` — the Python package (see `docs/architecture.md` for the module map).
- `data/` — the knowledge store (sources, prompts, cases, recipes, patterns, styles,
  techniques, dna, models, features).
- `docs/` — architecture, methodology, knowledge model, comparisons, roadmap.
- `tests/` — behavior tests.
- `examples/` — demo outputs.

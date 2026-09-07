# CLAUDE.md — MuseForge development rules

Rules for Claude Code (and any AI agent) working on this repository.

## Project identity

MuseForge is an **AI image-generation assistant** that distills image-generation knowledge
into better visual prompts. It is **not** a prompt collection, an awesome list, or a prompt
cleaner.

## Non-negotiable rules

- **Do not turn MuseForge into a prompt dump.** Store knowledge (recipe/pattern/style/
  technique/DNA), not raw prompt collections.
- **Preserve attribution.** Every redistributed prompt carries `source_repo`, `source_url`,
  `author`, and `license`. Unclear license → do not copy the prompt text.
- **Prefer reusable knowledge abstractions.** A new recipe/pattern covers a thousand prompts.
- **Do not duplicate knowledge unnecessarily.** Deduplicate at the visual-intent level.
- **Recipes and Patterns are first-class entities.** They are the core value, not prompts.
- **User-facing features belong in services, not CLI internals.** The CLI is a thin shell.
- **Keep MCP as an adapter.** MCP tools map onto Service Layer methods, never onto the
  ingestion pipeline or CLI internals.
- **Do not introduce image-generation dependencies in V0.** Output is CreativeDirection +
  Prompt. No image generation, storage, scoring, or benchmark.
- **Do not invent benchmark claims.** Model knowledge carries a `source_type` label
  (official / repository-derived / community-derived / inferred / experimental / unverified).
- **Run tests before committing.** `pytest`, `ruff`, `mypy` must pass.

## Architecture invariants

- Knowledge Layer → Service Layer → CLI (MCP is a future adapter over the Service Layer).
- The Service Layer depends on `LLMProvider` / `EmbeddingProvider` protocols, never on a
  specific vendor SDK.
- The Knowledge Store is plain JSON/JSONL in V0.
- The core path (`museforge ask`) works with no API key (heuristic fallback).

## Conventions

- Python 3.12+, typed, Pydantic models mirror the JSON schemas in `schemas/`.
- Keep schemas (`schemas/*.schema.json`) and Pydantic models in sync.
- Tests cover behavior (schema validation, normalization, dedup, retrieval, matching,
  routing, direction, composition, CLI), not getters.

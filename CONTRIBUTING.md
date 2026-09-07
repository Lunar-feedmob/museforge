# Contributing to MuseForge

Thanks for your interest in contributing. MuseForge is a **knowledge system**, not a prompt
dump — contributions should add *reusable knowledge*, not just more prompts.

## What to contribute

- **Recipes** — a method for a class of image task (steps, decision points, failure modes).
- **Visual Patterns** — a reusable visual structure.
- **Styles** — a reusable visual system.
- **Techniques** — a prompt-engineering lever.
- **Cases** — a complete, analyzed example (with full attribution).
- **Model knowledge** — with a `source_type` label.

## Attribution is non-negotiable

Every redistributed prompt must carry:

- `source_repo` — the repository it came from.
- `source_url` — a link to the original.
- `author` — the original author (if known).
- `license` — the license of the source.

**If the license is unclear, do not copy the prompt text.** Store metadata + source URL +
derived analysis (pattern/technique/knowledge) only.

## Process

1. Open an issue describing what you want to add and why it's reusable knowledge.
2. Follow the schema in `schemas/` for the entity type.
3. Add the entity to the right `data/` directory.
4. Run `pytest`, `ruff`, and `mypy`.
5. Open a PR.

## Code of conduct

Be kind. Attribute your sources. Don't fabricate benchmark claims.

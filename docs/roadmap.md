# Roadmap

## V0 (current) — the knowledge core

**Done:**

- Research of 15+ real image-generation repositories.
- `repository-comparison.md`, `best-of-existing-repos.md`, `feature-comparison.md`.
- Source registry (15 sources).
- Schemas (JSON Schema + Pydantic) for source, prompt, case, recipe, pattern, style,
  technique, DNA, model, feature, creative-direction.
- Ingestion pipeline: collector, parser, normalizer, license check, dedup (5 levels),
  analyzer, extractor, knowledge linker, store.
- Retrieval: metadata + BM25/fuzzy, typed retrievers, embedding interface.
- MuseForgeAssistant + Creative Director + Prompt Composer + Model Optimizer.
- CLI: `ask`, search groups, `analyze`, `improve`, `optimize`, `sources`, `stats`, and
  backend `ingest`/`normalize`/`dedup`.
- 6 demos + synthetic seed knowledge.
- Tests (58), ruff, mypy.

**Explicitly out of scope in V0:**

- Image generation (no API calls, no image storage, no scoring, no benchmark).
- MCP server (architecture is ready; see `mcp-roadmap.md`).
- Web gallery.

## V1 — the first product surface

- **Web gallery** — browse cases/patterns/recipes with filter + grid.
- **Semantic search** — plug a real embedding model behind the `EmbeddingProvider` interface.
- **Prompt remix** — remix at the knowledge level (swap pattern/style/technique).
- **Variables** — fill `[VARIABLE]` templates from user input.
- **Collections** — user-curated collections of recipes/patterns.
- **Related patterns** — explicit knowledge-linking in the UI.
- **JSON prompt output** — emit prose + JSON from one CreativeDirection.
- **Contribution workflow** — contribute knowledge (recipe/pattern), not just prompts.

## V2 — the agent surface

- **MCP server** — expose the Service Layer as MCP tools (see `mcp-roadmap.md`).
- **Image generation** — plug an image-generation provider behind a protocol.
- **Image comparison** — compare alternative directions side by side.
- **Auto prompt improvement loop** — generate → score → improve.

## Later

- **Benchmark** — a real, labeled evaluation of models (only with evidence).
- **Community contributions** — a public contribution pipeline.
- **Prompt ranking** — quality signals from usage.
- **Personal visual memory** — favorites + history feed a personal knowledge base.

## Anti-goals (never)

- "10,000+ prompts" as a headline.
- Verbatim prompt dumps.
- Un-attributed aggregation.
- Model-specific knowledge bases (model notes are a layer, not a base).
- Fake benchmark claims.

# Architecture

> MuseForge's layered architecture. The invariant: **Knowledge Layer → Service Layer → CLI**,
> with MCP as a future adapter over the Service Layer (never over the CLI internals).

## Layers

```
┌─────────────────────────────────────────────────────────────┐
│  Delivery Layer                                              │
│  CLI (Typer)          [future] MCP Adapter                   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│  Service Layer                                               │
│  MuseForgeAssistant                                          │
│    ├─ IntentAnalyzer                                         │
│    ├─ CreativeDirector                                       │
│    ├─ PromptComposer                                         │
│    └─ ModelOptimizer                                         │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│  Retrieval Layer                                             │
│  CaseRetriever · RecipeRetriever · PatternRetriever          │
│  StyleRetriever · TechniqueRetriever · DnaRetriever          │
│  PromptRetriever · SourceRetriever                           │
│  (metadata search + BM25/fuzzy + EmbeddingProvider interface)│
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│  Knowledge Layer                                             │
│  KnowledgeStore (JSON/JSONL)                                 │
│  Schemas (JSON Schema + Pydantic)                            │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│  Ingestion Pipeline (background, not user-facing)            │
│  Collector → Parser → Normalizer → LicenseCheck → Dedup      │
│  → Analyzer → Extractor → KnowledgeLinker → KnowledgeStore   │
└─────────────────────────────────────────────────────────────┘
```

## Design invariants

1. **The Service Layer never depends on a specific LLM SDK.** It depends on an `LLMProvider`
   protocol. Anthropic/OpenAI/Gemini/local are implementations.
2. **The Retrieval Layer never depends on a specific embedding vendor.** It depends on an
   `EmbeddingProvider` protocol. Local embeddings are the default; OpenAI/others are optional.
3. **The Knowledge Layer is plain JSON/JSONL.** No database in V0. The store is a thin,
   typed access layer so a real database can replace it later.
4. **The CLI is a thin shell over the Service Layer.** No business logic in CLI internals.
5. **MCP is an adapter over the Service Layer.** Adding MCP later requires no refactor of the
   knowledge or service layers (see `docs/mcp-roadmap.md`).
6. **No image-generation dependency in V0.** The output is CreativeDirection + Prompt.

## Module map

```
src/museforge/
  collectors/      # fetch/read source repositories
  parsers/         # parse markdown/json/html into raw records
  normalizers/     # normalize text (strip markdown, URLs, whitespace)
  licensing/       # license + attribution checks
  dedup/           # exact/normalized/near/semantic/visual-intent dedup
  analyzers/       # intent analysis, case analysis
  extractors/      # recipe/pattern/style/technique/dna extraction
  knowledge/       # schemas (pydantic), store, entities
  retrieval/       # retrievers + search backends
  creative_director/  # CreativeDirector
  prompt_composer/    # PromptComposer
  model_optimizer/    # ModelOptimizer
  providers/       # LLMProvider, EmbeddingProvider protocols + impls
  services/        # MuseForgeAssistant, IntentAnalyzer
  cli/             # Typer CLI
```

## Data flow (the user path)

```
User request
  → IntentAnalyzer.understand_request()      → Intent
  → Retrieval (cases/recipes/patterns/styles/techniques/dna)
  → CreativeDirector.design()               → CreativeDirection
  → PromptComposer.compose()                → Super Prompt
  → ModelOptimizer.optimize()               → model-specific variant
  → Assistant.generate_response()           → structured answer
```

## Data flow (the ingestion path)

```
Repository Discovery → Collector → Parser → Normalizer
  → LicenseCheck → Dedup → CaseAnalyzer → PromptAnalyzer
  → RecipeExtractor → PatternExtractor → StyleExtractor
  → TechniqueExtractor → DnaExtractor → KnowledgeLinker → KnowledgeStore
```

## Provider-agnosticism

```python
class LLMProvider(Protocol):
    def complete(self, prompt: str, *, system: str | None = None) -> str: ...

class EmbeddingProvider(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]: ...
```

- `AnthropicProvider` is provided for convenience (this project is developed in Claude Code),
  but the core never imports `anthropic` directly.
- `LocalEmbeddingProvider` (hash-based / TF-IDF fallback) is the V0 default so the system
  works with no API key.
- If no LLM is configured, the Assistant falls back to **deterministic heuristics** (rule-based
  intent analysis + retrieval + template composition), so `museforge ask` still works offline.

## Why this architecture survives MCP

The MCP tools map 1:1 onto Service Layer methods:

```
create_image_prompt        → Assistant.generate_response()
recommend_image_direction  → CreativeDirector.design()
search_image_cases         → CaseRetriever.search()
search_image_recipes       → RecipeRetriever.search()
search_visual_patterns     → PatternRetriever.search()
search_image_styles        → StyleRetriever.search()
search_prompt_techniques   → TechniqueRetriever.search()
improve_image_prompt       → Assistant.improve_prompt()
optimize_image_prompt      → ModelOptimizer.optimize()
analyze_image_request      → IntentAnalyzer.understand_request()
```

No MCP tool touches the ingestion pipeline or the CLI internals.

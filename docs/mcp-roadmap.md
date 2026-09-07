# MCP Roadmap

MuseForge will become an MCP server. This document records the plan and the architectural
guarantee that makes it a *small* change, not a refactor.

## The architectural guarantee

```
Knowledge Layer → Service Layer → CLI          (V0)
Knowledge Layer → Service Layer → MCP Adapter  (future)
```

The MCP adapter sits **over the Service Layer**, exactly where the CLI sits. It never touches
the ingestion pipeline or the CLI internals. Because the Service Layer is already
provider-agnostic and returns typed objects, the MCP tools are thin wrappers.

## The MCP tools

Each MCP tool maps 1:1 onto a Service Layer method:

| MCP tool | Service Layer method |
|---|---|
| `create_image_prompt` | `MuseForgeAssistant.generate_response()` |
| `recommend_image_direction` | `CreativeDirector.design()` |
| `search_image_cases` | `CaseRetriever.search()` |
| `search_image_prompts` | `PromptRetriever.search()` |
| `search_image_recipes` | `RecipeRetriever.search()` |
| `search_visual_patterns` | `PatternRetriever.search()` |
| `search_image_styles` | `StyleRetriever.search()` |
| `search_prompt_techniques` | `TechniqueRetriever.search()` |
| `improve_image_prompt` | `MuseForgeAssistant.improve_prompt()` |
| `optimize_image_prompt` | `ModelOptimizer.optimize()` |
| `analyze_image_request` | `IntentAnalyzer.understand_request()` |

## What the MCP server will NOT do

- It will not expose the ingestion pipeline (`ingest`/`normalize`/`dedup`/`extract`) — those
  are maintainer tools, not agent tools.
- It will not call an image-generation API in V0 (that is a V2 concern, behind a provider
  protocol).
- It will not bypass the license/attribution rules — every returned prompt carries provenance.

## Why this is a small change

1. The Service Layer already returns typed objects (`AssistantResponse`, `CreativeDirection`,
   `Intent`, entities).
2. The retrieval layer already exposes `search(query, top_k)` for every entity type.
3. The provider layer is already protocol-based, so the MCP server can run with or without an
   LLM key.

The only new code is a thin adapter that maps MCP tool schemas to these methods and serializes
the results.

## When

V2, after the V1 web gallery and semantic search. The knowledge model and service layer are
already stable enough that the MCP adapter can be added without touching them.

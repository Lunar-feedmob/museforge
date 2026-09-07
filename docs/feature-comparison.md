# Feature Comparison

> Feature mining across surveyed repositories. The full machine-readable matrix is in
> `data/features/features.json`. This document gives the adoption decision for each feature.

## Adoption tiers

- **V0** — must ship now (the core user path).
- **V1** — next (web gallery, advanced search, remix, collections).
- **V2** — MCP, image generation, comparison, auto-improvement loop.
- **Later** — benchmark, community ranking, personal visual memory.
- **Do Not Build** — anti-goals (things that would turn MuseForge into a prompt dump).

---

## V0 Features (must implement)

| Feature | Why it's in V0 | MuseForge's take |
|---|---|---|
| `search` | A knowledge base is useless without search | Search over typed knowledge (case/recipe/pattern/style/technique) |
| `full_text_search` | Users search by wording | BM25 over normalized text |
| `category_filter` | Category is the primary axis | First-class field on every entity |
| `style_filter` | Style is orthogonal to category | Style is a first-class entity |
| `model_filter` | Users care about target model | Model is a note layer, not a separate base |
| `prompt_templates` | Templates are the core value | Templates become recipes + patterns + DNA |
| `related_styles` | styles[] already links cases to styles | Style entity with related_patterns/techniques |
| `tags` | Tags capture what categories miss | tags + use_case + theme |
| `model_badge` | Model is a key filter | Model badge + source_type badge |
| `attribution_display` | Ethical + legal requirement | Schema field, non-negotiable |
| `source_link` | Enables verification | source_url on every entity |
| `model_specific_notes` | Model quirks matter | Notes carry a source_type label |
| `prompt_generator` | The terminal value | Director + composer, not template fill |
| `visual_director_workflow` | Planning before prompting | Platform-agnostic Creative Director |
| `json_style_pack` | Reusable visual systems | Style + variables + examples |
| `featured_prompts` | Quality signal | Featured recipes/patterns |

---

## V1 Features (next)

| Feature | Why V1 | MuseForge's take |
|---|---|---|
| `semantic_search` | Needs an embedding layer | Provider-agnostic EmbeddingProvider; local first |
| `prompt_copy` | Needs a web surface | Copy the composed Super Prompt |
| `prompt_remix` | Bridge from collection to creation | Remix at knowledge level |
| `prompt_variables` | Reuse without rewriting | Variables in DNA and recipes |
| `json_prompt` | Structured output | Emit prose + JSON from one CreativeDirection |
| `image_preview` | Needs seed images | Previews are evidence, not the product |
| `collections` | User's own taxonomy | Collections of recipes/patterns |
| `similar_prompts` | Basis of recommendation | Similarity at visual-intent level |
| `related_prompts` | Curated discovery | Knowledge linking |
| `gallery` | Natural browse surface | Gallery of patterns/recipes |
| `grid` | Standard layout | Grid + filter + sort |
| `multi_language` | Global audience | Compose in user's language |
| `contribution_workflow` | Community growth | Contribute knowledge, not prompts |

---

## V2 Features

| Feature | Why V2 | MuseForge's take |
|---|---|---|
| `prompt_comparison` | Needs multiple directions | Compare alternative directions |
| `before_after` | Needs image generation | Before/after as a recipe category |
| `prompt_editor` | Needs a web surface | Edit the CreativeDirection |
| `recommendation_skill` | Needs MCP | MCP server over the service layer |

---

## Later Features

| Feature | Why later | MuseForge's take |
|---|---|---|
| `favorites` | Needs accounts | Feeds personal visual memory |
| `prompt_history` | Needs accounts | Feeds personal visual memory |
| `random_prompt` | Low value | Random pattern/style |
| `trending_prompts` | Needs ranking data | Trending patterns |
| `automated_ingestion` | Needs scale | Feeds the knowledge pipeline |

---

## Do Not Build

| Anti-feature | Why not |
|---|---|
| "10,000+ prompts" as a headline | Quantity is not quality; MuseForge's value is design knowledge |
| Verbatim prompt dump | Violates the "Knowledge > Collection" principle |
| Un-attributed aggregation | Violates licensing and ethics |
| Model-specific knowledge bases | Duplicates knowledge; model notes should be a layer |
| PDF/HTML prompt distribution | Un-queryable, un-diffable |
| Image generation in V0 | Explicitly out of scope (see roadmap) |
| Fake benchmark claims | No evidence → no claim (see model-knowledge.md) |

---

## Feature provenance map

The strongest features come from a small set of repositories:

- **freestylefly/awesome-gpt-image-2** → structured cases, two-axis tags, templates, featured,
  attribution, gallery.
- **VigoZhao/AI-Visual-Prompt-Cookbook** → JSON style packs, variables + examples.
- **YouMind family** → scale, multilingual, recommendation skill, automated ingestion.
- **wuyoscar/GPT-Image2-Skill** → CLI + skill delivery, JSON-style prompts.
- **mythkiven/rednote-director-skill** → visual director workflow.
- **ZeroLu/awesome-nanobanana-pro** → templated `[VARIABLE]` prompts.
- **jamez-bondos/awesome-gpt4o-images** → case template, contribution contract.
- **alexewerlof / xcaeser** → typed JSON prompt schemas.

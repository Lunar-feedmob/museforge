# MuseForge

**Distill great image-generation knowledge into better visual prompts.**

> Your creative copilot for AI image generation.
>
> 简体中文版: [README.zh-CN.md](README.zh-CN.md)

Describe what you want. MuseForge will:

1. **Understand your intent** — infer the use case, platform, aspect ratio, style, and likely
   visual pattern from a natural-language request.
2. **Find proven image-generation patterns** — retrieve recipes, visual patterns, styles, and
   techniques from its knowledge base.
3. **Recommend a visual direction** — a Creative Director designs the image, not a template.
4. **Design the composition** — hierarchy, foreground/midground/background, lighting, color,
   typography, negative space.
5. **Apply relevant prompt techniques** — text rendering, product preservation, brand
   preservation, camera/lens control, whitespace, and more.
6. **Produce a production-ready prompt** — a structured, task-dependent Super Prompt that is
   clear, specific, visually coherent, non-redundant, and free of low-information adjectives.

```
Idea
  ↓
Intent analysis
  ↓
Knowledge retrieval (cases / recipes / patterns / styles / techniques / DNA)
  ↓
Creative Director (design the image)
  ↓
Prompt Composer (turn the design into a prompt)
  ↓
Model Optimizer (model-specific variant)
  ↓
Structured answer + Super Prompt
```

---

## What MuseForge is

MuseForge is an **AI image-generation assistant** that distills image-generation knowledge
into better visual prompts. It acts like a **Creative Director + Prompt Engineer**.

It is the result of systematically studying 17+ high-quality image-generation repositories and
distilling their wisdom into a typed knowledge model — recipes, visual patterns, styles,
techniques, and prompt DNA — so it can recommend *how to design an image*, not just *which
prompt to copy*.

## What MuseForge is NOT

- ❌ A prompt collection / awesome list.
- ❌ A prompt cleaner / formatter.
- ❌ A prompt database frontend.
- ❌ An image-generation API client (V0 does not call any image model).
- ❌ A benchmark or leaderboard.

> *Knowledge > Collection. Patterns > Prompt Dumps. Recipes > Random Examples. Quality >
> Quantity. Reusable Systems > Viral Prompts. Creative Direction > Prompt Expansion.
> Attribution > Copying.*

---

## 30-second demo

```bash
$ museforge ask "帮我做一张 AI 公司招聘小红书封面，3:4，极简，专业，有一点编辑感。"
```

MuseForge doesn't just return a prompt — it returns a **designed direction**:

```
Intent: recruitment marketing / social media poster
Platform: Xiaohongshu  Aspect ratio: 3:4

## Creative Direction
Concept: Communicate a message clearly and elegantly.
Goal: A text-first editorial poster with clear hierarchy.
Rationale: the Editorial Poster recipe matches the recruitment marketing use case;
           the Editorial Text-first Poster pattern fits the visual goal;
           the editorial minimalism style matches the requested aesthetic;
           5 technique(s) apply to this task.

## Recommended Recipe: Editorial Poster
  1. Set canvas/format and aspect ratio.
  2. Define the visual goal and message.
  3. Choose the layout (text-first, grid, centered).
  4. Place the headline as the dominant element.
  5. Add supporting text with clear hierarchy.
  6. Add a supporting illustration or icon.
  7. Select the style (editorial minimalism, retro, Swiss).
  8. Choose a restrained color palette.
  9. Specify typography (headline + supporting).
  10. Add details and constraints (text readability, low density).

## Recommended Pattern: Editorial Text-first Poster
Headline-first layout with supporting text and illustration.

## Style: editorial minimalism

## Composition
text-first with a single focal point

## Key Techniques
text rendering, visual hierarchy, whitespace / negative space,
negative constraints, reference image

## Super Prompt
Format: 3:4 Xiaohongshu
Visual goal: Communicate a message clearly and elegantly.
Layout: text-first with a single focal point
Visual hierarchy: headline -> supporting text -> illustration
Style: editorial minimalism
Color: muted, 1-2 accent colors
Typography: strong sans-serif or serif headline, small supporting text
Negative space: generous margins
Details: small illustration or icon
Constraints: text readability first; low density
Avoid: clutter; high density; many competing elements
```

Six full demos are in [`examples/`](examples/):

1. [`demo-1-xiaohongshu-recruitment.md`](examples/demo-1-xiaohongshu-recruitment.md) — Xiaohongshu recruitment cover.
2. [`demo-2-fintech-card-ad.md`](examples/demo-2-fintech-card-ad.md) — Premium fintech card advertisement.
3. [`demo-3-saas-hero.md`](examples/demo-3-saas-hero.md) — Clean SaaS / AI product hero.
4. [`demo-4-cinematic-portrait.md`](examples/demo-4-cinematic-portrait.md) — Cinematic character portrait.
5. [`demo-5-chinese-infographic.md`](examples/demo-5-chinese-infographic.md) — Chinese-language infographic.
6. [`demo-6-multi-panel-comic.md`](examples/demo-6-multi-panel-comic.md) — Multi-panel comic.

---

## Quick start

### Install

```bash
git clone https://github.com/Lunar-feedmob/museforge.git
cd museforge
pip install -e ".[dev]"
```

No API key is required. The core path works offline with deterministic heuristics. To enable
LLM-powered intent understanding, analysis, and composition, configure a provider in `.env`:

```bash
cp .env.example .env
# edit .env and set your provider (e.g. ANTHROPIC_API_KEY=... or another vendor's key)
```

### Ask

```bash
museforge ask "Create a premium fintech card advertisement"
museforge ask "Create a clean SaaS AI product hero" --model gpt-image-2
museforge ask "Create a Chinese infographic about AI trends" --prompt-only
```

### Search the knowledge base

```bash
museforge recipes search "poster"
museforge patterns search "product hero"
museforge styles search "editorial"
museforge techniques search "text rendering"
museforge cases search "fintech"
museforge prompts search "luxury product"
```

### Analyze, improve, optimize

```bash
museforge analyze "帮我做一张 AI 公司招聘小红书封面"        # intent analysis
museforge improve "amazing stunning product shot"          # strip low-info adjectives
museforge optimize "A product hero shot" --model nano-banana-pro  # model-specific variant
```

### Inspect

```bash
museforge stats     # knowledge-base counts
museforge sources   # registered source repositories
```

---

## CLI reference

```
museforge ask "..." [--model MODEL] [--prompt-only]
    Turn an image idea into a structured creative direction + Super Prompt.

museforge analyze "..."
    Analyze a request into a structured Intent (use case, platform, aspect ratio, …).

museforge improve "..." [--feedback "..."]
    Improve an existing prompt (strip low-information adjectives + append feedback).

museforge optimize "..." --model MODEL
    Produce a model-specific variant of a prompt. The output carries an
    `optimization_basis` label (repository-derived / community-derived / heuristic).

museforge {cases,prompts,recipes,patterns,styles,techniques} search "..." [--top K]
    Search the knowledge base.

museforge sources   List registered sources (license, attribution requirements).
museforge stats      Show knowledge-base counts per entity type.

# Backend (maintainers, not the README's first selling point)
museforge ingest  SOURCE_ID SOURCE_URL [--license LICENSE]
museforge normalize TEXT
museforge dedup {exact|normalized|near|semantic|visual-intent} TEXT1|TEXT2|...
```

### `--model` values

`universal` (default), `gpt-image`, `gpt-image-2`, `nano-banana`, `nano-banana-pro`,
`seedream` (and aliases). Universal returns no model-specific variant; the others append the
model's known guidance and label the `optimization_basis`.

---

## What MuseForge knows

MuseForge stores **typed knowledge**, not raw prompts.

| Entity | What it is | Why it matters |
|---|---|---|
| **Case** | A complete, analyzed example (subject, composition, lighting, style, …) | "Has MuseForge seen something like this before?" |
| **Recipe** | A method for a class of image task (steps, decision points, failure modes) | The *most valuable* entity. One recipe covers a thousand prompts. |
| **Visual Pattern** | A reusable visual structure (e.g. Breakout Product Hero) | Transfers across products, brands, and subjects. |
| **Style** | A reusable visual system (e.g. editorial minimalism) | Strictly separate from Category (what the image is *for*). |
| **Technique** | A prompt-engineering lever (e.g. text rendering, product preservation) | The smallest unit of "how to ask" that transfers. |
| **Prompt DNA** | A composable prompt structure unit | Replace the variables, keep the visual system. |
| **Model** | What a model can do, with a `source_type` label | Never an unverified benchmark claim. |
| **Source** | A repository or origin | Attribution is a schema field, not an afterthought. |

Every recommendation is **explainable**: the Assistant can always say *why* it recommended a
direction ("this case instantiates the Breakout Product Hero pattern, which the Product Hero
Ad recipe recommends").

---

## The pipeline

```
User request
  → IntentAnalyzer.understand_request()       → Intent
  → Retrieval (cases / recipes / patterns / styles / techniques / DNA)
  → CreativeDirector.design()                 → CreativeDirection
  → PromptComposer.compose()                  → Super Prompt
  → ModelOptimizer.optimize()                 → model-specific variant
  → MuseForgeAssistant.generate_response()    → structured answer
```

V0 ships a **deterministic heuristic** for every stage so `museforge ask` works with no API
key. When an LLM provider is configured, those same stages use it.

---

## How MuseForge differs

| Typical prompt collection | MuseForge |
|---|---|
| Stores **text** | Stores **typed knowledge with links** |
| "What prompt exists?" | "How should I design this image, and why?" |
| Scales by adding more prompts | Scales by adding **abstractions** (a new recipe covers a thousand prompts) |
| One-off inspiration | Reusable systems |
| Attribution is an afterthought | Attribution is a schema field (`source_repo`, `source_url`, `author`, `license`) |
| "10,000+ prompts" as the headline | "Knows how to design an image" as the headline |
| No Creative Director | A real Creative Director designs first, then composes |

The closest existing project to MuseForge's philosophy is
[`freestylefly/awesome-gpt-image-2`](https://github.com/freestylefly/awesome-gpt-image-2)
("Prompt as Code" — atomic schema, templates). MuseForge goes one level up: **Recipe** (a
method with steps and failure modes), **Visual Pattern** (a reusable visual structure), and a
**Creative Director** that selects and adapts them.

---

## Research foundation

MuseForge's knowledge model is grounded in a systematic study of 17+ high-quality
image-generation repositories. See:

- [`docs/repository-comparison.md`](docs/repository-comparison.md) — evidence base for
  every design decision (what to inherit, improve, avoid).
- [`docs/best-of-existing-repos.md`](docs/best-of-existing-repos.md) — distilled assets
  (best recipes, patterns, techniques, styles, metadata ideas).
- [`docs/feature-comparison.md`](docs/feature-comparison.md) — feature adoption decisions
  (V0 / V1 / V2 / Later / Do Not Build).

## Architecture

- [`docs/architecture.md`](docs/architecture.md) — layered architecture (Knowledge →
  Retrieval → Service → CLI; MCP as a future adapter).
- [`docs/methodology.md`](docs/methodology.md) — the knowledge-acquisition and
  prompt-generation pipelines.
- [`docs/knowledge-model.md`](docs/knowledge-model.md) — the full knowledge schema and
  entity relationships.
- [`docs/mcp-roadmap.md`](docs/mcp-roadmap.md) — how MCP will be added (small change,
  not a refactor).

---

## Licensing & attribution

> *"Unclear license → do not copy the prompt text."*

For every redistributed prompt, MuseForge records `source_repo`, `source_url`, `author`,
and `license`. For every model claim, it records a `source_type` label (`official` /
`repository-derived` / `community-derived` / `inferred` / `experimental` / `unverified`).

See [`docs/licensing.md`](docs/licensing.md) for the full policy and the license decision
table.

The seed knowledge in `data/` is **synthetic** (authored for MuseForge), with
`source_repositories` pointing at the repositories that *inspired* each abstraction. The
three seed prompts are annotated exemplars from MIT / CC BY 4.0 sources with full attribution.

---

## Status

**V0** — knowledge acquisition, deduplication, analysis, extraction, retrieval, creative
direction, and prompt composition. No image-generation API (yet).

- ✅ 17+ repositories studied.
- ✅ 9 typed knowledge entities + JSON Schema + Pydantic models.
- ✅ 5-level deduplication (exact → normalized → near → semantic → visual-intent).
- ✅ Retrieval (metadata + BM25/fuzzy + provider-agnostic embedding interface).
- ✅ Creative Director + Prompt Composer + Model Optimizer.
- ✅ CLI (`ask`, search groups, `analyze`, `improve`, `optimize`, `sources`, `stats`,
  backend `ingest`/`normalize`/`dedup`).
- ✅ 6 demos + synthetic seed knowledge.
- ✅ 58 tests, ruff clean, mypy clean.

See [`docs/roadmap.md`](docs/roadmap.md) for V1+ (web gallery, semantic search, prompt remix,
MCP server, image generation) and the anti-goals (what MuseForge will *never* do).

## Self-check

The V0 self-check from the project brief is answered honestly in
[`docs/self-check.md`](docs/self-check.md).

---

## Contributing

Contributions should add **reusable knowledge** (recipes, patterns, styles, techniques,
DNA), not raw prompts. Attribution is non-negotiable: every redistributed prompt must carry
`source_repo`, `source_url`, `author`, and `license`. Unclear license → store metadata +
analysis only.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full contribution guide and the knowledge
schema (`schemas/`).

## License

MIT. Redistributed third-party prompts carry their own license and attribution — see
[`docs/licensing.md`](docs/licensing.md).

## Acknowledgements

MuseForge is inspired by and grounded in the work of the maintainers and contributors of the
repositories studied in [`docs/repository-comparison.md`](docs/repository-comparison.md). In
particular:

- [`freestylefly/awesome-gpt-image-2`](https://github.com/freestylefly/awesome-gpt-image-2) —
  the "Prompt as Code" atomic-schema idea.
- [`VigoZhao/AI-Visual-Prompt-Cookbook`](https://github.com/VigoZhao/AI-Visual-Prompt-Cookbook)
  — the "copy one JSON, get a style" framing.
- [`wuyoscar/GPT-Image2-Skill`](https://github.com/wuyoscar/GPT-Image2-Skill) — the
  CLI + skill delivery model.
- [`mythkiven/rednote-director-skill`](https://github.com/mythkiven/rednote-director-skill)
  — the visual-director workflow.
- [`ZeroLu/awesome-nanobanana-pro`](https://github.com/ZeroLu/awesome-nanobanana-pro) —
  templated `[VARIABLE]` prompts.
- [`jamez-bondos/awesome-gpt4o-images`](https://github.com/jamez-bondos/awesome-gpt4o-images)
  — the case template + attribution discipline.
- The [`YouMind-OpenLab`](https://github.com/YouMind-OpenLab) family — multilingual scale and
  recommendation skills.
- [`alexewerlof`](https://gist.github.com/alexewerlof/1d13401a7647339469141dc2960e66a9) — the
  typed JSON-schema idea for image prompts.

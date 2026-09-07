# Repository Comparison

> Research date: 2026-09-07. Stars/forks are point-in-time snapshots and will drift.
> This document is the evidence base for MuseForge's knowledge model. Every claim about a
> repository is sourced from its public README, file tree, license file, or topic metadata.

## How to read this document

Each repository is assessed against the same four questions:

1. **What is genuinely good about this repository?**
2. **What should MuseForge inherit?**
3. **What should MuseForge improve?**
4. **What should MuseForge avoid?**

The goal is not to rank repositories. The goal is to extract the *design decisions* that make
some repositories more useful than others, and to identify the gaps that MuseForge exists to fill.

---

## 1. jamez-bondos/awesome-gpt4o-images

| Field | Value |
|---|---|
| URL | https://github.com/jamez-bondos/awesome-gpt4o-images |
| Stars | ~8.1k |
| Forks | ~1.8k |
| Last update | Active (129 commits) |
| License | CC BY 4.0 |
| Positioning | Curated collection of GPT-4o + gpt-image-1 images and prompts |
| Approx. prompt count | ~100+ cases (41 indexed by third-party crawlers, more in `cases/`) |
| Supported models | GPT-4o, gpt-image-1 |
| Image examples | Yes (inline in README + case folders) |
| Prompt format | Markdown case entries; some cases carry structured JSON fragments (e.g. `post_processing: { chromatic_aberration, glow, high_contrast, sharp_details }`) |
| Structured data | Partial — JSON fragments inside prose, not a uniform schema |
| Metadata design | Title, author handle, source link, model, prompt text, example image |
| Categories | Case-numbered flat list (案例 48, 案例 80 …) |
| Tags | GitHub topics only (ai-art, ghibli-style, gpt-4o, …) |
| Model metadata | Implicit (per-case model label) |
| Author attribution | Yes — Twitter/X handle per case |
| Source attribution | Yes — link to original post |
| Searchability | Weak — flat numbered list, no search UI |
| Prompt readability | Good — bilingual (zh/en), prose prompts |
| Multilingual | Yes (zh + en) |
| Contribution model | PR-based, `case-template/` + `CONTRIBUTING.md` |
| Update mechanism | Manual PRs |
| Duplicate level | Low (curated) |
| Content quality | High — hand-picked viral/representative cases |

### What is genuinely good about this repository?

It is the canonical "awesome list" for GPT-4o image generation. It proved that a *curated,
attributed, bilingual* collection of real cases is far more valuable than a raw dump. Its
`case-template/` folder is a real contribution contract — new cases must follow a shape. It
also demonstrates that a single case can carry a *structured JSON fragment* (post-processing,
color, texture) alongside prose, which is a seed of the "structured prompt" idea.

### What should MuseForge inherit?

- Per-case **author + source attribution** as a non-negotiable field.
- A **case template** that enforces a minimum shape for contributions.
- **Bilingual** presentation of prompts (the audience is global, and Chinese-language image
  prompts are a distinct, high-value genre).

### What should MuseForge improve?

- Replace the flat numbered list with **typed, queryable knowledge** (case vs. recipe vs.
  pattern vs. style vs. technique).
- Make the JSON fragments a **first-class schema** instead of prose-embedded fragments.
- Add **deduplication** — the same visual idea recurs across many cases.

### What should MuseForge avoid?

- The "numbered list of cases" as the *only* organization. It does not scale and does not
  teach the user *why* a case works.

---

## 2. YouMind-OpenLab/awesome-nano-banana-pro-prompts

| Field | Value |
|---|---|
| URL | https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts |
| Stars | ~13.2k |
| Forks | ~1.4k |
| Last update | Active (daily via GitHub Actions) |
| License | MIT |
| Positioning | "World's largest Nano Banana Pro prompt library — 10,000+ curated prompts, 16 languages" |
| Approx. prompt count | 10,000+ |
| Supported models | Nano Banana Pro (Gemini), Nano Banana 2 |
| Image examples | Yes (preview images) |
| Prompt format | Structured entries with preview images |
| Structured data | Yes — backed by PayloadCMS (`scripts/`, `docs/`, `public/images/`) |
| Metadata design | Category, use case, language, preview image |
| Categories | Social Media Post, Product Marketing, Profile/Avatar, Poster/Flyer, Infographic, E-commerce, Game Asset, Comic/Storyboard, YouTube Thumbnail, App/Web Design, Others |
| Tags | GitHub topics |
| Model metadata | Model family in title/topics |
| Author attribution | Community-sourced (aggregated) |
| Source attribution | Weak — aggregated, not per-prompt |
| Searchability | Strong — has a companion skill + gallery site |
| Prompt readability | Good |
| Multilingual | Yes — 16 languages |
| Contribution model | GitHub Actions sync from community |
| Update mechanism | Automated, twice-daily |
| Duplicate level | High (10k+ prompts inevitably overlap) |
| Content quality | Variable — quantity over curation |

### What is genuinely good about this repository?

It is the *scale* reference. It proves the demand for a large, multilingual, model-specific
prompt library, and it ships real infrastructure: a CMS backend, a gallery site, a
recommendation **skill** for Claude Code/OpenClaw, and automated daily ingestion. Its category
taxonomy (Social Media Post, Product Marketing, Infographic, Comic/Storyboard, …) is a useful
starting vocabulary for *use-case* classification.

### What should MuseForge inherit?

- The **use-case-first category taxonomy** (what is the image *for*?).
- The idea of a **companion agent skill** that recommends from the library.
- **Multilingual** as a first-class property.

### What should MuseForge improve?

- 10,000 prompts is a *collection*, not *knowledge*. MuseForge must distill the same territory
  into a few hundred **recipes/patterns/techniques** that are reusable.
- Add **per-prompt attribution** (the aggregation loses provenance).
- Add **deduplication** at the visual-intent level.

### What should MuseForge avoid?

- Quantity as the headline metric. "10,000+ prompts" is a marketing number, not a quality
  signal. MuseForge's value is "knows how to design an image", not "has the most prompts".

---

## 3. YouMind-OpenLab/awesome-gpt-image-2

| Field | Value |
|---|---|
| URL | https://github.com/YouMind-OpenLab/awesome-gpt-image-2 |
| Stars | ~9.4k |
| Forks | ~855 |
| Last update | Active (daily) |
| License | MIT |
| Positioning | "World's largest GPT Image 2 prompt library — 2000+ curated prompts, 16 languages" |
| Approx. prompt count | 2,000+ |
| Supported models | GPT Image 2 |
| Image examples | Yes |
| Prompt format | Structured entries with preview images |
| Structured data | Yes (same YouMind CMS infra) |
| Metadata design | Category, use case, language, preview |
| Categories | Similar taxonomy to the Nano Banana Pro repo |
| Tags | GitHub topics |
| Model metadata | Model family |
| Author attribution | Aggregated |
| Source attribution | Weak |
| Searchability | Strong (gallery + skill) |
| Prompt readability | Good |
| Multilingual | Yes — 16 languages |
| Contribution model | Automated sync |
| Update mechanism | Daily |
| Duplicate level | Moderate |
| Content quality | Variable |

### What is genuinely good about this repository?

Same infrastructure as #2, applied to GPT Image 2. It demonstrates that the *same* knowledge
pipeline can serve multiple models — which is exactly the model-agnostic posture MuseForge
wants. Its emphasis on "pixel-perfect text rendering" and "cross-image consistency" names two
capabilities that are actually *techniques*, not just model features.

### What should MuseForge inherit?

- **Model-agnostic knowledge** with model-specific *notes* layered on top.
- The recognition that "text rendering" and "consistency" are teachable techniques.

### What should MuseForge improve?

- Separate **model capability** from **prompt technique** (a model can render text well, but
  the *technique* is how you ask it to).
- Same dedup + attribution gaps as #2.

### What should MuseForge avoid?

- Duplicating the same prompt across model-specific repos (the YouMind family already shows
  this duplication risk).

---

## 4. freestylefly/awesome-gpt-image-2  (the "Prompt as Code" repo)

| Field | Value |
|---|---|
| URL | https://github.com/freestylefly/awesome-gpt-image-2 |
| Stars | ~1k (growing) |
| Forks | — |
| Last update | Active |
| License | MIT |
| Positioning | "Prompt as Code — GPT-Image2 industrial prompt engine & template library, 530+ reverse-engineered cases, 20+ industrial templates" |
| Approx. prompt count | 530+ cases (541 indexed) |
| Supported models | GPT Image 2 |
| Image examples | Yes (`data/images/caseNNN.jpg`) |
| Prompt format | Structured case objects: `id, title, category, styles[], scenes[], prompt, promptPreview, sourceLabel, sourceUrl, githubUrl, imageUrl, featured` |
| Structured data | **Yes — the strongest of any repo surveyed.** Atomic schema: subject / lighting / materials / layout / visual details split into composable parts |
| Metadata design | Category + styles[] + scenes[] + source author + source URL + image |
| Categories | 13: Architecture & Spaces, Brand & Logos, Characters & People, Charts & Infographics, Documents & Publishing, History & Classical Themes, Illustration & Art, Other Use Cases, Photography & Realism, Posters & Typography, Products & E-commerce, Scenes & Storytelling, UI & Interfaces |
| Tags | styles[] + scenes[] (two orthogonal tag axes) |
| Model metadata | GPT Image 2 |
| Author attribution | Yes — `sourceLabel` (X handle) + `sourceUrl` |
| Source attribution | Yes — per-case X/Twitter URL |
| Searchability | Strong — live gallery site (gpt-image2.canghe.ai) with filter by style/scenario |
| Prompt readability | High — prompts are long, structured, production-grade |
| Multilingual | Yes (en / zh / ja) |
| Contribution model | Reverse-engineering of community cases into templates |
| Update mechanism | Manual, ongoing |
| Duplicate level | Low (curated + reverse-engineered) |
| Content quality | **Highest of any repo surveyed** — each case is a full production prompt |

### What is genuinely good about this repository?

This is the closest existing project to MuseForge's philosophy. It explicitly rejects the
"prompt dump" model and instead **reverse-engineers** community cases into an **atomic,
composable schema** (subject, lighting, materials, layout, visual details). It ships **20+
industrial templates** (reusable structures, not one-off prompts) and a **skill** (a
"GPT-Image2 Style Library"). Its two-axis tagging (`styles[]` × `scenes[]`) is a clean,
orthogonal metadata design. Its case objects are fully structured and machine-readable.

### What should MuseForge inherit?

- **"Prompt as Code"** — prompts as structured, composable objects, not prose blobs.
- The **atomic schema** idea (split subject / lighting / materials / layout / details).
- **Two-axis tagging** (style × scene/use-case).
- **Reverse-engineering** as an ingestion strategy: turn observed cases into reusable
  templates.
- Full **per-case attribution** (`sourceLabel` + `sourceUrl`).

### What should MuseForge improve?

- freestylefly's "templates" are still *prompt-shaped*. MuseForge goes one level up: a
  **Recipe** (a method with steps, decision points, failure modes) and a **Visual Pattern**
  (a reusable visual structure) are more general than a template.
- Add **deduplication** and **knowledge linking** (which pattern does this case instantiate?).
- Add a **Creative Director** layer that *designs* before composing — freestylefly composes
  directly from a template.

### What should MuseForge avoid?

- Stopping at "template library". Templates are the *output*; MuseForge's value is the
  *reasoning* that selects and adapts them.

---

## 5. EvoLinkAI/awesome-gpt-image-2-API-and-Prompts

| Field | Value |
|---|---|
| URL | https://github.com/EvoLinkAI/awesome-gpt-image-2-API-and-Prompts |
| Stars | ~17.1k |
| Forks | ~1.7k |
| Last update | Active |
| License | CC0-1.0 |
| Positioning | "GPT-Image-2 API and Prompts" |
| Approx. prompt count | Large (cases/ + data/ + images/) |
| Supported models | GPT Image 2 |
| Image examples | Yes |
| Prompt format | Markdown + structured data files |
| Structured data | Yes — `cases/`, `data/`, `docs/`, `images/`, `script/`, `scripts/` |
| Metadata design | Case + data separation |
| Categories | Multiple |
| Tags | GitHub topics |
| Model metadata | GPT Image 2 |
| Author attribution | Partial |
| Source attribution | Partial |
| Searchability | Moderate |
| Prompt readability | Good |
| Multilingual | Yes (many README translations) |
| Contribution model | PR-based (CONTRIBUTING + CODE_OF_CONDUCT + SECURITY) |
| Update mechanism | Manual |
| Duplicate level | Moderate |
| Content quality | Good |

### What is genuinely good about this repository?

It is the highest-starred GPT Image 2 prompt repo, and it has the most *complete* engineering
hygiene: `cases/` (content) separated from `data/` (structured), plus `script/` and `scripts/`
for tooling, plus CODE_OF_CONDUCT, CONTRIBUTING, and SECURITY files. Its **CC0-1.0** license is
the most permissive of any repo surveyed — content can be freely reused.

### What should MuseForge inherit?

- **Content/data/tooling separation** in the repo layout.
- The **CC0/CC-BY licensing posture** — make reuse easy and explicit.

### What should MuseForge improve?

- Its structure is still case-centric; MuseForge adds the recipe/pattern/style/technique
  abstraction layer above cases.

### What should MuseForge avoid?

- A `tmp/` folder in the repo (observed in its tree) — a sign of un-curated ingestion.

---

## 6. wuyoscar/GPT-Image2-Skill

| Field | Value |
|---|---|
| URL | https://github.com/wuyoscar/GPT-Image2-Skill |
| Stars | ~4.9k |
| Forks | — |
| Last update | Active |
| License | (see repo) |
| Positioning | "GPT Image 2 prompt gallery, image prompt library, agentic skill, and CLI" |
| Approx. prompt count | Large gallery |
| Supported models | GPT Image 2 |
| Image examples | Yes |
| Prompt format | Structured prompts (some JSON-style) |
| Structured data | Yes |
| Metadata design | Category + prompt + example |
| Categories | Portraits, posters, UI mockups, game screenshots, character sheets, product ads |
| Tags | GitHub topics |
| Model metadata | GPT Image 2 |
| Author attribution | Partial |
| Source attribution | Partial |
| Searchability | Strong (CLI + skill) |
| Prompt readability | High — includes JSON-style structured prompts |
| Multilingual | Partial |
| Contribution model | — |
| Update mechanism | Active |
| Duplicate level | Moderate |
| Content quality | High |

### What is genuinely good about this repository?

It is the **Python + CLI + agent-skill** reference. It shows that a prompt library is most
useful when it is *callable* — a CLI and a skill, not just a README. Its prompts include
**JSON-style structured prompts** (e.g. a 3D product box from a dieline, a wallet UI), which
is direct evidence that structured prompting is a real, practiced technique.

### What should MuseForge inherit?

- **CLI + skill as first-class delivery surfaces** (not just a README).
- **JSON-style structured prompts** as a supported output format.

### What should MuseForge improve?

- wuyoscar's skill is model-specific (GPT Image 2). MuseForge is model-agnostic with a
  model-optimizer layer.

### What should MuseForge avoid?

- Coupling the knowledge layer to a single model's API.

---

## 7. ZeroLu/awesome-nanobanana-pro

| Field | Value |
|---|---|
| URL | https://github.com/ZeroLu/awesome-nanobanana-pro |
| Stars | ~1k |
| Forks | — |
| Last update | Active (69 commits) |
| License | CC BY 4.0 |
| Positioning | "Curated collection of the best Nano Banana prompts, styles, and resources" |
| Approx. prompt count | Dozens of curated cases |
| Supported models | Nano Banana Pro |
| Image examples | Yes |
| Prompt format | Markdown with **templated prompts** (e.g. `Product: [BRAND] [PRODUCT NAME] - [bottle shape] …`) |
| Structured data | Partial — templates with `[VARIABLE]` placeholders |
| Metadata design | Title, source author, source link, prompt |
| Categories | Product shots, creative experiments, portraits, stylized aesthetics |
| Tags | GitHub topics |
| Model metadata | Nano Banana Pro |
| Author attribution | Yes — per-case author handle |
| Source attribution | Yes — X/WeChat/Replicate links |
| Searchability | Weak |
| Prompt readability | High — templates are explicit |
| Multilingual | Partial |
| Contribution model | — |
| Update mechanism | Manual |
| Duplicate level | Low |
| Content quality | High — curated, high-fidelity |

### What is genuinely good about this repository?

It demonstrates **templated prompts with `[VARIABLE]` placeholders** — a prompt that is
*parameterized* rather than fixed. This is a direct ancestor of MuseForge's "Prompt DNA" and
"variables" concepts. Its sourcing (X, WeChat, Replicate, top prompt engineers) is explicit.

### What should MuseForge inherit?

- **Templated prompts with named variables** as a first-class concept.
- Explicit **multi-platform sourcing** (X / WeChat / Replicate).

### What should MuseForge improve?

- Templates are still prompt-shaped; MuseForge generalizes them into recipes + DNA with
  variables.

### What should MuseForge avoid?

- Hard-coding a single model's quirks into the knowledge.

---

## 8. PicoTrex/Awesome-Nano-Banana-images

| Field | Value |
|---|---|
| URL | https://github.com/PicoTrex/Awesome-Nano-Banana-images |
| Stars | ~1k |
| Forks | — |
| Last update | Active |
| License | (see repo) |
| Positioning | "Curated collection of images and prompts for Nano Banana" |
| Approx. prompt count | ~90+ cases |
| Supported models | Nano Banana |
| Image examples | Yes |
| Prompt format | Markdown cases (input image + prompt + output) |
| Structured data | Partial |
| Metadata design | Case title, author, input/output, prompt |
| Categories | Illustration-to-figure, character pose, line-drawing, film-noir story, etc. |
| Tags | GitHub topics |
| Model metadata | Nano Banana |
| Author attribution | Yes — per-case author |
| Source attribution | Yes |
| Searchability | Weak |
| Prompt readability | Good |
| Multilingual | Partial (en) |
| Contribution model | Community |
| Update mechanism | Manual |
| Duplicate level | Low |
| Content quality | Good — emphasizes **image-editing** workflows (input → output) |

### What is genuinely good about this repository?

It documents **image-editing / image-to-image** workflows (illustration→figure, pose change,
line-drawing→render, multi-image story), not just text-to-image. This is a distinct and
under-served knowledge area: *reference-image* and *editing* recipes.

### What should MuseForge inherit?

- **Image-editing / reference-image recipes** as a first-class recipe category (not just
  text-to-image).

### What should MuseForge improve?

- Turn the observed editing workflows into reusable **recipes** with steps and failure modes.

### What should MuseForge avoid?

- Treating "input image + prompt" as unstructured prose; it should be a typed recipe.

---

## 9. muset-ai/awesome-nano-banana-pro

| Field | Value |
|---|---|
| URL | https://github.com/muset-ai/awesome-nano-banana-pro |
| Stars | ~1.1k |
| Forks | — |
| Last update | Active |
| License | (see repo) |
| Positioning | "Curated collection of images and prompts built with Nano Banana Pro (early access)" |
| Approx. prompt count | Dozens |
| Supported models | Nano Banana Pro |
| Image examples | Yes |
| Prompt format | Markdown cases |
| Structured data | Partial |
| Metadata design | Case + prompt + image |
| Categories | Consistency, editing, generation |
| Tags | GitHub topics |
| Model metadata | Nano Banana Pro |
| Author attribution | Partial |
| Source attribution | Partial |
| Searchability | Weak |
| Prompt readability | Good |
| Multilingual | Partial |
| Contribution model | — |
| Update mechanism | Manual |
| Duplicate level | Low |
| Content quality | Good — early-access focus on consistency/editing |

### What is genuinely good about this repository?

Early-access documentation of a model's *strengths* (consistency, editing) before the model is
widely available. It is a reminder that **model knowledge** is time-sensitive and should be
labeled with a confidence/source type.

### What should MuseForge inherit?

- The idea of **model knowledge with a source-type label** (early-access / community-derived /
  unverified).

### What should MuseForge improve?

- Make the "early access" status explicit and machine-readable (MuseForge's `source_type`).

### What should MuseForge avoid?

- Presenting early-access observations as stable facts.

---

## 10. YouMind-OpenLab/nano-banana-pro-prompts-recommend-skill

| Field | Value |
|---|---|
| URL | https://github.com/YouMind-OpenLab/nano-banana-pro-prompts-recommend-skill |
| Stars | ~1.8k |
| Forks | ~196 |
| Last update | Active |
| License | MIT |
| Positioning | "AI skill for OpenClaw & Claude Code — recommend from 10,000+ Nano Banana Pro prompts" |
| Approx. prompt count | 10,000+ (via parent library) |
| Supported models | Nano Banana Pro |
| Image examples | Yes |
| Prompt format | Structured (CMS-backed) |
| Structured data | Yes |
| Metadata design | Category + use case + sample image |
| Categories | Social Media Post (10k+), Product Marketing (3.6k+), Profile/Avatar (1k+), Poster/Flyer (470+), Infographic (450+), E-commerce (370+), Game Asset (370+), Comic/Storyboard (280+), YouTube Thumbnail (170+), App/Web Design (160+), Others (900+) |
| Tags | GitHub topics |
| Model metadata | Nano Banana Pro |
| Author attribution | Aggregated |
| Source attribution | Weak |
| Searchability | Strong (skill = smart search by use case, remix, sample images) |
| Prompt readability | Good |
| Multilingual | Yes |
| Contribution model | Automated |
| Update mechanism | Daily |
| Duplicate level | High |
| Content quality | Variable |

### What is genuinely good about this repository?

It is the **"recommendation skill"** reference — the closest existing thing to MuseForge's
Assistant. It turns a 10k-prompt library into a *callable* "smart search by use case, content
remix, sample images" skill. Its published category counts are a useful *demand* signal: social
media posts and product marketing dominate.

### What should MuseForge inherit?

- The **recommendation-skill** delivery model (search by use case → recommend → remix).
- The **category demand signal** (social media + product marketing are the biggest use cases).

### What should MuseForge improve?

- It *recommends prompts*; MuseForge *designs images* (Creative Director → Composer). The
  difference is the whole point of MuseForge.

### What should MuseForge avoid?

- "Recommend a prompt" as the terminal output. MuseForge's terminal output is a *designed
  visual direction + composed prompt*.

---

## 11. YouMind-OpenLab/awesome-seedream-4.5

| Field | Value |
|---|---|
| URL | https://github.com/YouMind-OpenLab/awesome-seedream-4.5 |
| Stars | ~57 |
| Forks | — |
| Last update | Active |
| License | (see repo) |
| Positioning | "100+ hand-picked Seedream 4.5 prompts with images, multilingual" |
| Approx. prompt count | 100+ |
| Supported models | Seedream 4.5 |
| Image examples | Yes |
| Prompt format | Structured entries |
| Structured data | Yes |
| Metadata design | Category + prompt + image |
| Categories | Similar YouMind taxonomy |
| Tags | GitHub topics |
| Model metadata | Seedream 4.5 |
| Author attribution | Aggregated |
| Source attribution | Weak |
| Searchability | Moderate |
| Prompt readability | Good |
| Multilingual | Yes |
| Contribution model | Automated |
| Update mechanism | Active |
| Duplicate level | Moderate |
| Content quality | Good |

### What is genuinely good about this repository?

Evidence that the **same knowledge pipeline** extends to a third model family (ByteDance
Seedream). It confirms the model-agnostic thesis: the *knowledge* (recipes, patterns,
techniques) transfers; only the *model notes* change.

### What should MuseForge inherit?

- **Model-agnostic core + thin model-notes layer** (Seedream, Nano Banana, GPT Image all
  share the same recipes/patterns).

### What should MuseForge improve?

- Stop duplicating the same prompt across model-specific repos; store it once, tag it with
  model notes.

### What should MuseForge avoid?

- A separate knowledge base per model.

---

## 12. VigoZhao/AI-Visual-Prompt-Cookbook

| Field | Value |
|---|---|
| URL | https://github.com/VigoZhao/AI-Visual-Prompt-Cookbook |
| Stars | ~1k |
| Forks | — |
| Last update | Active (daily) |
| License | (see repo) |
| Positioning | "118+ plug-and-play JSON style packs — copy one JSON, get a style" |
| Approx. prompt count | 118+ style packs |
| Supported models | Nano Banana Pro, GPT Image, Midjourney (LLM-based workflows) |
| Image examples | Yes |
| Prompt format | **`style.json`** — structured JSON with `prompt_template`, `environment_variables`, `examples[].values` |
| Structured data | **Yes — the strongest JSON-schema design of any repo surveyed** |
| Metadata design | Style name, variables, examples, recommended models |
| Categories | Styles (Mono Noir Type Portrait, etc.) |
| Tags | Style tags |
| Model metadata | Recommended models per style |
| Author attribution | Curated by @VigoCreativeAI |
| Source attribution | Partial |
| Searchability | Strong (gallery + catalog) |
| Prompt readability | High — JSON is explicit and reusable |
| Multilingual | Yes (6 languages) |
| Contribution model | — |
| Update mechanism | Daily |
| Duplicate level | Low |
| Content quality | High — each style is a distilled, reusable system |

### What is genuinely good about this repository?

This is the **"style as a reusable JSON system"** reference. Each style is distilled into a
`style.json` with a `prompt_template`, declared `environment_variables`, and concrete
`examples[].values`. The tagline — "copy one JSON, get a style; replace the variables, keep
the visual system" — is *exactly* MuseForge's "Style" and "Prompt DNA" philosophy. It is the
strongest evidence that **styles should be structured, parameterized, and reusable**, not
prose.

### What should MuseForge inherit?

- **Style as a structured, parameterized object** with variables and examples.
- The "replace the variables, keep the visual system" framing.

### What should MuseForge improve?

- VigoZhao's styles are *style-only*. MuseForge adds **recipes** (method), **patterns**
  (visual structure), and **techniques** (prompt-engineering levers) as sibling abstractions,
  and a Creative Director that *selects* among them.

### What should MuseForge avoid?

- Style packs that are disconnected from *when to use them* (MuseForge links style → pattern
  → recipe → use case).

---

## 13. ImgEdify/Awesome-GPT4o-Image-Prompts

| Field | Value |
|---|---|
| URL | https://github.com/ImgEdify/Awesome-GPT4o-Image-Prompts |
| Stars | ~1k |
| Forks | — |
| Last update | Active |
| License | (see repo) |
| Positioning | "GPT4o Prompts Dictionary — curated collection of AI image generation prompts" |
| Approx. prompt count | Dozens (PDF + HTML) |
| Supported models | GPT-4o |
| Image examples | Yes |
| Prompt format | Markdown + PDF + HTML |
| Structured data | Weak — prose + PDF |
| Metadata design | Title, author, model, prompt text, example image |
| Categories | Flat list |
| Tags | GitHub topics |
| Model metadata | gpt4o label per prompt |
| Author attribution | Yes — per-prompt author (e.g. 宝玉, 藏师傅) |
| Source attribution | Partial |
| Searchability | Weak (PDF/HTML) |
| Prompt readability | Good — bilingual |
| Multilingual | Yes (en + zh-CN) |
| Contribution model | — |
| Update mechanism | Manual |
| Duplicate level | Low |
| Content quality | Good — representative Chinese-language prompts |

### What is genuinely good about this repository?

It is a clean, attributed, bilingual "dictionary" of GPT-4o prompts, and it is a good source
of **Chinese-language** prompt exemplars (VOGUE cover, micro-world café, etc.). It shows that
Chinese image prompts have their own idiom and are worth preserving as a distinct genre.

### What should MuseForge inherit?

- **Chinese-language prompt exemplars** as a distinct, valuable genre.
- Per-prompt **author attribution**.

### What should MuseForge improve?

- PDF/HTML is not queryable. MuseForge stores everything as structured JSON.

### What should MuseForge avoid?

- Distributing prompts as PDF/HTML (un-queryable, un-diffable).

---

## 14. ChaosRealmsAI/gpt-image-2-gallery

| Field | Value |
|---|---|
| URL | https://github.com/ChaosRealmsAI/gpt-image-2-gallery |
| Stars | ~27 |
| Forks | — |
| Last update | Active |
| License | MIT + CC BY 4.0 |
| Positioning | "AI image inspiration atlas — 3,800+ GPT-Image-2 works across 445 themes" |
| Approx. prompt count | 3,800+ |
| Supported models | GPT Image 2 |
| Image examples | Yes |
| Prompt format | Structured gallery |
| Structured data | Yes |
| Metadata design | Theme + prompt + image |
| Categories | 445 themes |
| Tags | Theme tags |
| Model metadata | GPT Image 2 |
| Author attribution | Partial |
| Source attribution | Partial |
| Searchability | Strong (gallery) |
| Prompt readability | Good |
| Multilingual | Partial |
| Contribution model | — |
| Update mechanism | Active |
| Duplicate level | High (3,800 works) |
| Content quality | Variable |

### What is genuinely good about this repository?

It demonstrates the **"theme"** as an organizing unit (445 themes) — a finer-grained axis than
"category". It also shows the *long tail* problem: 3,800 works is a lot of near-duplicate
visual intent.

### What should MuseForge inherit?

- The **theme** concept as a fine-grained tag axis (MuseForge's `tags` + `use_case`).

### What should MuseForge improve?

- 3,800 works → a few hundred **patterns/recipes** via visual-intent deduplication.

### What should MuseForge avoid?

- The long tail of near-duplicate cases as "knowledge".

---

## 15. gpt-img-2/ai-image-prompt-cookbook  (Chinese cookbook)

| Field | Value |
|---|---|
| URL | https://github.com/gpt-img-2/ai-image-prompt-cookbook |
| Stars | small |
| Forks | — |
| Last update | Active |
| License | (see repo) |
| Positioning | "中文 AI 图片提示词库 — 女装、童装、电商主图、产品摄影、小红书封面、广告海报" |
| Approx. prompt count | Dozens |
| Supported models | GPT Image 2 |
| Image examples | Yes |
| Prompt format | Markdown cookbook |
| Structured data | Weak |
| Metadata design | Category + prompt |
| Categories | 女装 (women's fashion), 童装 (children's), 电商主图 (e-commerce hero), 产品摄影 (product photography), 小红书封面 (Xiaohongshu cover), 广告海报 (ad poster) |
| Tags | — |
| Model metadata | GPT Image 2 |
| Author attribution | Partial |
| Source attribution | Partial |
| Searchability | Weak |
| Prompt readability | Good — Chinese |
| Multilingual | Chinese |
| Contribution model | — |
| Update mechanism | Active |
| Duplicate level | Low |
| Content quality | Good — domain-specific (e-commerce, Xiaohongshu) |

### What is genuinely good about this repository?

It is a **domain-specific Chinese cookbook** — it names concrete Chinese e-commerce and social
commerce use cases (电商主图, 小红书封面, 广告海报) that are under-represented in English
repos. This is direct evidence for MuseForge's Xiaohongshu / Chinese-editorial recipes.

### What should MuseForge inherit?

- **Chinese e-commerce / Xiaohongshu / ad-poster recipes** as first-class knowledge.

### What should MuseForge improve?

- Turn the cookbook prose into structured recipes with steps and failure modes.

### What should MuseForge avoid?

- English-only knowledge; the Chinese social-commerce genre is a core MuseForge strength.

---

## 16. mythkiven/rednote-director-skill  (Xiaohongshu agent skill)

| Field | Value |
|---|---|
| URL | https://github.com/mythkiven/rednote-director-skill |
| Stars | small |
| Forks | — |
| Last update | Active |
| License | (see repo) |
| Positioning | "面向小红书/RedNote 创作者的 Agent Skill：图文轮播规划、视觉导演、封面内页设计、AI 生图提示词与发布文案" |
| Approx. prompt count | Skill (not a prompt list) |
| Supported models | GPT Image 2 (via skill) |
| Image examples | Yes |
| Prompt format | Agent skill (SKILL.md) |
| Structured data | Skill instructions |
| Metadata design | — |
| Categories | 图文轮播 (carousel), 封面 (cover), 内页 (inner pages), 发布文案 (captions) |
| Tags | — |
| Model metadata | GPT Image 2 |
| Author attribution | — |
| Source attribution | — |
| Searchability | N/A (skill) |
| Prompt readability | High — it is a *director* workflow |
| Multilingual | Chinese |
| Contribution model | — |
| Update mechanism | Active |
| Duplicate level | N/A |
| Content quality | High — it is a *creative direction* workflow, not a prompt list |

### What is genuinely good about this repository?

This is the **"visual director"** reference — the closest existing thing to MuseForge's
Creative Director. It plans a Xiaohongshu carousel (cover + inner pages + captions) as a
*directorial* workflow, then generates prompts. It proves the demand for a *director* layer
above prompt generation.

### What should MuseForge inherit?

- The **Creative Director** concept as a distinct layer (plan → design → compose).
- **Platform-aware** direction (Xiaohongshu cover vs. inner page vs. caption).

### What should MuseForge improve?

- mythkiven's skill is platform-specific (Xiaohongshu) and model-specific (GPT Image 2).
  MuseForge generalizes the *director* layer to be platform- and model-agnostic.

### What should MuseForge avoid?

- A director layer that is hard-wired to one platform.

---

## 17. Structured JSON-schema references (gists / small repos)

Two small but important references define **structured JSON prompting** as a technique:

- **alexewerlof — "Nano Banana (Gemini 3 Pro) Ultimate Image Schema"** (gist): a JSON Schema
  with `meta` (aspect_ratio, guidance_scale 1–20), `subject[]` (typed: person/animal/robot/
  object…), `scene`, `user_intent`. It is the clearest public example of a *typed, validated*
  image-prompt schema.
- **xcaeser/image-json-gen**: a TypeScript `ImageGenerationPrompt` interface + published JSON
  schema + SuperJSON serialization, producing a reproducible `prompt.json`.

### What should MuseForge inherit?

- **Typed, validated prompt schemas** (JSON Schema + code models) as a first-class concept.
- The `guidance_scale` / `aspect_ratio` / typed-subject vocabulary.

### What should MuseForge improve?

- These are *prompt schemas*, not *knowledge schemas*. MuseForge's schemas describe
  **knowledge** (case/recipe/pattern/style/technique/DNA), and the prompt is the *output*.

### What should MuseForge avoid?

- Confusing "a schema for a prompt" with "a schema for knowledge about prompts".

---

## Cross-repository synthesis

### The spectrum

```
Prompt dump ──────────────────────────────────────────────► Knowledge system
   │                                                            │
   YouMind (10k prompts)          freestylefly (Prompt as Code)  MuseForge
   ChaosRealms (3.8k works)       VigoZhao (style.json)         (recipes + patterns
   EvoLinkAI (cases)              wuyoscar (CLI + skill)          + director + composer)
```

### What the best repositories converge on

1. **Attribution is non-negotiable** (freestylefly, awesome-gpt4o-images, ZeroLu all do
   per-case author + source).
2. **Structured > prose** (freestylefly's atomic schema, VigoZhao's style.json, the JSON-schema
   gists).
3. **Reusable > one-off** (freestylefly's templates, VigoZhao's style packs, ZeroLu's
   `[VARIABLE]` templates).
4. **Callable > readable** (wuyoscar's CLI, YouMind's skills, mythkiven's director skill).
5. **Model-agnostic knowledge with model notes** (YouMind's multi-model family).

### What no repository does (MuseForge's gap)

1. **No repository has a Creative Director layer** that *designs* the image before composing
   the prompt. (mythkiven comes closest, but is platform-locked.)
2. **No repository has a Recipe abstraction** — a method with steps, decision points, and
   failure modes. (freestylefly's "templates" are the closest, but are prompt-shaped.)
3. **No repository does visual-intent deduplication** — they all accumulate near-duplicate
   cases.
4. **No repository links knowledge** — case → pattern → style → technique → recipe → DNA.
5. **No repository separates model capability from prompt technique** — they conflate "the
   model renders text well" with "how to ask for text".

### Licensing summary

| Repo | License | Redistribution |
|---|---|---|
| awesome-gpt4o-images | CC BY 4.0 | Yes, with attribution |
| awesome-nano-banana-pro-prompts | MIT | Yes |
| awesome-gpt-image-2 (YouMind) | MIT | Yes |
| freestylefly/awesome-gpt-image-2 | MIT | Yes |
| EvoLinkAI/awesome-gpt-image-2-API-and-Prompts | CC0-1.0 | Yes, unrestricted |
| ZeroLu/awesome-nanobanana-pro | CC BY 4.0 | Yes, with attribution |
| nano-banana-pro-prompts-recommend-skill | MIT | Yes |
| ChaosRealmsAI/gpt-image-2-gallery | MIT + CC BY 4.0 | Yes, with attribution |

> MuseForge's policy (see `docs/licensing.md`): **never copy a prompt whose license is
> unclear.** For CC BY / MIT / CC0 content, copy with full attribution. For everything else,
> store only metadata + source URL + derived analysis (pattern/technique/knowledge), never the
> original prompt text.

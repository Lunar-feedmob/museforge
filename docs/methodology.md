# Methodology

> How MuseForge turns raw repositories into structured knowledge, and how it turns a user
> request into a production-ready prompt. This is the "why" behind the code.

## Part 1 — Knowledge acquisition

### 1. Repository discovery

Find high-quality image-generation prompt/example repositories. Selection criteria:

- Real, active, and non-trivial (not a single-file dump).
- Clear license (or explicitly flagged as unclear).
- Structured or semi-structured content (cases, JSON, templates).
- Representative of a model family (GPT Image, Nano Banana, Seedream) or a use-case genre
  (e-commerce, Xiaohongshu, editorial).

### 2. Collection

Fetch the repository's content (README, data files, case folders). V0 collects a **curated
subset**, not a full scrape — the goal is to validate the knowledge model, not to ingest
everything.

### 3. Parsing

Parse markdown/JSON/HTML into raw records. Each parser targets a specific repository's format
(e.g. freestylefly's case objects, VigoZhao's `style.json`).

### 4. Normalization

Strip markdown, URLs, author intros, invalid wrappers, and duplicate whitespace. Normalize
Unicode. This is the input to deduplication.

### 5. License / attribution check

For every prompt: identify the license, decide whether redistribution is allowed, and record
attribution requirements. **Unclear license → do not copy the prompt text** (store metadata +
source URL + derived analysis only).

### 6. Deduplication

Five levels (exact → normalized → near → semantic → visual-intent). The visual-intent level is
the most important: near-duplicate visual intents are aggregated into one Pattern/Recipe/Family,
keeping important variants.

### 7. Analysis

- **Case analysis** — decompose a case into subject/environment/composition/lighting/camera/
  style/color/typography.
- **Prompt analysis** — identify techniques used, why the prompt works, its visual pattern.

### 8. Extraction

Extract reusable abstractions from analyzed cases:

- **Recipe** — a method (steps, decision points, failure modes).
- **Visual Pattern** — a reusable visual structure.
- **Style** — a reusable visual system.
- **Technique** — a prompt-engineering lever.
- **Prompt DNA** — a composable prompt structure unit.

### 9. Knowledge linking

Link entities by explicit IDs: case → pattern/style/technique/recipe; recipe → recommended
pattern/style/technique; etc. This is what makes recommendations explainable.

### 10. Storage

Write to the Knowledge Store (JSON/JSONL), validated against the schemas.

---

## Part 2 — Prompt generation

### 1. Understand the request

`IntentAnalyzer` infers: use_case, category, platform, aspect_ratio, priority, style,
visual_density, likely pattern. It works with a configured LLM, or falls back to deterministic
heuristics (keyword → category/style mapping).

### 2. Retrieve knowledge

Retrieve cases, recipes, patterns, styles, techniques, and DNA relevant to the intent. V0 uses
metadata search + BM25/fuzzy; the embedding layer is reserved behind an interface.

### 3. Design (Creative Director)

The Creative Director produces a `CreativeDirection`: concept, goal, recommended recipe/pattern/
style, visual hierarchy, composition, subject strategy, environment, perspective, lighting,
color palette, typography, supporting elements, negative space, visual density, constraints,
avoid, rationale.

**The director designs the image first.** The composer only translates the design into a prompt.

### 4. Compose (Prompt Composer)

The Prompt Composer turns the CreativeDirection (+ recipe + pattern + style + techniques + DNA
+ constraints) into a **Universal Super Prompt**. The prompt structure is **task-dependent**:

- Poster → Canvas/Format, Visual Goal, Layout, Headline, Supporting Text, Illustration, Style,
  Color, Typography, Details, Constraints.
- Photography → Subject, Environment, Composition, Camera, Lens, Lighting, Color, Texture,
  Mood, Constraints.

The composer avoids low-information adjectives (`amazing`, `stunning`, `masterpiece`) and
redundancy.

### 5. Optimize (Model Optimizer)

Produce a model-specific variant. Every optimization carries an `optimization_basis` label
(`repository-derived` / `community-derived` / `heuristic`) — never a fabricated authority.

### 6. Respond

The Assistant returns a structured answer: Intent, Creative Direction, Recommended Recipe,
Recommended Pattern, Style, Composition, Key Techniques, Super Prompt, Model-specific Variant,
Alternative Direction, Notes. If the user asks for "prompt only", return only the prompt.

---

## Part 3 — Quality principles

1. **Knowledge > Collection** — store abstractions, not raw dumps.
2. **Attribution > Copying** — provenance is a schema field, not an afterthought.
3. **Explainability** — every recommendation carries a rationale (which case/pattern/recipe
   justifies it).
4. **No fabricated authority** — model claims carry a `source_type` label.
5. **Offline-first** — the core path works with no API key (heuristic fallback).

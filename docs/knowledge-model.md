# Knowledge Model

> The core design of MuseForge. This document defines the knowledge entities, their
> relationships, and the reasoning that turns them into a production-ready prompt.

## The central thesis

```
Knowledge > Collection
Patterns > Prompt Dumps
Recipes > Random Examples
Quality > Quantity
Reusable Systems > Viral Prompts
Creative Direction > Prompt Expansion
Attribution > Copying
```

A prompt is the *output*. Knowledge is the *input*. MuseForge stores knowledge, not prompts.

---

## The knowledge entities

MuseForge has **nine** first-class knowledge entities, arranged in three layers:

```
Layer 1 — Raw evidence
    Source        (where knowledge came from)
    Prompt        (a single, attributed prompt)
    Case          (a complete, analyzed example)

Layer 2 — Reusable abstractions
    Recipe        (a method for a class of image task)
    Visual Pattern (a reusable visual structure)
    Style         (a reusable visual system)
    Technique     (a prompt-engineering lever)
    Prompt DNA    (a composable prompt structure unit)

Layer 3 — Model knowledge
    Model         (what a model can do, with a source_type label)
```

Plus one **output** entity:

```
CreativeDirection  (the designed plan, produced by the Creative Director)
```

---

## Entity definitions

### Source

A repository or origin that knowledge was derived from.

```yaml
id, name, url, kind (github|web|community|official),
license, allowed_usage, redistribution_status, attribution_requirements,
description, last_checked, notes
```

### Prompt

A single, attributed prompt. The *only* entity that may carry verbatim third-party text, and
only when the license permits redistribution.

```yaml
id, title, original_prompt, source_repo, source_url, author, license,
target_model, category, tags, why_it_is_good, techniques_used,
visual_pattern, style, prompt_dna, tier (original|annotated|refined|enhanced)
```

### Case

A complete, analyzed example. A Case is *more* than a Prompt: it carries the full visual
analysis (subject, environment, composition, lighting, camera, style, …) and links to the
abstractions it instantiates.

```yaml
id, title, category, use_case, user_intent, input_type,
reference_requirements, source, model, original_prompt,
visual_intent, subject, environment, composition, lighting, camera, lens,
perspective, style, color, materials, typography, layout,
supporting_elements, techniques, constraints, negative_constraints,
tags, pattern_ids, style_ids, technique_ids, recipe_ids
```

### Recipe

A **method** for completing a class of image task. The most valuable entity — it is *how* to
produce a class of image, not a single prompt.

```yaml
id, name, category, goal, description,
required_inputs, optional_inputs, workflow, steps, decision_points,
recommended_patterns, recommended_styles, recommended_techniques,
prompt_structure, composition_guidance, text_guidance, constraints,
common_failures, failure_recovery, example_cases, source_repositories,
confidence, tags
```

### Visual Pattern

A **reusable visual structure** that works across products, brands, and subjects.

```yaml
id, name, aliases, category, description, visual_goal, best_for, not_good_for,
composition, visual_hierarchy, subject_placement,
foreground, midground, background, perspective,
lighting_strategy, color_strategy, typography_strategy, negative_space_strategy,
supporting_elements, prompt_structure, constraints, common_failures,
related_styles, related_techniques, related_recipes,
example_cases, source_repositories, confidence, tags
```

### Style

A **reusable visual system** (aesthetic), strictly separate from Category (what the image is
*for*).

```yaml
id, name, aliases, description,
visual_characteristics, composition_behavior, color_behavior, lighting_behavior,
typography_behavior, material_behavior, texture_behavior,
best_for, avoid, related_patterns, related_techniques,
example_cases, source_repositories, tags
```

### Technique

A **prompt-engineering lever** that affects output quality.

```yaml
id, name, category, description, problem_it_solves, pattern,
implementation_guidance, when_to_use, when_not_to_use,
good_examples, bad_examples, related_patterns, related_recipes, related_styles,
source_repositories, confidence, tags
```

### Prompt DNA

A **composable prompt structure unit** — the smallest reusable building block of a prompt.

```yaml
id, name, category, description, components, pattern, variables,
best_for, related_patterns, related_techniques, related_styles,
source_families, source_repositories, confidence, tags
```

### Model

What a model can do, **with a source_type label** (never an unverified claim).

```yaml
id, name, family, provider, capabilities, strengths, limitations,
text_rendering, consistency, editing, prompt_style_notes,
source_type (official|repository-derived|community-derived|inferred|experimental|unverified),
source_references, tags
```

### CreativeDirection (output)

The designed plan produced by the Creative Director.

```yaml
concept, goal, recommended_recipe, recommended_pattern, recommended_style,
visual_hierarchy, composition, subject_strategy, environment, perspective,
lighting, color_palette, typography, supporting_elements, negative_space,
visual_density, constraints, avoid, rationale
```

---

## Relationships (the knowledge graph)

```
Source ──derives──► Prompt ──analyzed into──► Case
                        │                        │
                        │                        ├──instantiates──► Visual Pattern
                        │                        ├──uses──────────► Style
                        │                        ├──applies───────► Technique
                        │                        └──follows───────► Recipe
                        │
                        └──composed from──► Prompt DNA

Recipe ──recommends──► Visual Pattern / Style / Technique
Visual Pattern ──related──► Style / Technique / Recipe
Style ──related──► Pattern / Technique
Technique ──related──► Pattern / Recipe / Style
Prompt DNA ──related──► Pattern / Technique / Style
```

The links are **explicit IDs** (`pattern_ids`, `style_ids`, …), not inferred similarity. This
is what makes MuseForge's recommendations *explainable*: the Assistant can always say *why* it
recommended a direction ("this case instantiates the Breakout Product Hero pattern, which the
Product Hero Ad recipe recommends").

---

## The four prompt tiers

Every redistributed prompt is stored at one of four tiers:

1. **Original** — verbatim, license-permitting, fully attributed.
2. **Annotated** — original + MuseForge's analysis (why it works, techniques used).
3. **Refined** — cleaned/normalized, still attributed to the source.
4. **MuseForge Enhanced** — a new prompt composed by MuseForge, *derived from* the source
   knowledge but not a copy.

If a license does not permit redistribution, MuseForge stores **only** metadata + source URL +
derived analysis (pattern/technique/knowledge), never the original text.

---

## Deduplication levels

1. **Exact** — identical text.
2. **Normalized** — identical after stripping markdown/URLs/wrappers/whitespace.
3. **Near** — Jaccard / token / n-gram / edit-distance similarity.
4. **Semantic** — embedding similarity (via a provider-agnostic `EmbeddingProvider`).
5. **Visual intent** — same subject/composition/lighting/style/camera/environment even if the
   text differs. This is the *most important* level: near-duplicate visual intents are
   aggregated into one Pattern/Recipe/Family, keeping important variants.

---

## Why this model is not a prompt dump

- A prompt dump stores **text**. MuseForge stores **typed knowledge with links**.
- A prompt dump answers "what prompt exists?". MuseForge answers "how should I design this
  image, and why?".
- A prompt dump scales by adding more prompts. MuseForge scales by adding more
  **abstractions** (a new recipe covers a thousand prompts).

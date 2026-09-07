# Recipes

A **Recipe** is a method for completing a class of image task. It is the most valuable entity
in MuseForge — more valuable than any single prompt, because a recipe covers a thousand
prompts.

## Why recipes matter

A prompt is a single answer. A recipe is the *method* that produces the answer. When a user
asks for "a fintech card ad", MuseForge doesn't just retrieve a prompt — it retrieves the
**Fintech Card Ad recipe** (steps, decision points, failure modes) and uses it to *design* the
image.

## Recipe schema

```yaml
id, name, category, goal, description,
required_inputs, optional_inputs, workflow, steps, decision_points,
recommended_patterns, recommended_styles, recommended_techniques,
prompt_structure, composition_guidance, text_guidance, constraints,
common_failures, failure_recovery, example_cases, source_repositories,
confidence, tags
```

## The seed recipes

| Recipe | Category | What it solves |
|---|---|---|
| Product Hero Ad | product advertisement | A premium product hero that preserves the product |
| Editorial Poster | poster | A text-first editorial poster with clear hierarchy |
| Xiaohongshu Information Card | social media poster | A platform-aware cover that prioritizes text readability |
| Character Consistency | character | Keep the same character across images |
| Reference Image Restyle | image editing | Restyle an input image while preserving its subject |
| Multi-panel Comic | comic | A multi-panel comic with consistent characters |
| Infographic | infographic | A clear, beautiful data visualization |
| Fintech Card Ad | product advertisement | A card ad with exact numbers and clean hierarchy |
| SaaS Landing Hero | product hero | A clean SaaS landing hero |
| App Screenshot Ad | product hero | An app screenshot advertisement |

## Example: Product Hero Ad

```
1. Identify the hero product and its critical geometry.
2. Preserve critical product geometry and branding.
3. Select a primary visual metaphor (breakout, floating, reflection).
4. Create strong foreground/background separation.
5. Choose commercial lighting (rim, golden hour, soft studio).
6. Add controlled supporting elements (particles, flowers, ripples).
7. Reserve negative space for the product and any text.
8. Protect branding (exact name, logo, colors).
9. Add text-rendering constraints if text is present.
10. Remove irrelevant decorative elements.
```

Each recipe also records **common failures** (e.g. "product distortion", "cluttered
background") and **failure recovery** (e.g. "re-state product geometry", "add negative
constraints"), so the Assistant can warn the user *before* they hit a known pitfall.

## How recipes are used

1. The Assistant matches the user's intent to a recipe.
2. The recipe's `recommended_patterns` / `recommended_styles` / `recommended_techniques`
   drive the Creative Director's selection.
3. The recipe's `steps` are shown to the user as the method.
4. The recipe's `common_failures` become the Assistant's "Notes".

The seed recipes are synthetic (authored for MuseForge), but each is grounded in workflows
observed across the surveyed repositories (see `docs/repository-comparison.md`).

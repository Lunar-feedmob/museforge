# Visual Patterns

A **Visual Pattern** is a reusable visual structure that works across products, brands, and
subjects. It is *not* a prompt — it is a repeatable visual solution.

## Why patterns matter

A prompt is one-off. A pattern transfers. "Breakout Product Hero" works for a skincare bottle,
a fintech card, or a SaaS device — the *structure* (hero object + forced perspective +
foreground overlap + particles + commercial lighting) is the same; only the subject changes.

## Pattern schema

```yaml
id, name, aliases, category, description, visual_goal, best_for, not_good_for,
composition, visual_hierarchy, subject_placement,
foreground, midground, background, perspective,
lighting_strategy, color_strategy, typography_strategy, negative_space_strategy,
supporting_elements, prompt_structure, constraints, common_failures,
related_styles, related_techniques, related_recipes,
example_cases, source_repositories, confidence, tags
```

## The seed patterns

| Pattern | Category | Visual structure |
|---|---|---|
| Breakout Product Hero | product advertisement | hero object + forced perspective + foreground overlap + particles |
| Editorial Text-first Poster | poster | headline-first + supporting text + illustration |
| Centered Luxury Product Shot | product advertisement | centered product + reflection + flowers + golden hour |
| Cinematic Character Portrait | photography | subject + 85mm + shallow DOF + editorial mood |
| Magazine Infographic | infographic | editorial layout + data + typography + whitespace |
| Multi-panel Comic | comic | grid + sequential panels + consistency |
| Minimal SaaS Illustration | product hero | flat vector + device + negative space + brand color |
| Hero Device Composition | product hero | device + product + environment, layered depth |
| Double-exposure Portrait | photography | subject + layered semi-transparent profile |
| Layered Depth Product Ad | product advertisement | foreground/midground/background separation |

## How patterns are used

1. The Assistant matches the user's intent to a recipe, then to a pattern (via the recipe's
   `recommended_patterns`).
2. The pattern's `composition`, `lighting_strategy`, `color_strategy`, etc. become the
   Creative Direction.
3. The pattern's `common_failures` become the Assistant's "Notes".

## Pattern vs. Recipe vs. Style

- **Recipe** = *how* to do a task (method, steps).
- **Pattern** = *what* the visual structure looks like (composition, hierarchy).
- **Style** = *what aesthetic* it uses (color, typography, texture).

A recipe recommends patterns; a pattern relates to styles and techniques. They are distinct
axes, not synonyms.

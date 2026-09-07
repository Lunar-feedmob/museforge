# Prompt DNA

**Prompt DNA** is a composable prompt structure unit — the smallest reusable building block of
a prompt. It is the "recipe for a single prompt", expressed as a list of components.

## Why DNA matters

A great prompt is not a blob — it is a *composition* of components. "Direct Flash Editorial
Portrait" is:

```
subject + direct flash + dark ambient environment + 35mm framing
+ natural skin texture + slightly candid composition + editorial mood
```

Each component is a variable. Swap the subject, keep the structure. This is what makes a
prompt *reusable* rather than *one-off*.

## DNA schema

```yaml
id, name, category, description, components, pattern, variables,
best_for, related_patterns, related_techniques, related_styles,
source_families, source_repositories, confidence, tags
```

## The seed DNA

| DNA | Components |
|---|---|
| Breakout Product Hero DNA | hero object + forced perspective + foreground overlap + particles + commercial lighting + negative space |
| Editorial Text-first Poster DNA | format + headline + supporting text + illustration + style + color + typography + negative space |
| Direct Flash Editorial Portrait DNA | subject + direct flash + dark ambient + 35mm + natural skin + candid + editorial mood |
| Luxury Product Shot DNA | product + dark water + flowers + golden hour + reflections + shallow DOF + commercial |
| Cinematic Portrait DNA | subject + 85mm + shallow DOF + key/rim light + warm grade + film grain + editorial mood |

## DNA vs. Pattern vs. Recipe

- **DNA** = the structure of a *single prompt* (components + variables).
- **Pattern** = the structure of a *visual composition* (hierarchy, placement, lighting).
- **Recipe** = the structure of a *method* (steps, decision points, failure modes).

DNA is the finest-grained abstraction; a pattern may be realized by one or more DNA, and a
recipe may recommend several patterns.

## How DNA is used

The Assistant retrieves DNA alongside patterns and techniques, and the composer can use a DNA's
`components` to structure the prompt. In V0, DNA is primarily a *knowledge* entity that
documents reusable prompt structure; the composer uses the Creative Direction (which already
encodes the pattern's structure) as its primary input.

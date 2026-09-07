# Prompt Techniques

A **Technique** is a prompt-engineering lever that actually affects output quality. It is the
smallest unit of "how to ask" that transfers across models and tasks.

## Why techniques matter

Techniques are what separate a good prompt from a vague one. "Put exact text in quotes and
specify font style" (text rendering) is a technique. "Preserve critical product geometry"
(product preservation) is a technique. MuseForge applies the right techniques to the right
task, instead of dumping adjectives.

## Technique schema

```yaml
id, name, category, description, problem_it_solves, pattern,
implementation_guidance, when_to_use, when_not_to_use,
good_examples, bad_examples, related_patterns, related_recipes, related_styles,
source_repositories, confidence, tags
```

## The seed techniques

| Technique | Category | Problem it solves |
|---|---|---|
| text rendering | Typography | Models garble or misspell text |
| product preservation | Product Preservation | Models distort the product |
| brand preservation | Brand Preservation | Models alter brand elements |
| reference image | Reference Image | Models can't match a specific face/object |
| character consistency | Character Consistency | Models change a character between images |
| negative constraints | Negative Constraints | Models add unwanted elements |
| camera & lens control | Camera | Models default to generic framing |
| lighting control | Lighting | Models default to flat lighting |
| color grading | Color Control | Models pick arbitrary colors |
| whitespace / negative space | Whitespace | Models fill every area with clutter |
| subject hierarchy | Composition | Models produce flat compositions |
| multi-panel grid | Layout | Models misalign panels |
| visual hierarchy | Visual Hierarchy | Models give equal weight to everything |
| templated variables | Prompt Structure | One-off prompts can't be reused |
| structured JSON prompting | Prompt Structure | Prose prompts are hard to reuse |

## The anti-pattern MuseForge avoids

MuseForge never emits low-information adjectives (`amazing`, `stunning`, `masterpiece`,
`beautiful`). These add no information and are the hallmark of a prompt dump. The composer
strips them and the `improve` command removes them.

## How techniques are used

1. The recipe's `recommended_techniques` and the pattern's `related_techniques` drive the
   selection.
2. The selected techniques are shown to the user as "Key Techniques".
3. The composer applies them to the prompt structure (e.g. text rendering → quote exact text).

# Demo: demo-4-cinematic-portrait

**User request:** Create a realistic cinematic character portrait.

---

Intent: photography / photography

## Creative Direction
Concept: A premium, editorial portrait.
Goal: Keep the same character across images or panels.
Rationale: the Character Consistency recipe matches the photography use case; the Cinematic Character Portrait pattern fits the visual goal; the cinematic realism style matches the requested aesthetic; 5 technique(s) apply to this task.

## Recommended Recipe: Character Consistency
1. Provide a reference image or a detailed character description.
2. Preserve the character's identity (face, hair, build).
3. Apply the new styling or scene.
4. Keep the character's geometry consistent.
5. Re-anchor with a consolidated prompt if drift occurs.

## Recommended Pattern: Cinematic Character Portrait
Subject + 85mm + shallow DOF + editorial mood.

## Style: cinematic realism

## Composition
subject-forward, rule of thirds

## Key Techniques
reference image, character consistency, camera & lens control, lighting control, color grading

## Super Prompt
Subject: off-center or centered, eye-level
Environment: minimal or environmental
Composition: subject-forward, rule of thirds
Perspective: eye-level, 85mm
Lighting: soft key + rim, high contrast
Color: warm desaturated or teal-orange grade
Style: cinematic realism
Mood: A premium, editorial portrait.
Constraints: preserve identity; natural skin texture
Avoid: flat lighting; over-saturation

## Model-specific Variant (gpt-image-2)
optimization_basis: repository-derived
Subject: off-center or centered, eye-level
Environment: minimal or environmental
Composition: subject-forward, rule of thirds
Perspective: eye-level, 85mm
Lighting: soft key + rim, high contrast
Color: warm desaturated or teal-orange grade
Style: cinematic realism
Mood: A premium, editorial portrait.
Constraints: preserve identity; natural skin texture
Avoid: flat lighting; over-saturation
Render all text exactly as written (pixel-perfect; quote exact text and specify type style).
Maintain consistency: strong cross-image consistency reported.
JSON-style structured prompts are a practiced technique.

## Alternative Direction
pattern: Double-exposure Portrait; style: editorial minimalism

## Notes
- Watch for: identity drift, plastic skin
- Pattern pitfalls: plastic skin, flat lighting

# Best-of Existing Repositories

> This document distills the *genuinely good assets* found across the surveyed repositories.
> It is the raw material for MuseForge's seed knowledge base. Everything here is either a
> public fact, a derived pattern/technique, or a design idea — never a verbatim copy of a
> prompt whose license is unclear.

---

## Best Prompts (representative, high-quality exemplars)

These are *categories* of prompt that recur across repos and are worth preserving as
exemplars. MuseForge stores the *structure* and *why it works*, not necessarily the verbatim
text (see `docs/licensing.md`).

1. **Double-exposure fashion portrait** (freestylefly case 490) — subject + reference face +
   layered semi-transparent profile + 85mm lens + warm desaturated grade. *Why good:* it
   combines a reference-image technique with a strong compositional device.
2. **Six-panel grid beverage campaign** (freestylefly case 532) — strict 2×3 grid, six aligned
   panels, brand name "LIMORA", Cannes-level premium. *Why good:* multi-panel layout with
   brand preservation.
3. **Travel-souvenir enamel pin** (freestylefly case 543) — "compose it as a SCENE, not a
   single isolated object", subject hierarchy. *Why good:* explicit subject-hierarchy
   instruction.
4. **Black-and-white typographic portrait poster** (freestylefly case 542) — silhouette blocks,
   negative space, stencil edges. *Why good:* typography-as-image technique.
5. **VOGUE cover — Ashe as fashion model** (ImgEdify) — real subject + fashion-editorial
   styling + simple background. *Why good:* character-restyle recipe.
6. **Micro-world café in a mug** (ImgEdify) — miniature scene + macro + shallow DOF. *Why good:*
   scale-contrast visual pattern.
7. **3D product box from dieline** (wuyoscar) — assemble dieline → 3D box, three-quarter angle,
   "AURAE / COLD-BREW MATCHA" text. *Why good:* product-preservation + text-rendering.
8. **Wallet UI mockup** (wuyoscar) — "crisp labels, exact numbers, clean hierarchy, believable
   wallet UX". *Why good:* UI-mockup recipe with text-rendering constraints.
9. **Song Dynasty social feed** (wuyoscar) — anachronistic UI (Song Dynasty WeChat). *Why good:*
   creative concept + UI-mockup technique.
10. **Luxury product on dark water** (ZeroLu) — `[BRAND] [PRODUCT NAME]` template, floating on
    water with flowers, golden-hour glow. *Why good:* templated product-hero recipe.

---

## Best Cases (complete, reusable scenarios)

1. **Product hero advertisement** — hero product + metaphor + foreground/background separation
   + commercial lighting + negative space.
2. **Editorial text-first poster** — headline-first layout + supporting text + illustration.
3. **Xiaohongshu information card** — cover + inner pages + caption, platform-aware.
4. **Character consistency / restyle** — reference face + new styling (VOGUE cover, avatar).
5. **Reference-image restyle** — illustration→figure, line-drawing→render, pose change.
6. **Multi-panel comic / storyboard** — 12-part film-noir story, no text, imagery only.
7. **Infographic / educational card** — vocabulary card, data visualization.
8. **Fintech card ad** — wallet UI, bank card, exact numbers, clean hierarchy.
9. **SaaS landing hero** — device composition, minimal illustration.
10. **App screenshot advertisement** — App Store screenshot, UI mockup.

---

## Best Recipes (methods, not prompts)

Distilled from observed workflows across repos:

1. **Product Hero Ad Recipe** — identify hero → preserve geometry → choose metaphor → separate
   foreground/background → commercial lighting → controlled supporting elements → reserve
   negative space → protect branding → text constraints → remove decoration.
2. **Editorial Poster Recipe** — canvas/format → visual goal → layout → headline → supporting
   text → illustration → style → color → typography → details → constraints.
3. **Xiaohongshu Information Card Recipe** — platform → aspect ratio → text-readability-first
   → editorial minimalism → low density → cover + inner pages.
4. **Character Consistency Recipe** — reference image → preserve identity → restyle → keep
   geometry → consistent across panels.
5. **Reference Image Restyle Recipe** — input image → identify subject → apply new style →
   preserve composition → output.
6. **Multi-panel Comic Recipe** — story → panel grid → character consistency → no-text
   storytelling → sequential art.
7. **Infographic Recipe** — data → hierarchy → chart type → typography → color → whitespace.
8. **Fintech Card Ad Recipe** — product → exact numbers → clean hierarchy → believable UX →
   brand → text rendering.
9. **SaaS Landing Hero Recipe** — product → device → minimal illustration → negative space →
   brand color.
10. **App Screenshot Ad Recipe** — app → screenshot → device frame → caption → platform
    constraints.

---

## Best Visual Patterns (reusable visual structures)

1. **Breakout Product Hero** — hero object + forced perspective + foreground overlap +
   frame/device breakout + particles + commercial lighting.
2. **Editorial Text-first Poster** — headline-first + supporting text + illustration.
3. **Floating 3D Product Scene** — product floating + soft shadows + minimal background.
4. **Centered Luxury Product Shot** — centered + dark water/reflection + flowers + golden hour.
5. **Cinematic Character Portrait** — subject + 85mm + shallow DOF + editorial mood.
6. **Split-screen Comparison** — before/after, two panels.
7. **Exploded View** — product disassembled into layers.
8. **Isometric System Diagram** — isometric + labeled parts.
9. **Magazine Infographic** — editorial layout + data + typography.
10. **Multi-panel Comic** — grid + sequential panels + consistency.
11. **Minimal SaaS Illustration** — flat vector + device + negative space.
12. **Hero Device Composition** — device + product + environment.
13. **Layered Depth Product Ad** — foreground/midground/background separation.
14. **Double-exposure Portrait** — subject + layered semi-transparent profile.
15. **Scale-contrast Miniature** — tiny scene in a real object (micro-world café).

---

## Best Prompt Techniques (prompt-engineering levers)

1. **Subject hierarchy** — "compose it as a SCENE, not a single isolated object" (freestylefly).
2. **Text rendering** — put exact text in quotes, specify font style, "pixel-perfect text".
3. **Product preservation** — "preserve critical product geometry", "assemble the dieline".
4. **Brand preservation** — "protect branding", exact brand name + logo.
5. **Reference image** — "use the uploaded face 100% as reference".
6. **Character consistency** — "these two characters", "same character across panels".
7. **Negative constraints** — "do not include any words or text", "no props".
8. **Camera/lens control** — "85mm lens", "shallow depth of field", "three-quarter angle".
9. **Lighting control** — "golden hour glow", "soft diffused", "commercial lighting".
10. **Color grading** — "warm desaturated sepia and charcoal palette".
11. **Whitespace / negative space** — "reserve negative space", "controlled negative space".
12. **Structured JSON prompting** — JSON schema with typed subject/scene/meta (alexewerlof).
13. **Templated variables** — `[BRAND] [PRODUCT NAME] [bottle shape]` (ZeroLu).
14. **Multi-panel grid** — "strict 2-column by 3-row grid" (freestylefly).
15. **Guidance scale** — 1–4 creative, 7–10 balanced, 15+ strict (alexewerlof).

---

## Best Styles (reusable visual systems)

1. **Editorial minimalism** — clean, text-first, generous whitespace.
2. **Premium SaaS** — flat vector + device + brand color.
3. **Luxury commercial** — dark, reflective, golden-hour, high-end.
4. **Japanese magazine editorial** — structured grid, refined typography.
5. **Retro print** — halftone, grain, vintage palette.
6. **Cinematic realism** — 85mm, shallow DOF, film grain, color grade.
7. **Flat vector** — minimal, geometric, brand-friendly.
8. **Soft editorial illustration** — gentle shapes, muted palette.
9. **New Yorker inspired** — line art + wash + editorial.
10. **Swiss editorial** — grid, sans-serif, high contrast.
11. **Modern Chinese editorial** — 中文 typography, red/ink accents.
12. **3D commercial** — product render, studio lighting.
13. **Documentary photography** — natural light, candid, real texture.
14. **Brutalist graphic design** — raw, high-contrast, oversized type.

---

## Best Metadata Ideas

1. **Two-axis tagging** — `styles[]` × `scenes[]` (freestylefly). Orthogonal, composable.
2. **Per-case source attribution** — `sourceLabel` + `sourceUrl` (freestylefly, awesome-gpt4o-images).
3. **Case template** — enforce a minimum shape for contributions (awesome-gpt4o-images).
4. **Model-agnostic + model notes** — store knowledge once, tag with model notes (YouMind family).
5. **`source_type` label** — official / repository-derived / community-derived / inferred /
   experimental / unverified (MuseForge's own addition, inspired by muset-ai's early-access).
6. **Category demand signal** — publish category counts (YouMind skill).
7. **Theme as fine-grained tag** — 445 themes (ChaosRealms).
8. **Variables + examples** — `environment_variables` + `examples[].values` (VigoZhao).

---

## Best Product Features

See `docs/feature-comparison.md` for the full feature matrix. Highlights:

1. **CLI + agent skill** (wuyoscar, YouMind) — callable, not just readable.
2. **Live gallery with filter** (freestylefly, YouMind) — browse by style/scenario.
3. **Recommendation skill** (YouMind) — search by use case → recommend → remix.
4. **Visual director workflow** (mythkiven) — plan cover + inner pages + captions.
5. **Automated daily ingestion** (YouMind, VigoZhao) — GitHub Actions sync.
6. **JSON style packs** (VigoZhao) — copy one JSON, get a style.

---

## Best UX Ideas

1. **"Copy one JSON, get a style"** (VigoZhao) — the value prop is *reuse*, not *reading*.
2. **"Prompt as Code"** (freestylefly) — prompts are composable, diffable, versionable.
3. **Input → output walkthrough** (VigoZhao, PicoTrex) — show the reference image, the prompt,
   and the result together.
4. **Bilingual presentation** (awesome-gpt4o-images, ImgEdify) — the audience is global.
5. **Category counts as a map** (YouMind) — "what's in here" at a glance.

---

## Best Contribution Ideas

1. **Case template** (awesome-gpt4o-images) — a `case-template/` folder + CONTRIBUTING.md.
2. **Reverse-engineering as contribution** (freestylefly) — turn observed cases into templates.
3. **Automated community sync** (YouMind) — GitHub Actions pulls from community sources.
4. **CODE_OF_CONDUCT + SECURITY + CONTRIBUTING** (EvoLinkAI) — full engineering hygiene.
5. **CC0/CC-BY licensing** (EvoLinkAI, awesome-gpt4o-images) — make reuse explicit and easy.

---

## What MuseForge will NOT copy

- **Verbatim prompt dumps** — MuseForge stores *knowledge*, not raw collections.
- **Un-attributed aggregation** — every redistributed prompt carries provenance.
- **Model-specific duplication** — one knowledge base, model notes layered on top.
- **"10,000+ prompts" as a headline** — MuseForge's headline is "knows how to design an image".

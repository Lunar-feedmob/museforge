# MuseForge

**Your creative copilot for AI image generation.**

> Distill great image-generation knowledge into better visual prompts.

Describe what you want. MuseForge will:

1. **Understand your intent**
2. **Find proven image-generation patterns**
3. **Recommend a visual direction**
4. **Design the composition**
5. **Apply relevant prompt techniques**
6. **Produce a production-ready prompt**

```
Idea
  ↓
Recipe
  ↓
Visual Pattern
  ↓
Style
  ↓
Technique
  ↓
Creative Direction
  ↓
Super Prompt
```

MuseForge is **not** a prompt collection, an awesome list, or a prompt cleaner. It absorbs
knowledge from multiple high-quality image-generation repositories and distills it into
**reusable knowledge** — recipes, visual patterns, styles, techniques, and prompt DNA — so it
can act like a **Creative Director + Prompt Engineer** for your image idea.

---

## Quick start

```bash
pip install -e ".[dev]"

museforge ask "帮我做一张 AI 公司招聘小红书封面，3:4，极简，专业，有一点 Claude 的编辑感。"
```

No API key required — the core path works offline with deterministic heuristics. (Optionally
configure an LLM provider via `.env` for richer intent understanding and composition.)

```bash
museforge ask "Create a premium fintech card advertisement"
museforge recipes search "poster"
museforge patterns search "product hero"
museforge styles search "editorial"
museforge techniques search "text rendering"
museforge optimize "..." --model nano-banana-pro
museforge stats
```

---

## What MuseForge knows

MuseForge stores **typed knowledge**, not raw prompts:

| Entity | What it is |
|---|---|
| **Case** | A complete, analyzed example (subject, composition, lighting, style, …) |
| **Recipe** | A method for a class of image task (steps, decision points, failure modes) |
| **Visual Pattern** | A reusable visual structure (e.g. Breakout Product Hero) |
| **Style** | A reusable visual system (e.g. editorial minimalism) |
| **Technique** | A prompt-engineering lever (e.g. text rendering, product preservation) |
| **Prompt DNA** | A composable prompt structure unit |
| **Model** | What a model can do, with a `source_type` label |

Every recommendation is **explainable**: the Assistant can always say *why* it recommended a
direction ("this case instantiates the Breakout Product Hero pattern, which the Product Hero
Ad recipe recommends").

---

## The pipeline

```
User request
  → Intent analysis
  → Knowledge retrieval (cases / recipes / patterns / styles / techniques / DNA)
  → Creative Director (design the image)
  → Prompt Composer (turn the design into a prompt)
  → Model Optimizer (model-specific variant)
  → Structured answer
```

See `docs/architecture.md` and `docs/methodology.md` for the full design.

---

## See it work

```bash
museforge ask "帮我做一张 AI 公司招聘小红书封面，3:4，极简，专业，有一点 Claude 的编辑感。"
```

MuseForge doesn't just return a prompt — it returns a **designed direction**:

```
Intent: recruitment marketing / social media poster
Platform: Xiaohongshu  Aspect ratio: 3:4

Recommended Recipe: Editorial Poster
  1. Set canvas/format and aspect ratio.
  2. Define the visual goal and message.
  ...

Recommended Pattern: Editorial Text-first Poster
Style: editorial minimalism
Key Techniques: text rendering, visual hierarchy, whitespace

Super Prompt:
  Format: 3:4 Xiaohongshu
  Visual goal: Communicate a message clearly and elegantly.
  Layout: text-first with a single focal point
  Visual hierarchy: headline -> supporting text -> illustration
  Style: editorial minimalism
  ...
```

Six full demos are in [`examples/`](examples/) — Xiaohongshu recruitment, fintech card ad, SaaS
hero, cinematic portrait, Chinese infographic, and multi-panel comic.

## Research foundation

MuseForge's knowledge model is grounded in a systematic study of 15+ high-quality
image-generation repositories. See:

- `docs/repository-comparison.md` — the evidence base.
- `docs/best-of-existing-repos.md` — the distilled assets.
- `docs/feature-comparison.md` — the feature adoption decisions.
- `docs/licensing.md` — attribution and redistribution policy.

---

## Status

**V0** — knowledge acquisition, deduplication, analysis, extraction, retrieval, creative
direction, and prompt composition. No image-generation API (yet). See `docs/roadmap.md`.

## License

MIT. Redistributed third-party prompts carry their own license and attribution — see
`docs/licensing.md`.

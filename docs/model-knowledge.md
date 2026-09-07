# Model Knowledge

MuseForge maintains knowledge about image-generation models — but **never fabricates
authority**. There is no real benchmark in V0, so every claim carries a `source_type` label.

## The `source_type` label

Every model knowledge entry carries one of:

| source_type | Meaning |
|---|---|
| `official` | From the model vendor's official documentation |
| `repository-derived` | Observed across multiple source repositories |
| `community-derived` | Reported by the community (X, forums, etc.) |
| `inferred` | Inferred from indirect evidence |
| `experimental` | From our own experiments |
| `unverified` | Unverified claim — treat with caution |

## The rule

MuseForge **never** says "Nano Banana performs best at X" without a labeled, reliable source.
Instead it says:

- "Community-derived guidance: strong multilingual text accuracy is reported."
- "Observed in source repositories: templated `[VARIABLE]` prompts are a practiced technique."

## The seed models

| Model | Family | Provider | source_type |
|---|---|---|---|
| GPT Image | gpt-image | OpenAI | community-derived |
| GPT Image 2 | gpt-image | OpenAI | repository-derived |
| Nano Banana | gemini | Google | community-derived |
| Nano Banana Pro | gemini | Google | repository-derived |
| Seedream | seedream | ByteDance | community-derived |

Each entry records `capabilities`, `strengths`, `limitations`, `text_rendering`,
`consistency`, `editing`, and `prompt_style_notes` — all phrased as *reported* observations,
not as benchmark results.

## How model knowledge is used

The **Model Optimizer** adapts a Universal Super Prompt to a target model by appending the
model's `prompt_style_notes`, `text_rendering`, and `consistency` guidance. Every optimization
carries an `optimization_basis` label:

- `repository-derived` — from `official` or `repository-derived` model knowledge.
- `community-derived` — from `community-derived` model knowledge.
- `heuristic` — no model-specific knowledge; a generic heuristic.

This keeps the system honest: the user always knows *why* a variant looks the way it does.

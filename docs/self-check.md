# V0 Self-Check

The final self-check from the project brief, answered honestly.

## 1. Does MuseForge look like another Awesome Prompt List?

**No.** An awesome list stores *text* in a flat numbered list. MuseForge stores *typed
knowledge* (case / recipe / pattern / style / technique / DNA / model) with explicit links, and
a Creative Director that *designs* before composing. The terminal output is a designed
direction + rationale, not a copied prompt.

## 2. Can a user with zero prompt-engineering knowledge use it?

**Yes.** `museforge ask "帮我做一张 AI 公司招聘小红书封面，3:4，极简，专业"` works with no
API key and no prompt-engineering knowledge. The user describes the image; MuseForge infers
intent, retrieves knowledge, designs the direction, and composes the prompt.

## 3. Does MuseForge actually use Case / Recipe / Pattern / Style / Technique / DNA?

**Yes.** The Assistant retrieves all six, and they drive the output:

- **Recipe** → the method (steps shown to the user) and the recommended pattern/style/techniques.
- **Pattern** → the composition, lighting, color, hierarchy.
- **Style** → the aesthetic (color/typography/texture behavior).
- **Technique** → the "Key Techniques" applied to the prompt.
- **DNA** → retrieved and available to the composer.
- **Case** → retrieved as evidence (shown in the response).

## 4. Can MuseForge explain why it recommends a direction?

**Yes.** Every `CreativeDirection` carries a `rationale` field, e.g.:

> "the Fintech Card Ad recipe matches the fintech marketing use case; the Breakout Product
> Hero pattern fits the visual goal; the luxury commercial style matches the requested
> aesthetic; 5 technique(s) apply to this task."

## 5. Is source attribution complete?

**Yes.** The source registry (`data/sources/`, 15 repositories) records license, redistribution
status, and attribution requirements. Every redistributed prompt carries `source_repo`,
`source_url`, `author`, and `license`. The seed knowledge is synthetic (authored for
MuseForge), and the three seed prompts are annotated exemplars from MIT / CC BY 4.0 sources
with full attribution.

## 6. Is there obvious duplicate knowledge?

**No.** The ingestion pipeline deduplicates at five levels (exact → normalized → near →
semantic → visual-intent), and the seed knowledge is curated (10 recipes, 10 patterns, 8
styles, 15 techniques, 5 DNA — no duplicates).

## 7. Is there any un-evidenced "model X is better" claim?

**No.** Every model knowledge entry carries a `source_type` label (official /
repository-derived / community-derived / inferred / experimental / unverified), and every
optimization carries an `optimization_basis` label. Capabilities are phrased as *reported*
observations, never as benchmark results.

## 8. Would adding MCP require a large refactor?

**No.** The architecture is `Knowledge Layer → Service Layer → CLI`, and MCP is a future
adapter over the Service Layer (see `docs/mcp-roadmap.md`). The MCP tools map 1:1 onto Service
Layer methods; no knowledge or service code changes.

---

## Verification status

- `pytest`: 58 passed.
- `ruff check .`: all checks passed.
- `mypy src/museforge`: no issues in 39 source files.
- `museforge ask` (6 demos): all route correctly.

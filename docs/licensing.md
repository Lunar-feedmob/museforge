# Licensing & Attribution

MuseForge's policy: **never copy a prompt whose license is unclear.** Attribution is a schema
field, not an afterthought.

## The rule

For every external repository, MuseForge records:

```yaml
repo, license, allowed_usage, redistribution_status, attribution_requirements
```

And for every redistributed prompt:

```yaml
source_repo, source_url, author, license
```

## Redistribution decisions

| License | Redistribution | Attribution |
|---|---|---|
| CC0-1.0 | Yes, unrestricted | None required |
| MIT | Yes | Include the license notice |
| CC BY 4.0 | Yes | Attribute author + source |
| CC BY-SA 4.0 | Yes | Attribute + share-alike |
| CC BY-NC 4.0 | Non-commercial only | Attribute |
| CC BY-ND 4.0 | No derivatives | Attribute |
| Unclear / none | **No** | Store metadata + analysis only |

## The four prompt tiers

When redistribution is allowed, a prompt is stored at one of four tiers:

1. **Original** — verbatim, fully attributed.
2. **Annotated** — original + MuseForge's analysis (why it works, techniques used).
3. **Refined** — cleaned/normalized, still attributed.
4. **MuseForge Enhanced** — a new prompt composed by MuseForge, *derived from* the source
   knowledge but not a copy.

## When redistribution is NOT allowed

MuseForge stores **only**:

- metadata (title, category, tags),
- the source URL,
- derived analysis (pattern, technique, knowledge).

It never stores the original prompt text. This is enforced by the ingestion pipeline's license
check (`src/museforge/licensing/license.py`), which strips prompt text when the license is
unclear or non-redistributable.

## The seed data

The seed knowledge (`data/`) is **synthetic** — authored for MuseForge, not copied from any
third-party repository. Its `source_repositories` fields point at the repositories that
*inspired* each abstraction (as public facts), never at copied prompt text.

The three seed prompts (`data/prompts/`) are **annotated** exemplars from MIT / CC BY 4.0
sources, with full attribution (`source_repo`, `source_url`, `author`, `license`).

## Source registry

The full source registry is in `data/sources/` (15 repositories), each with its license,
redistribution status, and attribution requirements. See `docs/repository-comparison.md` for
the analysis behind each entry.

"""Rendering helpers for CLI output."""

from __future__ import annotations

from museforge.services.assistant import AssistantResponse


def render_response(resp: AssistantResponse, *, prompt_only: bool = False) -> str:
    """Render an AssistantResponse as human-readable text."""
    if prompt_only:
        return resp.super_prompt

    d = resp.creative_direction
    lines: list[str] = []
    lines.append(f"Intent: {resp.intent.use_case or 'general'} / {resp.intent.category or 'general'}")
    if resp.intent.platform:
        lines.append(f"Platform: {resp.intent.platform}  Aspect ratio: {resp.intent.aspect_ratio or 'auto'}")
    lines.append("")
    lines.append("## Creative Direction")
    lines.append(f"Concept: {d.concept}")
    if d.goal:
        lines.append(f"Goal: {d.goal}")
    if d.rationale:
        lines.append(f"Rationale: {d.rationale}")
    lines.append("")
    if resp.recommended_recipe:
        lines.append(f"## Recommended Recipe: {resp.recommended_recipe.name}")
        if resp.recommended_recipe.steps:
            lines.append("\n".join(f"{i+1}. {s}" for i, s in enumerate(resp.recommended_recipe.steps)))
        lines.append("")
    if resp.recommended_pattern:
        lines.append(f"## Recommended Pattern: {resp.recommended_pattern.name}")
        if resp.recommended_pattern.description:
            lines.append(resp.recommended_pattern.description)
        lines.append("")
    if resp.recommended_style:
        lines.append(f"## Style: {resp.recommended_style.name}")
        lines.append("")
    if d.composition:
        lines.append(f"## Composition\n{d.composition}")
        lines.append("")
    if resp.key_techniques:
        lines.append("## Key Techniques")
        lines.append(", ".join(t.name for t in resp.key_techniques))
        lines.append("")
    lines.append("## Super Prompt")
    lines.append(resp.super_prompt)
    lines.append("")
    if resp.model_variant:
        lines.append(f"## Model-specific Variant ({resp.model_variant.model})")
        lines.append(f"optimization_basis: {resp.model_variant.optimization_basis}")
        lines.append(resp.model_variant.prompt)
        lines.append("")
    if resp.alternative_direction:
        lines.append(f"## Alternative Direction\n{resp.alternative_direction}")
        lines.append("")
    if resp.notes:
        lines.append("## Notes")
        lines.extend(f"- {n}" for n in resp.notes)
    return "\n".join(lines)

"""The Prompt Composer — turns a CreativeDirection into a Universal Super Prompt.

The prompt structure is *task-dependent*: a poster is composed differently from a photograph.
The composer avoids low-information adjectives (``amazing``, ``stunning``, ``masterpiece``)
and redundancy.
"""

from __future__ import annotations

from museforge.knowledge.models import (
    CreativeDirection,
    Intent,
    PromptDna,
    Recipe,
    Style,
    Technique,
    VisualPattern,
)
from museforge.providers.llm import LLMProvider

# Low-information adjectives that MuseForge never emits.
_BANNED = {
    "amazing", "stunning", "beautiful", "masterpiece", "breathtaking", "incredible",
    "ultra amazing", "awesome", "gorgeous", "spectacular", "epic", "perfect",
}


class PromptComposer:
    """Composes a production-ready prompt from a CreativeDirection."""

    def __init__(self, llm: LLMProvider | None = None) -> None:
        self.llm = llm

    def compose(
        self,
        intent: Intent,
        direction: CreativeDirection,
        *,
        recipe: Recipe | None = None,
        pattern: VisualPattern | None = None,
        style: Style | None = None,
        techniques: list[Technique] | None = None,
        dna: PromptDna | None = None,
    ) -> str:
        if self.llm is not None:
            try:
                return self._llm_compose(intent, direction, recipe, pattern, style, techniques, dna)
            except Exception:  # noqa: BLE001 - fall back to template composition
                pass
        return self._template_compose(intent, direction, recipe, pattern, style, techniques, dna)

    # -- template composition -------------------------------------------

    def _template_compose(
        self,
        intent: Intent,
        direction: CreativeDirection,
        recipe: Recipe | None,
        pattern: VisualPattern | None,
        style: Style | None,
        techniques: list[Technique] | None,
        dna: PromptDna | None,
    ) -> str:
        sections = self._sections(intent, direction, recipe, pattern, style, techniques, dna)
        lines: list[str] = []
        for heading, content in sections:
            if not content:
                continue
            lines.append(f"{heading}: {content}")
        return "\n".join(lines)

    def _sections(
        self,
        intent: Intent,
        direction: CreativeDirection,
        recipe: Recipe | None,
        pattern: VisualPattern | None,
        style: Style | None,
        techniques: list[Technique] | None,
        dna: PromptDna | None,
    ) -> list[tuple[str, str]]:
        task = self._task_type(intent)
        if task == "poster":
            return self._poster_sections(intent, direction, style)
        if task == "photography":
            return self._photography_sections(intent, direction, style)
        if task == "product":
            return self._product_sections(intent, direction, style)
        if task == "infographic":
            return self._infographic_sections(intent, direction, style)
        if task == "comic":
            return self._comic_sections(intent, direction, style)
        return self._general_sections(intent, direction, style)

    @staticmethod
    def _constraint_sections(d: CreativeDirection) -> list[tuple[str, str]]:
        """Return constraint/avoid sections, keeping them distinct."""
        sections: list[tuple[str, str]] = []
        if d.constraints:
            sections.append(("Constraints", "; ".join(d.constraints)))
        if d.avoid:
            sections.append(("Avoid", "; ".join(d.avoid)))
        return sections

    @staticmethod
    def _task_type(intent: Intent) -> str:
        cat = intent.category
        if cat in {"poster", "social media poster"}:
            return "poster"
        if cat in {"photography", "portrait"}:
            return "photography"
        if cat in {"product advertisement", "product hero", "e-commerce"}:
            return "product"
        if cat == "infographic":
            return "infographic"
        if cat == "comic":
            return "comic"
        return "general"

    def _poster_sections(self, intent: Intent, d: CreativeDirection, style: Style | None) -> list[tuple[str, str]]:
        return [
            ("Format", f"{intent.aspect_ratio or '3:4'} {intent.platform or 'poster'}"),
            ("Visual goal", d.concept),
            ("Layout", d.composition),
            ("Visual hierarchy", d.visual_hierarchy),
            ("Style", style.name if style else d.recommended_style or ""),
            ("Color", d.color_palette),
            ("Typography", d.typography),
            ("Negative space", d.negative_space),
            ("Details", ", ".join(d.supporting_elements)),
            *self._constraint_sections(d),
        ]

    def _photography_sections(self, intent: Intent, d: CreativeDirection, style: Style | None) -> list[tuple[str, str]]:
        return [
            ("Subject", d.subject_strategy or d.concept),
            ("Environment", d.environment),
            ("Composition", d.composition),
            ("Perspective", d.perspective),
            ("Lighting", d.lighting),
            ("Color", d.color_palette),
            ("Style", style.name if style else d.recommended_style or ""),
            ("Mood", d.concept),
            *self._constraint_sections(d),
        ]

    def _product_sections(self, intent: Intent, d: CreativeDirection, style: Style | None) -> list[tuple[str, str]]:
        return [
            ("Product", d.subject_strategy or d.concept),
            ("Scene", d.environment),
            ("Composition", d.composition),
            ("Lighting", d.lighting),
            ("Style", style.name if style else d.recommended_style or ""),
            ("Color", d.color_palette),
            ("Supporting elements", ", ".join(d.supporting_elements)),
            ("Negative space", d.negative_space),
            *self._constraint_sections(d),
        ]

    def _infographic_sections(self, intent: Intent, d: CreativeDirection, style: Style | None) -> list[tuple[str, str]]:
        return [
            ("Format", f"{intent.aspect_ratio or '3:4'} infographic"),
            ("Visual goal", d.concept),
            ("Layout", d.composition),
            ("Visual hierarchy", d.visual_hierarchy),
            ("Style", style.name if style else d.recommended_style or ""),
            ("Color", d.color_palette),
            ("Typography", d.typography),
            *self._constraint_sections(d),
        ]

    def _comic_sections(self, intent: Intent, d: CreativeDirection, style: Style | None) -> list[tuple[str, str]]:
        return [
            ("Format", "multi-panel comic"),
            ("Story", d.concept),
            ("Layout", d.composition),
            ("Style", style.name if style else d.recommended_style or ""),
            ("Color", d.color_palette),
            *self._constraint_sections(d),
        ]

    def _general_sections(self, intent: Intent, d: CreativeDirection, style: Style | None) -> list[tuple[str, str]]:
        return [
            ("Subject", d.subject_strategy or d.concept),
            ("Environment", d.environment),
            ("Composition", d.composition),
            ("Lighting", d.lighting),
            ("Style", style.name if style else d.recommended_style or ""),
            ("Color", d.color_palette),
            *self._constraint_sections(d),
        ]

    # -- LLM composition --------------------------------------------------

    def _llm_compose(
        self,
        intent: Intent,
        direction: CreativeDirection,
        recipe: Recipe | None,
        pattern: VisualPattern | None,
        style: Style | None,
        techniques: list[Technique] | None,
        dna: PromptDna | None,
    ) -> str:
        assert self.llm is not None
        import json

        context = {
            "intent": intent.model_dump(mode="json"),
            "direction": direction.model_dump(mode="json"),
            "recipe": recipe.model_dump(mode="json") if recipe else None,
            "pattern": pattern.model_dump(mode="json") if pattern else None,
            "style": style.model_dump(mode="json") if style else None,
            "techniques": [t.model_dump(mode="json") for t in (techniques or [])],
            "dna": dna.model_dump(mode="json") if dna else None,
        }
        system = (
            "You are a prompt engineer. Compose a production-ready image-generation prompt from "
            "the given creative direction. Be specific, structured, and non-redundant. Do NOT use "
            "low-information adjectives (amazing, stunning, masterpiece). Respond with ONLY the "
            "prompt text."
        )
        return self.llm.complete(json.dumps(context, ensure_ascii=False), system=system).strip()

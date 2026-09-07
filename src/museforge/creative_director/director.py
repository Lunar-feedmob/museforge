"""The Creative Director — designs the image before the prompt is composed.

The director is the layer that makes MuseForge more than a retriever + prompt stitcher. It
takes the user's intent and the retrieved knowledge, and produces a ``CreativeDirection``: a
complete visual plan (concept, hierarchy, composition, lighting, color, typography, …). The
Prompt Composer then *translates* that plan into a prompt.
"""

from __future__ import annotations

from typing import Any

from museforge.knowledge.models import CreativeDirection, Intent, Recipe, Style, VisualPattern
from museforge.providers.llm import LLMProvider


class CreativeDirector:
    """Designs a visual direction from intent + retrieved knowledge."""

    def __init__(self, llm: LLMProvider | None = None) -> None:
        self.llm = llm

    def design(
        self,
        intent: Intent,
        *,
        recipe: Recipe | None = None,
        pattern: VisualPattern | None = None,
        style: Style | None = None,
        techniques: list[Any] | None = None,
    ) -> CreativeDirection:
        if self.llm is not None:
            try:
                return self._llm_design(intent, recipe, pattern, style, techniques)
            except Exception:  # noqa: BLE001 - fall back to heuristics
                pass
        return self._heuristic_design(intent, recipe, pattern, style, techniques)

    # -- heuristic design -------------------------------------------------

    def _heuristic_design(
        self,
        intent: Intent,
        recipe: Recipe | None,
        pattern: VisualPattern | None,
        style: Style | None,
        techniques: list[Any] | None,
    ) -> CreativeDirection:
        techniques = techniques or []
        concept = self._concept(intent, recipe, pattern)
        return CreativeDirection(
            concept=concept,
            goal=recipe.goal if recipe else intent.use_case,
            recommended_recipe=recipe.id if recipe else None,
            recommended_pattern=pattern.id if pattern else None,
            recommended_style=style.id if style else None,
            visual_hierarchy=pattern.visual_hierarchy if pattern else self._default_hierarchy(intent),
            composition=pattern.composition if pattern else self._default_composition(intent),
            subject_strategy=pattern.subject_placement if pattern else "",
            environment=pattern.background if pattern else "",
            perspective=pattern.perspective if pattern else "",
            lighting=pattern.lighting_strategy if pattern else self._default_lighting(intent),
            color_palette=style.color_behavior if style else pattern.color_strategy if pattern else "",
            typography=style.typography_behavior if style else pattern.typography_strategy if pattern else "",
            supporting_elements=list(pattern.supporting_elements) if pattern else [],
            negative_space=pattern.negative_space_strategy if pattern else "",
            visual_density=intent.visual_density,
            constraints=list(recipe.constraints) if recipe else [],
            avoid=list(style.avoid) if style else [],
            rationale=self._rationale(intent, recipe, pattern, style, techniques),
        )

    @staticmethod
    def _concept(intent: Intent, recipe: Recipe | None, pattern: VisualPattern | None) -> str:
        if pattern and pattern.visual_goal:
            return pattern.visual_goal
        if recipe and recipe.goal:
            return recipe.goal
        return f"A {intent.style or 'clean'} visual for {intent.use_case or 'the request'}."

    @staticmethod
    def _default_hierarchy(intent: Intent) -> str:
        if intent.priority == "text readability":
            return "Headline first, then supporting text, then illustration."
        return "Hero subject first, then supporting elements."

    @staticmethod
    def _default_composition(intent: Intent) -> str:
        if intent.category in {"poster", "social media poster", "infographic"}:
            return "Text-first layout with a clear focal point and generous margins."
        return "Centered hero subject with strong foreground/background separation."

    @staticmethod
    def _default_lighting(intent: Intent) -> str:
        if intent.style in {"luxury commercial", "premium commercial"}:
            return "Soft commercial lighting with controlled highlights."
        return "Clean, even lighting."

    @staticmethod
    def _rationale(
        intent: Intent,
        recipe: Recipe | None,
        pattern: VisualPattern | None,
        style: Style | None,
        techniques: list[Any],
    ) -> str:
        parts: list[str] = []
        if recipe:
            parts.append(f"the {recipe.name} recipe matches the {intent.use_case or 'requested'} use case")
        if pattern:
            parts.append(f"the {pattern.name} pattern fits the visual goal")
        if style:
            parts.append(f"the {style.name} style matches the requested aesthetic")
        if techniques:
            parts.append(f"{len(techniques)} technique(s) apply to this task")
        return "; ".join(parts) + "." if parts else "Heuristic direction."

    # -- LLM design -------------------------------------------------------

    def _llm_design(
        self,
        intent: Intent,
        recipe: Recipe | None,
        pattern: VisualPattern | None,
        style: Style | None,
        techniques: list[Any] | None,
    ) -> CreativeDirection:
        assert self.llm is not None
        import json

        context = {
            "intent": intent.model_dump(mode="json"),
            "recipe": recipe.model_dump(mode="json") if recipe else None,
            "pattern": pattern.model_dump(mode="json") if pattern else None,
            "style": style.model_dump(mode="json") if style else None,
            "techniques": [t.model_dump(mode="json") for t in (techniques or [])],
        }
        system = (
            "You are a Creative Director for AI image generation. Design a visual direction. "
            "Respond with ONLY a JSON object matching the CreativeDirection schema."
        )
        data = json.loads(self.llm.complete(json.dumps(context, ensure_ascii=False), system=system))
        return CreativeDirection.model_validate(data)

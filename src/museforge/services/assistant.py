"""MuseForgeAssistant — the product core.

Orchestrates the full path: understand → retrieve → design → compose → optimize → respond.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from museforge.analyzers.intent import IntentAnalyzer
from museforge.creative_director.director import CreativeDirector
from museforge.knowledge.models import (
    Case,
    CreativeDirection,
    Intent,
    Prompt,
    PromptDna,
    Recipe,
    Style,
    Technique,
    VisualPattern,
)
from museforge.knowledge.store import KnowledgeStore
from museforge.model_optimizer.optimizer import ModelOptimizer, OptimizedPrompt
from museforge.prompt_composer.composer import PromptComposer
from museforge.providers.llm import LLMProvider
from museforge.retrieval.retrievers import (
    CaseRetriever,
    DnaRetriever,
    PatternRetriever,
    PromptRetriever,
    RecipeRetriever,
    StyleRetriever,
    TechniqueRetriever,
)


@dataclass
class AssistantResponse:
    """The structured answer returned to the user."""

    intent: Intent
    creative_direction: CreativeDirection
    recommended_recipe: Recipe | None = None
    recommended_pattern: VisualPattern | None = None
    recommended_style: Style | None = None
    key_techniques: list[Technique] = field(default_factory=list)
    retrieved_cases: list[Case] = field(default_factory=list)
    super_prompt: str = ""
    model_variant: OptimizedPrompt | None = None
    alternative_direction: str = ""
    notes: list[str] = field(default_factory=list)


class MuseForgeAssistant:
    """The MuseForge assistant: Creative Director + Prompt Engineer."""

    def __init__(self, store: KnowledgeStore, *, llm: LLMProvider | None = None) -> None:
        self.store = store
        self.llm = llm
        self.intent_analyzer = IntentAnalyzer(llm)
        self.cases = CaseRetriever(store)
        self.prompts = PromptRetriever(store)
        self.recipes = RecipeRetriever(store)
        self.patterns = PatternRetriever(store)
        self.styles = StyleRetriever(store)
        self.techniques = TechniqueRetriever(store)
        self.dna = DnaRetriever(store)
        self.director = CreativeDirector(llm)
        self.composer = PromptComposer(llm)
        self.optimizer = ModelOptimizer(store)

    # -- the pipeline ----------------------------------------------------

    def understand_request(self, request: str) -> Intent:
        return self.intent_analyzer.understand_request(request)

    def retrieve_cases(self, query: str, top_k: int = 3) -> list[Case]:
        return [c for c, _ in self.cases.search(query, top_k) if isinstance(c, Case)]

    def retrieve_prompts(self, query: str, top_k: int = 3) -> list[Prompt]:
        return [p for p, _ in self.prompts.search(query, top_k) if isinstance(p, Prompt)]

    def analyze_constraints(self, request: str) -> dict[str, str]:
        """Extract the explicit constraints (platform, ratio, priority, density) from a request."""
        intent = self.understand_request(request)
        return {
            "platform": intent.platform,
            "aspect_ratio": intent.aspect_ratio,
            "priority": intent.priority,
            "visual_density": intent.visual_density,
        }

    def design_composition(self, intent: Intent, direction: CreativeDirection) -> str:
        """Return the composition plan from a designed direction."""
        return direction.composition

    def retrieve_recipes(self, query: str, top_k: int = 3) -> list[Recipe]:
        return [r for r, _ in self.recipes.search(query, top_k) if isinstance(r, Recipe)]

    def retrieve_patterns(self, query: str, top_k: int = 3) -> list[VisualPattern]:
        return [p for p, _ in self.patterns.search(query, top_k) if isinstance(p, VisualPattern)]

    def retrieve_styles(self, query: str, top_k: int = 3) -> list[Style]:
        return [s for s, _ in self.styles.search(query, top_k) if isinstance(s, Style)]

    def retrieve_techniques(self, query: str, top_k: int = 5) -> list[Technique]:
        return [t for t, _ in self.techniques.search(query, top_k) if isinstance(t, Technique)]

    def retrieve_prompt_dna(self, query: str, top_k: int = 3) -> list[PromptDna]:
        return [d for d, _ in self.dna.search(query, top_k) if isinstance(d, PromptDna)]

    def recommend_direction(
        self,
        intent: Intent,
        *,
        recipe: Recipe | None = None,
        pattern: VisualPattern | None = None,
        style: Style | None = None,
        techniques: list[Technique] | None = None,
    ) -> CreativeDirection:
        return self.director.design(intent, recipe=recipe, pattern=pattern, style=style, techniques=techniques)

    def compose_prompt(
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
        return self.composer.compose(
            intent, direction, recipe=recipe, pattern=pattern, style=style, techniques=techniques, dna=dna
        )

    def optimize_for_model(self, prompt: str, model: str) -> OptimizedPrompt:
        return self.optimizer.optimize(prompt, model)

    def improve_prompt(self, prompt: str, feedback: str = "") -> str:
        """Improve an existing prompt (V0: heuristic — strip banned adjectives + append feedback)."""
        from museforge.prompt_composer.composer import _BANNED

        words = prompt.split()
        cleaned = " ".join(w for w in words if w.strip(".,;:").lower() not in _BANNED)
        if feedback:
            cleaned = cleaned.rstrip() + f"\nAdditional guidance: {feedback}"
        return cleaned

    # -- the full path ----------------------------------------------------

    def generate_response(
        self,
        request: str,
        *,
        model: str = "universal",
        prompt_only: bool = False,
    ) -> AssistantResponse:
        intent = self.understand_request(request)
        query = self._query(intent, request)

        recipes = self.retrieve_recipes(query)
        patterns = self.retrieve_patterns(query)
        styles = self.retrieve_styles(query)
        dna_list = self.retrieve_prompt_dna(query)
        cases = self.retrieve_cases(query)

        recipe = recipes[0] if recipes else None
        pattern = self._pick_pattern(intent, patterns, recipe)
        style = self._pick_style(intent, styles, recipe)
        dna = dna_list[0] if dna_list else None
        techniques = self._select_techniques(recipe, pattern, self.retrieve_techniques(query))

        direction = self.recommend_direction(intent, recipe=recipe, pattern=pattern, style=style, techniques=techniques)
        super_prompt = self.compose_prompt(
            intent, direction, recipe=recipe, pattern=pattern, style=style, techniques=techniques, dna=dna
        )
        variant = self.optimize_for_model(super_prompt, model) if model != "universal" else None

        return AssistantResponse(
            intent=intent,
            creative_direction=direction,
            recommended_recipe=recipe,
            recommended_pattern=pattern,
            recommended_style=style,
            key_techniques=techniques,
            retrieved_cases=cases,
            super_prompt=super_prompt,
            model_variant=variant,
            alternative_direction=self._alternative(intent, patterns, styles),
            notes=self._notes(intent, recipe, pattern, style, techniques),
        )

    # -- helpers ---------------------------------------------------------

    @staticmethod
    def _query(intent: Intent, request: str) -> str:
        parts = [request, intent.use_case, intent.category, intent.style, intent.likely_pattern]
        return " ".join(p for p in parts if p)

    def _select_techniques(
        self,
        recipe: Recipe | None,
        pattern: VisualPattern | None,
        retrieved: list[Technique],
    ) -> list[Technique]:
        """Prioritize techniques recommended by the recipe/pattern, then fill with retrieved.

        Recommended techniques are looked up by id/name from the full store (not just the
        retrieved top-k), so a recipe's guidance is always honored.
        """
        preferred: list[str] = []
        if recipe:
            preferred.extend(recipe.recommended_techniques)
        if pattern:
            preferred.extend(pattern.related_techniques)
        ordered: list[Technique] = []
        seen: set[str] = set()
        for ref in preferred:
            t = self.techniques.get(ref)
            if t is not None and isinstance(t, Technique) and t.id not in seen:
                ordered.append(t)
                seen.add(t.id)
        for t in retrieved:
            if t.id not in seen:
                ordered.append(t)
                seen.add(t.id)
        return ordered[:5]

    @staticmethod
    def _pick_pattern(intent: Intent, patterns: list[VisualPattern], recipe: Recipe | None) -> VisualPattern | None:
        # The recipe's curated recommendations are more reliable than the coarse intent heuristic.
        if recipe:
            for pid in recipe.recommended_patterns:
                for p in patterns:
                    if p.id == pid or p.name == pid:
                        return p
        if intent.likely_pattern:
            for p in patterns:
                if p.name == intent.likely_pattern or intent.likely_pattern in p.aliases:
                    return p
        return patterns[0] if patterns else None

    @staticmethod
    def _pick_style(intent: Intent, styles: list[Style], recipe: Recipe | None) -> Style | None:
        if intent.style:
            for s in styles:
                if s.name == intent.style or intent.style in s.aliases:
                    return s
        if recipe:
            for sid in recipe.recommended_styles:
                for s in styles:
                    if s.id == sid or s.name == sid:
                        return s
        return styles[0] if styles else None

    @staticmethod
    def _alternative(intent: Intent, patterns: list[VisualPattern], styles: list[Style]) -> str:
        alt_parts: list[str] = []
        if len(patterns) > 1:
            alt_parts.append(f"pattern: {patterns[1].name}")
        if len(styles) > 1:
            alt_parts.append(f"style: {styles[1].name}")
        return "; ".join(alt_parts) if alt_parts else ""

    @staticmethod
    def _notes(
        intent: Intent,
        recipe: Recipe | None,
        pattern: VisualPattern | None,
        style: Style | None,
        techniques: list[Technique],
    ) -> list[str]:
        notes: list[str] = []
        if recipe and recipe.common_failures:
            notes.append(f"Watch for: {', '.join(recipe.common_failures[:3])}")
        if pattern and pattern.common_failures:
            notes.append(f"Pattern pitfalls: {', '.join(pattern.common_failures[:3])}")
        if not techniques:
            notes.append("No techniques matched; the prompt is composed from the direction alone.")
        return notes

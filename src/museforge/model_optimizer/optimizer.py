"""The Model Optimizer — adapts a Universal Super Prompt to a target model.

There is no real benchmark in V0, so the optimizer never claims a model "performs best". Every
optimization carries an ``optimization_basis`` label (repository-derived / community-derived /
heuristic) and is grounded in the model's ``ModelKnowledge`` (which itself carries a
``source_type`` label).
"""

from __future__ import annotations

from dataclasses import dataclass

from museforge.knowledge.models import ModelKnowledge
from museforge.knowledge.store import KnowledgeStore

# Canonical model ids → the id used in data/models/.
_MODEL_ALIASES = {
    "universal": "universal",
    "gpt-image": "gpt-image",
    "gpt-image-1": "gpt-image",
    "gpt-image-2": "gpt-image-2",
    "gptimage2": "gpt-image-2",
    "nano-banana": "nano-banana",
    "nanobanana": "nano-banana",
    "nano-banana-pro": "nano-banana-pro",
    "nanobanana-pro": "nano-banana-pro",
    "nano-banana-2": "nano-banana-2",
    "seedream": "seedream",
    "seedream-4.5": "seedream",
    "seedream-5": "seedream",
}


@dataclass
class OptimizedPrompt:
    """A model-specific prompt variant with its optimization basis."""

    model: str
    prompt: str
    optimization_basis: str
    notes: list[str]


class ModelOptimizer:
    """Adapts a prompt to a target model using labeled model knowledge."""

    def __init__(self, store: KnowledgeStore) -> None:
        self.store = store
        self._models: dict[str, ModelKnowledge] = {
            m.id: m for m in store.load("model") if isinstance(m, ModelKnowledge)
        }

    def optimize(self, prompt: str, model: str) -> OptimizedPrompt:
        canonical = _MODEL_ALIASES.get(model.lower(), model.lower())
        knowledge = self._models.get(canonical)
        if canonical == "universal" or knowledge is None:
            return OptimizedPrompt(
                model=model,
                prompt=prompt,
                optimization_basis="heuristic",
                notes=["No model-specific knowledge; returning the universal prompt."],
            )
        notes: list[str] = []
        additions: list[str] = []
        if knowledge.text_rendering:
            additions.append(f"Render all text exactly as written ({knowledge.text_rendering}).")
        if knowledge.consistency:
            additions.append(f"Maintain consistency: {knowledge.consistency}.")
        if knowledge.prompt_style_notes:
            additions.append(knowledge.prompt_style_notes)
        basis = self._basis(knowledge)
        notes.append(f"optimization_basis={basis}; source_type={knowledge.source_type.value}")
        if additions:
            prompt = prompt.rstrip() + "\n" + "\n".join(additions)
        return OptimizedPrompt(model=model, prompt=prompt, optimization_basis=basis, notes=notes)

    @staticmethod
    def _basis(knowledge: ModelKnowledge) -> str:
        if knowledge.source_type.value in {"official", "repository-derived"}:
            return "repository-derived"
        if knowledge.source_type.value == "community-derived":
            return "community-derived"
        return "heuristic"

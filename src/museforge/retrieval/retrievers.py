"""Typed retrievers over the knowledge store.

Each retriever wraps a ``Retriever`` for a specific entity type and exposes a ``search``
method plus typed ``get`` access. The Assistant composes these.
"""

from __future__ import annotations

from typing import Any

from museforge.knowledge.models import (
    Case,
    ModelKnowledge,
    Prompt,
    PromptDna,
    Recipe,
    Source,
    Style,
    Technique,
    VisualPattern,
)
from museforge.knowledge.store import KnowledgeStore
from museforge.retrieval.search import Retriever


class _TypedRetriever:
    entity: str = ""

    def __init__(self, store: KnowledgeStore) -> None:
        self.store = store
        self._retriever = Retriever(store.load(self.entity))

    def search(self, query: str, top_k: int = 5) -> list[tuple[Any, float]]:
        return self._retriever.search(query, top_k)

    def get(self, ident: str) -> Any | None:
        return self._retriever.get(ident)

    def all(self) -> list[Any]:
        return self._retriever.entities


class CaseRetriever(_TypedRetriever):
    entity = "case"


class RecipeRetriever(_TypedRetriever):
    entity = "recipe"


class PatternRetriever(_TypedRetriever):
    entity = "pattern"


class StyleRetriever(_TypedRetriever):
    entity = "style"


class TechniqueRetriever(_TypedRetriever):
    entity = "technique"


class DnaRetriever(_TypedRetriever):
    entity = "dna"


class PromptRetriever(_TypedRetriever):
    entity = "prompt"


class SourceRetriever(_TypedRetriever):
    entity = "source"


class ModelRetriever(_TypedRetriever):
    entity = "model"


__all__ = [
    "Case",
    "CaseRetriever",
    "DnaRetriever",
    "ModelKnowledge",
    "ModelRetriever",
    "PatternRetriever",
    "Prompt",
    "PromptDna",
    "PromptRetriever",
    "Recipe",
    "RecipeRetriever",
    "Source",
    "SourceRetriever",
    "Style",
    "StyleRetriever",
    "Technique",
    "TechniqueRetriever",
    "VisualPattern",
]

"""Knowledge extractors — turn analyzed cases into reusable abstractions.

These are the LLM-dependent parts of the ingestion pipeline. V0 ships a working LLM-based
extractor behind a stable interface; the seed knowledge is hand-authored, so these run only
when a user ingests new repositories with an LLM configured.
"""

from __future__ import annotations

import json
from typing import Any, Protocol

from museforge.knowledge.models import (
    PromptDna,
    Recipe,
    Style,
    Technique,
    VisualPattern,
    model_for,
)
from museforge.providers.llm import LLMProvider


class Extractor(Protocol):
    """An extractor that turns a case into a reusable knowledge entity."""

    entity: str

    def extract(self, case: dict[str, Any]) -> dict[str, Any]:
        ...


class LlmExtractor:
    """Extract a knowledge entity from a case using an LLM.

    The LLM is asked to produce a JSON object matching the entity's schema; the result is
    validated against the Pydantic model before being returned.
    """

    def __init__(self, entity: str, llm: LLMProvider) -> None:
        self.entity = entity
        self.llm = llm
        self.model = model_for(entity)

    def extract(self, case: dict[str, Any]) -> dict[str, Any]:
        system = (
            f"You extract a {self.entity} from an image-generation case. Respond with ONLY a "
            f"JSON object matching this schema: {json.dumps(self.model.model_json_schema())}. "
            "Use empty strings/arrays for unknown fields."
        )
        raw = self.llm.complete(json.dumps(case, ensure_ascii=False), system=system)
        data = json.loads(raw)
        return self.model.model_validate(data).model_dump(mode="json")


# Concrete extractor factories (used by the ingestion pipeline).
def recipe_extractor(llm: LLMProvider) -> LlmExtractor:
    return LlmExtractor("recipe", llm)


def pattern_extractor(llm: LLMProvider) -> LlmExtractor:
    return LlmExtractor("pattern", llm)


def style_extractor(llm: LLMProvider) -> LlmExtractor:
    return LlmExtractor("style", llm)


def technique_extractor(llm: LLMProvider) -> LlmExtractor:
    return LlmExtractor("technique", llm)


def dna_extractor(llm: LLMProvider) -> LlmExtractor:
    return LlmExtractor("dna", llm)


__all__ = [
    "Extractor",
    "LlmExtractor",
    "PromptDna",
    "Recipe",
    "Style",
    "Technique",
    "VisualPattern",
    "dna_extractor",
    "pattern_extractor",
    "recipe_extractor",
    "style_extractor",
    "technique_extractor",
]

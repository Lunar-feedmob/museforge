"""Schema validation tests — the Pydantic models and JSON schemas must agree."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from museforge.knowledge.models import (
    ENTITY_MODELS,
    Case,
    Recipe,
    SourceType,
    VisualPattern,
    model_for,
    validate_entity,
)

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"


def test_entity_models_registered() -> None:
    assert set(ENTITY_MODELS) == {
        "source", "prompt", "case", "recipe", "pattern", "style",
        "technique", "dna", "model", "feature", "creative-direction",
    }


def test_minimal_case_validates() -> None:
    case = Case(id="c1", title="A case")
    assert case.id == "c1"
    assert case.pattern_ids == []


def test_case_rejects_bad_confidence() -> None:
    with pytest.raises(ValidationError):
        Recipe(id="r1", name="bad", confidence=1.5)


def test_source_type_enum() -> None:
    assert SourceType.REPOSITORY_DERIVED.value == "repository-derived"
    assert SourceType.UNVERIFIED.value == "unverified"


def test_validate_entity_roundtrip() -> None:
    data = {"id": "p1", "name": "Breakout Product Hero", "category": "product"}
    obj = validate_entity("pattern", data)
    assert isinstance(obj, VisualPattern)
    assert obj.name == "Breakout Product Hero"


def test_model_for_unknown_raises() -> None:
    with pytest.raises(ValueError):
        model_for("nope")


@pytest.mark.parametrize("entity", list(ENTITY_MODELS))
def test_json_schema_exists_and_matches_model(entity: str) -> None:
    """Every entity has a generated JSON schema whose required fields match the model."""
    path = SCHEMAS_DIR / f"{entity}.schema.json"
    assert path.is_file(), f"missing schema for {entity}"
    schema = json.loads(path.read_text(encoding="utf-8"))
    model = model_for(entity)
    model_schema = model.model_json_schema()
    # The generated schema must carry the same required fields as the model.
    assert set(schema.get("required", [])) == set(model_schema.get("required", []))

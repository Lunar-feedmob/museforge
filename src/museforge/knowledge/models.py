"""Pydantic models for MuseForge's knowledge entities.

These models are the single source of truth for the knowledge schema. The JSON schemas in
``schemas/`` are generated from them (see ``scripts/generate_schemas.py``) so the two can
never drift apart.

Every entity is a *knowledge* object, not a prompt. Prompts are the *output* of the system;
knowledge is the *input*.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class SourceKind(StrEnum):
    GITHUB = "github"
    WEB = "web"
    COMMUNITY = "community"
    OFFICIAL = "official"


class PromptTier(StrEnum):
    ORIGINAL = "original"
    ANNOTATED = "annotated"
    REFINED = "refined"
    ENHANCED = "enhanced"


class SourceType(StrEnum):
    """Provenance label for model knowledge. Never fabricate authority."""

    OFFICIAL = "official"
    REPOSITORY_DERIVED = "repository-derived"
    COMMUNITY_DERIVED = "community-derived"
    INFERRED = "inferred"
    EXPERIMENTAL = "experimental"
    UNVERIFIED = "unverified"


class Source(BaseModel):
    """A repository or origin that knowledge was derived from."""

    id: str
    name: str
    url: str
    kind: SourceKind = SourceKind.GITHUB
    license: str | None = None
    allowed_usage: str | None = None
    redistribution_status: str | None = None
    attribution_requirements: str | None = None
    description: str = ""
    last_checked: str | None = None
    notes: str = ""


class Prompt(BaseModel):
    """A single, attributed prompt.

    The only entity that may carry verbatim third-party text, and only when the license
    permits redistribution. Otherwise store metadata + source URL + derived analysis only.
    """

    id: str
    title: str
    original_prompt: str
    source_repo: str
    source_url: str | None = None
    author: str | None = None
    license: str | None = None
    target_model: str | None = None
    category: str = ""
    tags: list[str] = Field(default_factory=list)
    why_it_is_good: str = ""
    techniques_used: list[str] = Field(default_factory=list)
    visual_pattern: str | None = None
    style: str | None = None
    prompt_dna: str | None = None
    tier: PromptTier = PromptTier.ORIGINAL


class Case(BaseModel):
    """A complete, analyzed example. More than a prompt: full visual analysis + links."""

    id: str
    title: str
    category: str = ""
    use_case: str = ""
    user_intent: str = ""
    input_type: str = "text-to-image"
    reference_requirements: str = ""
    source: str | None = None
    model: str | None = None
    original_prompt: str = ""
    visual_intent: str = ""
    subject: str = ""
    environment: str = ""
    composition: str = ""
    lighting: str = ""
    camera: str = ""
    lens: str = ""
    perspective: str = ""
    style: str = ""
    color: str = ""
    materials: str = ""
    typography: str = ""
    layout: str = ""
    supporting_elements: list[str] = Field(default_factory=list)
    techniques: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    negative_constraints: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    pattern_ids: list[str] = Field(default_factory=list)
    style_ids: list[str] = Field(default_factory=list)
    technique_ids: list[str] = Field(default_factory=list)
    recipe_ids: list[str] = Field(default_factory=list)


class Recipe(BaseModel):
    """A method for completing a class of image task. The most valuable entity."""

    id: str
    name: str
    category: str = ""
    goal: str = ""
    description: str = ""
    required_inputs: list[str] = Field(default_factory=list)
    optional_inputs: list[str] = Field(default_factory=list)
    workflow: list[str] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    decision_points: list[str] = Field(default_factory=list)
    recommended_patterns: list[str] = Field(default_factory=list)
    recommended_styles: list[str] = Field(default_factory=list)
    recommended_techniques: list[str] = Field(default_factory=list)
    prompt_structure: list[str] = Field(default_factory=list)
    composition_guidance: str = ""
    text_guidance: str = ""
    constraints: list[str] = Field(default_factory=list)
    common_failures: list[str] = Field(default_factory=list)
    failure_recovery: list[str] = Field(default_factory=list)
    example_cases: list[str] = Field(default_factory=list)
    source_repositories: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    tags: list[str] = Field(default_factory=list)


class VisualPattern(BaseModel):
    """A reusable visual structure that works across products, brands, and subjects."""

    id: str
    name: str
    aliases: list[str] = Field(default_factory=list)
    category: str = ""
    description: str = ""
    visual_goal: str = ""
    best_for: list[str] = Field(default_factory=list)
    not_good_for: list[str] = Field(default_factory=list)
    composition: str = ""
    visual_hierarchy: str = ""
    subject_placement: str = ""
    foreground: str = ""
    midground: str = ""
    background: str = ""
    perspective: str = ""
    lighting_strategy: str = ""
    color_strategy: str = ""
    typography_strategy: str = ""
    negative_space_strategy: str = ""
    supporting_elements: list[str] = Field(default_factory=list)
    prompt_structure: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    common_failures: list[str] = Field(default_factory=list)
    related_styles: list[str] = Field(default_factory=list)
    related_techniques: list[str] = Field(default_factory=list)
    related_recipes: list[str] = Field(default_factory=list)
    example_cases: list[str] = Field(default_factory=list)
    source_repositories: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    tags: list[str] = Field(default_factory=list)


class Style(BaseModel):
    """A reusable visual system (aesthetic). Strictly separate from category."""

    id: str
    name: str
    aliases: list[str] = Field(default_factory=list)
    description: str = ""
    visual_characteristics: list[str] = Field(default_factory=list)
    composition_behavior: str = ""
    color_behavior: str = ""
    lighting_behavior: str = ""
    typography_behavior: str = ""
    material_behavior: str = ""
    texture_behavior: str = ""
    best_for: list[str] = Field(default_factory=list)
    avoid: list[str] = Field(default_factory=list)
    related_patterns: list[str] = Field(default_factory=list)
    related_techniques: list[str] = Field(default_factory=list)
    example_cases: list[str] = Field(default_factory=list)
    source_repositories: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class Technique(BaseModel):
    """A prompt-engineering lever that affects output quality."""

    id: str
    name: str
    category: str = ""
    description: str = ""
    problem_it_solves: str = ""
    pattern: str = ""
    implementation_guidance: str = ""
    when_to_use: list[str] = Field(default_factory=list)
    when_not_to_use: list[str] = Field(default_factory=list)
    good_examples: list[str] = Field(default_factory=list)
    bad_examples: list[str] = Field(default_factory=list)
    related_patterns: list[str] = Field(default_factory=list)
    related_recipes: list[str] = Field(default_factory=list)
    related_styles: list[str] = Field(default_factory=list)
    source_repositories: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    tags: list[str] = Field(default_factory=list)


class PromptDna(BaseModel):
    """A composable prompt structure unit — the smallest reusable building block."""

    id: str
    name: str
    category: str = ""
    description: str = ""
    components: list[str] = Field(default_factory=list)
    pattern: str = ""
    variables: list[str] = Field(default_factory=list)
    best_for: list[str] = Field(default_factory=list)
    related_patterns: list[str] = Field(default_factory=list)
    related_techniques: list[str] = Field(default_factory=list)
    related_styles: list[str] = Field(default_factory=list)
    source_families: list[str] = Field(default_factory=list)
    source_repositories: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    tags: list[str] = Field(default_factory=list)


class ModelKnowledge(BaseModel):
    """What a model can do, with a source_type label. Never an unverified claim."""

    id: str
    name: str
    family: str = ""
    provider: str = ""
    capabilities: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    text_rendering: str = ""
    consistency: str = ""
    editing: str = ""
    prompt_style_notes: str = ""
    source_type: SourceType = SourceType.UNVERIFIED
    source_references: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class Feature(BaseModel):
    """A product feature mined from a source repository."""

    name: str
    description: str = ""
    source_repo: str = ""
    source_url: str = ""
    why_it_is_good: str = ""
    user_value: str = ""
    implementation_complexity: str = "low"
    adoption_priority: str = "Later"
    should_museforge_adopt: bool = False
    how_museforge_can_improve_it: str = ""
    notes: str = ""


class CreativeDirection(BaseModel):
    """The designed plan produced by the Creative Director (the *output* entity)."""

    concept: str = ""
    goal: str = ""
    recommended_recipe: str | None = None
    recommended_pattern: str | None = None
    recommended_style: str | None = None
    visual_hierarchy: str = ""
    composition: str = ""
    subject_strategy: str = ""
    environment: str = ""
    perspective: str = ""
    lighting: str = ""
    color_palette: str = ""
    typography: str = ""
    supporting_elements: list[str] = Field(default_factory=list)
    negative_space: str = ""
    visual_density: str = ""
    constraints: list[str] = Field(default_factory=list)
    avoid: list[str] = Field(default_factory=list)
    rationale: str = ""


class Intent(BaseModel):
    """The result of intent analysis on a user request."""

    use_case: str = ""
    category: str = ""
    platform: str = ""
    aspect_ratio: str = ""
    priority: str = ""
    style: str = ""
    visual_density: str = ""
    likely_pattern: str = ""
    keywords: list[str] = Field(default_factory=list)
    language: str = "en"
    raw_request: str = ""


# Registry of entity models, used by the store and schema generator.
ENTITY_MODELS: dict[str, type[BaseModel]] = {
    "source": Source,
    "prompt": Prompt,
    "case": Case,
    "recipe": Recipe,
    "pattern": VisualPattern,
    "style": Style,
    "technique": Technique,
    "dna": PromptDna,
    "model": ModelKnowledge,
    "feature": Feature,
    "creative-direction": CreativeDirection,
}


def model_for(entity: str) -> type[BaseModel]:
    """Return the Pydantic model for a knowledge entity type."""
    try:
        return ENTITY_MODELS[entity]
    except KeyError as exc:  # pragma: no cover - defensive
        raise ValueError(f"Unknown entity type: {entity!r}") from exc


def validate_entity(entity: str, data: dict[str, Any]) -> BaseModel:
    """Validate a raw dict against the entity's model."""
    return model_for(entity).model_validate(data)

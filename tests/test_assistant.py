"""Assistant tests — routing, direction, composition, and optimization."""

from __future__ import annotations

from museforge.prompt_composer.composer import _BANNED
from museforge.services.assistant import MuseForgeAssistant


def test_intent_routing_xiaohongshu(assistant: MuseForgeAssistant) -> None:
    intent = assistant.understand_request("帮我做一张 AI 公司招聘小红书封面，3:4，极简，专业")
    assert intent.use_case == "recruitment marketing"
    assert intent.category == "social media poster"
    assert intent.platform == "Xiaohongshu"
    assert intent.aspect_ratio == "3:4"
    assert intent.style == "editorial minimalism"


def test_intent_routing_fintech(assistant: MuseForgeAssistant) -> None:
    intent = assistant.understand_request("Create a premium fintech card advertisement")
    assert intent.use_case == "fintech marketing"
    assert intent.category == "product advertisement"


def test_recipe_matching(assistant: MuseForgeAssistant) -> None:
    resp = assistant.generate_response("Create a premium fintech card advertisement")
    assert resp.recommended_recipe is not None
    assert resp.recommended_recipe.name == "Fintech Card Ad"


def test_pattern_matching(assistant: MuseForgeAssistant) -> None:
    resp = assistant.generate_response("Create a clean SaaS AI product hero visual")
    assert resp.recommended_pattern is not None
    assert resp.recommended_pattern.name == "Minimal SaaS Illustration"


def test_style_matching(assistant: MuseForgeAssistant) -> None:
    resp = assistant.generate_response("Create a realistic cinematic character portrait")
    assert resp.recommended_style is not None
    assert resp.recommended_style.name == "cinematic realism"


def test_creative_direction_has_rationale(assistant: MuseForgeAssistant) -> None:
    resp = assistant.generate_response("Create a premium fintech card advertisement")
    assert resp.creative_direction.rationale
    assert resp.creative_direction.recommended_recipe == "recipe-fintech-card-ad"


def test_prompt_composition_no_banned_adjectives(assistant: MuseForgeAssistant) -> None:
    resp = assistant.generate_response("Create a premium fintech card advertisement")
    low = resp.super_prompt.lower()
    for word in _BANNED:
        assert word not in low, f"banned adjective {word!r} leaked into the prompt"


def test_prompt_composition_is_structured(assistant: MuseForgeAssistant) -> None:
    resp = assistant.generate_response("Create a premium fintech card advertisement")
    assert "Product:" in resp.super_prompt
    assert "Lighting:" in resp.super_prompt


def test_model_optimization_basis_label(assistant: MuseForgeAssistant) -> None:
    resp = assistant.generate_response("Create a premium fintech card advertisement", model="nano-banana-pro")
    assert resp.model_variant is not None
    assert resp.model_variant.optimization_basis in {"repository-derived", "community-derived", "heuristic"}


def test_prompt_only_mode(assistant: MuseForgeAssistant) -> None:
    resp = assistant.generate_response("Create a premium fintech card advertisement", prompt_only=True)
    assert resp.super_prompt


def test_techniques_prioritize_recipe(assistant: MuseForgeAssistant) -> None:
    resp = assistant.generate_response("帮我做一张 AI 公司招聘小红书封面，3:4，极简")
    names = [t.name for t in resp.key_techniques]
    assert "text rendering" in names
    assert "visual hierarchy" in names

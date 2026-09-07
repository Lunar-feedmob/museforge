"""Retrieval tests — search must surface the right knowledge."""

from __future__ import annotations

from museforge.knowledge.models import Recipe, VisualPattern
from museforge.retrieval.retrievers import (
    PatternRetriever,
    RecipeRetriever,
    StyleRetriever,
    TechniqueRetriever,
)


def test_recipe_search_poster(store) -> None:
    results = RecipeRetriever(store).search("poster")
    top = [r.name for r, _ in results if isinstance(r, Recipe)]
    assert "Editorial Poster" in top[:2]


def test_pattern_search_product_hero(store) -> None:
    results = PatternRetriever(store).search("product hero")
    top = [p.name for p, _ in results if isinstance(p, VisualPattern)]
    assert "Breakout Product Hero" in top[:2]


def test_style_search_editorial(store) -> None:
    results = StyleRetriever(store).search("editorial")
    top = [s.name for s, _ in results]
    assert "editorial minimalism" in top[:3]


def test_technique_search_text_rendering(store) -> None:
    results = TechniqueRetriever(store).search("text rendering")
    top = [t.name for t, _ in results]
    assert "text rendering" in top[:2]


def test_get_by_id(store) -> None:
    recipe = RecipeRetriever(store).get("recipe-product-hero-ad")
    assert recipe is not None
    assert recipe.name == "Product Hero Ad"


def test_get_missing_returns_none(store) -> None:
    assert RecipeRetriever(store).get("does-not-exist") is None

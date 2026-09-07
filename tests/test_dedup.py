"""Deduplication tests across the five levels."""

from __future__ import annotations

from museforge.dedup.dedup import Deduplicator, visual_intent_key
from museforge.dedup.similarity import edit_distance, jaccard, ngram_similarity, token_similarity


def test_exact_dedup() -> None:
    items = ["a product hero", "a product hero", "other"]
    result = Deduplicator().dedup(items, level="exact")
    assert len(result.kept) == 2
    assert result.removed == 1


def test_normalized_dedup_ignores_case_and_markdown() -> None:
    items = ["**A** product", "a product", "A PRODUCT"]
    result = Deduplicator().dedup(items, level="normalized")
    assert len(result.kept) == 1


def test_near_dedup_typo() -> None:
    items = ["a product hero advertisement", "a product hero advertisment"]
    result = Deduplicator().dedup(items, level="near")
    assert len(result.kept) == 1


class _MockEmbedding:
    """Controlled embeddings: identical text -> identical vector, different -> orthogonal."""

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[1.0, 0.0] if "dark water" in t else [0.0, 1.0] for t in texts]


def test_semantic_dedup() -> None:
    items = ["a luxury product on dark water", "a luxury product on dark water with flowers"]
    result = Deduplicator(embedding=_MockEmbedding()).dedup(items, level="semantic")
    assert len(result.kept) == 1


def test_semantic_dedup_keeps_distinct() -> None:
    items = ["a luxury product on dark water", "a flat vector illustration"]
    result = Deduplicator(embedding=_MockEmbedding()).dedup(items, level="semantic")
    assert len(result.kept) == 2


def test_visual_intent_dedup_aggregates_similar_cases() -> None:
    a = {"subject": "card", "composition": "centered", "lighting": "golden", "style": "luxury", "camera": "", "environment": "water"}
    b = {"subject": "card", "composition": "centered", "lighting": "golden", "style": "luxury", "camera": "", "environment": "water"}
    c = {"subject": "bottle", "composition": "breakout", "lighting": "rim", "style": "luxury", "camera": "", "environment": "gradient"}
    result = Deduplicator().dedup([a, b, c], level="visual-intent")
    assert len(result.kept) == 2
    assert len(result.clusters) == 2


def test_visual_intent_key() -> None:
    assert visual_intent_key({"subject": "X", "composition": "Y"}) == ("x", "y", "", "", "", "")


def test_similarity_measures() -> None:
    assert jaccard(["a", "b"], ["a", "b"]) == 1.0
    assert jaccard(["a"], ["b"]) == 0.0
    assert token_similarity("a b c", "a b c") == 1.0
    assert ngram_similarity("product", "product") == 1.0
    assert edit_distance("kitten", "sitting") == 3

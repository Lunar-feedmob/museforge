"""Deduplication across five levels.

1. **Exact** — identical text.
2. **Normalized** — identical after normalization (markdown/URL/whitespace stripped).
3. **Near** — Jaccard / token / n-gram / edit-distance similarity above a threshold.
4. **Semantic** — embedding cosine similarity (via an ``EmbeddingProvider``).
5. **Visual intent** — same subject/composition/lighting/style/camera/environment even when the
   text differs. This is the most important level: near-duplicate visual intents are aggregated
   into one Pattern/Recipe/Family, keeping important variants.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from museforge.dedup.similarity import (
    edit_similarity,
    ngram_similarity,
    token_similarity,
)
from museforge.normalizers.text import normalize
from museforge.providers.embeddings import EmbeddingProvider, LocalEmbeddingProvider, cosine

# Fields that define a "visual intent" for aggregation.
VISUAL_INTENT_FIELDS = ("subject", "composition", "lighting", "style", "camera", "environment")


@dataclass
class DedupResult:
    """The outcome of a dedup pass: kept items and the clusters they were grouped into."""

    kept: list[Any] = field(default_factory=list)
    clusters: list[list[Any]] = field(default_factory=list)
    removed: int = 0


def _text_of(item: Any) -> str:
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        return str(item.get("original_prompt") or item.get("text") or item.get("prompt") or "")
    return str(getattr(item, "original_prompt", "") or getattr(item, "text", "") or "")


def visual_intent_key(item: Any) -> tuple[str, ...]:
    """A stable key for visual-intent aggregation from a case-like object."""
    if isinstance(item, dict):
        return tuple(str(item.get(f, "")).strip().lower() for f in VISUAL_INTENT_FIELDS)
    return tuple(str(getattr(item, f, "")).strip().lower() for f in VISUAL_INTENT_FIELDS)


class Deduplicator:
    """Deduplicates a list of items at a configurable level."""

    def __init__(
        self,
        *,
        near_threshold: float = 0.85,
        semantic_threshold: float = 0.9,
        embedding: EmbeddingProvider | None = None,
    ) -> None:
        self.near_threshold = near_threshold
        self.semantic_threshold = semantic_threshold
        self.embedding = embedding or LocalEmbeddingProvider()

    def dedup(self, items: list[Any], level: str = "normalized") -> DedupResult:
        """Deduplicate items at the given level.

        ``level`` is one of: exact, normalized, near, semantic, visual-intent.
        """
        if level == "exact":
            return self._dedup_by(items, lambda i: _text_of(i))
        if level == "normalized":
            return self._dedup_by(items, lambda i: normalize(_text_of(i)))
        if level == "near":
            return self._dedup_near(items)
        if level == "semantic":
            return self._dedup_semantic(items)
        if level == "visual-intent":
            return self._dedup_by(items, visual_intent_key)
        raise ValueError(f"Unknown dedup level: {level!r}")

    # -- helpers ---------------------------------------------------------

    def _dedup_by(self, items: list[Any], key: Callable[[Any], Any]) -> DedupResult:
        seen: dict[Any, int] = {}
        kept: list[Any] = []
        clusters: list[list[Any]] = []
        for item in items:
            k = key(item)
            if k in seen:
                clusters[seen[k]].append(item)
            else:
                seen[k] = len(clusters)
                clusters.append([item])
                kept.append(item)
        return DedupResult(kept=kept, clusters=clusters, removed=len(items) - len(kept))

    def _dedup_near(self, items: list[Any]) -> DedupResult:
        kept: list[Any] = []
        clusters: list[list[Any]] = []
        for item in items:
            text = normalize(_text_of(item))
            placed = False
            for cluster in clusters:
                rep = normalize(_text_of(cluster[0]))
                if self._near_similar(text, rep) >= self.near_threshold:
                    cluster.append(item)
                    placed = True
                    break
            if not placed:
                clusters.append([item])
                kept.append(item)
        return DedupResult(kept=kept, clusters=clusters, removed=len(items) - len(kept))

    def _near_similar(self, a: str, b: str) -> float:
        if not a and not b:
            return 1.0
        if not a or not b:
            return 0.0
        return max(
            token_similarity(a, b),
            ngram_similarity(a, b),
            edit_similarity(a, b),
        )

    def _dedup_semantic(self, items: list[Any]) -> DedupResult:
        texts = [normalize(_text_of(i)) for i in items]
        vectors = self.embedding.embed(texts)
        kept: list[Any] = []
        clusters: list[list[Any]] = []
        for i, item in enumerate(items):
            placed = False
            for cluster in clusters:
                if cosine(vectors[i], vectors[kept.index(cluster[0])]) >= self.semantic_threshold:
                    cluster.append(item)
                    placed = True
                    break
            if not placed:
                clusters.append([item])
                kept.append(item)
        return DedupResult(kept=kept, clusters=clusters, removed=len(items) - len(kept))

"""Deduplication (exact / normalized / near / semantic / visual-intent)."""

from museforge.dedup.dedup import Deduplicator, DedupResult, visual_intent_key
from museforge.dedup.similarity import (
    edit_distance,
    edit_similarity,
    jaccard,
    ngram_similarity,
    token_similarity,
)

__all__ = [
    "DedupResult",
    "Deduplicator",
    "edit_distance",
    "edit_similarity",
    "jaccard",
    "ngram_similarity",
    "token_similarity",
    "visual_intent_key",
]

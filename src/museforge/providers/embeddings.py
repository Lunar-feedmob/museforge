"""Embedding providers.

MuseForge is embedding-agnostic: the retrieval and dedup layers depend on the
``EmbeddingProvider`` protocol, never on a specific vendor. V0 ships a deterministic local
provider (hashed n-gram bag) so semantic dedup/search work with no API key.
"""

from __future__ import annotations

import hashlib
import math
from typing import Protocol

from museforge.normalizers.text import ngrams, tokenize


class EmbeddingProvider(Protocol):
    """A provider that turns texts into dense vectors."""

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text."""
        ...


class LocalEmbeddingProvider:
    """Deterministic, dependency-free embedding via hashed character n-grams.

    Not a real semantic model, but a stable, offline baseline that captures lexical overlap
    and is robust to CJK. Swap in a real model (OpenAI, sentence-transformers, …) behind the
    same interface when available.
    """

    def __init__(self, dim: int = 256) -> None:
        self.dim = dim

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_one(t) for t in texts]

    def _embed_one(self, text: str) -> list[float]:
        vec = [0.0] * self.dim
        for gram in ngrams(tokenize(text), 3):
            idx = int(hashlib.md5(gram.encode("utf-8")).hexdigest(), 16) % self.dim
            vec[idx] += 1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]


def cosine(a: list[float], b: list[float]) -> float:
    """Cosine similarity between two vectors."""
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)

"""Similarity measures for near-duplicate detection."""

from __future__ import annotations

from collections.abc import Iterable

from museforge.normalizers.text import ngrams, tokenize


def jaccard(a: Iterable[str], b: Iterable[str]) -> float:
    """Jaccard similarity over two token/ngram sets."""
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def token_similarity(a: str, b: str) -> float:
    """Jaccard over word tokens."""
    return jaccard(tokenize(a), tokenize(b))


def ngram_similarity(a: str, b: str, n: int = 3) -> float:
    """Jaccard over character n-grams (robust to CJK and typos)."""
    return jaccard(ngrams(tokenize(a), n), ngrams(tokenize(b), n))


def edit_distance(a: str, b: str) -> int:
    """Levenshtein edit distance (iterative, O(n*m) memory-optimized)."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        cur = [i]
        for j, cb in enumerate(b, start=1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def edit_similarity(a: str, b: str) -> float:
    """Normalized edit similarity in [0, 1]."""
    if not a and not b:
        return 1.0
    dist = edit_distance(a, b)
    return 1.0 - dist / max(len(a), len(b))

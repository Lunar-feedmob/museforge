"""Search backends: metadata + BM25/fuzzy scoring.

V0 ships a dependency-free BM25-lite scorer over entity fields. The embedding layer is reserved
behind the ``EmbeddingProvider`` interface (see ``providers/embeddings.py``) for V1 semantic
search.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Any

from museforge.normalizers.text import ngrams, tokenize


class BM25:
    """A compact BM25 scorer over a corpus of documents."""

    def __init__(self, docs: list[list[str]], *, k1: float = 1.5, b: float = 0.75) -> None:
        self.docs = docs
        self.k1 = k1
        self.b = b
        self.n = len(docs)
        self.doc_len = [len(d) for d in docs]
        self.avgdl = sum(self.doc_len) / self.n if self.n else 0.0
        self.df: Counter[str] = Counter()
        for d in docs:
            self.df.update(set(d))

    def idf(self, term: str) -> float:
        n_t = self.df.get(term, 0)
        return math.log(1 + (self.n - n_t + 0.5) / (n_t + 0.5))

    def score(self, query_terms: list[str], doc: list[str]) -> float:
        if not doc:
            return 0.0
        tf = Counter(doc)
        dl = len(doc)
        total = 0.0
        for term in query_terms:
            if term not in tf:
                continue
            f = tf[term]
            denom = f + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            total += self.idf(term) * f * (self.k1 + 1) / denom
        return total


def _entity_text(entity: Any) -> str:
    """Concatenate the searchable text fields of an entity."""
    parts: list[str] = []
    for field in (
        "name", "title", "description", "goal", "category", "use_case", "visual_goal",
        "problem_it_solves", "concept", "original_prompt", "subject", "environment",
        "composition", "lighting", "style", "typography", "best_for", "not_good_for",
    ):
        val = getattr(entity, field, None)
        if isinstance(val, str) and val:
            parts.append(val)
        elif isinstance(val, list):
            parts.extend(str(v) for v in val)
    return " ".join(parts)


def _entity_metadata(entity: Any) -> str:
    """Concatenate the high-signal metadata fields (category/style/tags/aliases)."""
    parts: list[str] = []
    for field in ("category", "style", "use_case", "platform", "aliases", "tags"):
        val = getattr(entity, field, None)
        if isinstance(val, str) and val:
            parts.append(val)
        elif isinstance(val, list):
            parts.extend(str(v) for v in val)
    return " ".join(parts)


class Retriever:
    """Retrieves entities by scoring them against a query.

    Scoring combines:
    - **metadata match** (category/style/tags/aliases) — high weight, exact-ish.
    - **BM25** over the entity's text fields.
    - **fuzzy n-gram** overlap as a tiebreaker for CJK/typos.
    """

    def __init__(self, entities: list[Any]) -> None:
        self.entities = entities
        self.bm25 = BM25([tokenize(_entity_text(e)) for e in entities])

    def search(self, query: str, top_k: int = 5) -> list[tuple[Any, float]]:
        q_terms = tokenize(query)
        if not q_terms:
            return [(e, 0.0) for e in self.entities[:top_k]]
        q_grams = ngrams(q_terms, 3)
        scored: list[tuple[Any, float]] = []
        for i, entity in enumerate(self.entities):
            meta = tokenize(_entity_metadata(entity))
            meta_hits = sum(1 for t in q_terms if t in meta)
            meta_score = meta_hits / max(len(q_terms), 1)
            bm25_score = self.bm25.score(q_terms, self.bm25.docs[i])
            fuzzy = len(q_grams & ngrams(tokenize(_entity_text(entity)), 3)) / max(len(q_grams), 1)
            total = 3.0 * meta_score + bm25_score + 0.5 * fuzzy
            scored.append((entity, total))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def get(self, ident: str) -> Any | None:
        for e in self.entities:
            if getattr(e, "id", None) == ident or getattr(e, "name", None) == ident:
                return e
        return None

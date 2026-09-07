"""Text normalization for prompts and knowledge content.

Normalization strips the noise that makes two semantically-identical prompts look different:
markdown, URLs, author intros, invalid wrappers, duplicate whitespace, and Unicode variants.
"""

from __future__ import annotations

import re
import unicodedata

_URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
_MARKDOWN_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_MARKDOWN_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
_MARKDOWN_HEADING_RE = re.compile(r"^#{1,6}\s+", re.MULTILINE)
_MARKDOWN_EMPHASIS_RE = re.compile(r"(\*\*|__|\*|_|~~|`)(.*?)\1")
_WHITESPACE_RE = re.compile(r"\s+")
_HTML_TAG_RE = re.compile(r"<[^>]+>")


def strip_markdown(text: str) -> str:
    """Remove markdown syntax, keeping the inner text."""
    text = _MARKDOWN_CODE_RE.sub(" ", text)
    text = _MARKDOWN_LINK_RE.sub(r"\1", text)
    text = _MARKDOWN_HEADING_RE.sub("", text)
    text = _MARKDOWN_EMPHASIS_RE.sub(r"\2", text)
    text = _HTML_TAG_RE.sub(" ", text)
    return text


def strip_urls(text: str) -> str:
    return _URL_RE.sub(" ", text)


def normalize_unicode(text: str) -> str:
    return unicodedata.normalize("NFKC", text)


def collapse_whitespace(text: str) -> str:
    return _WHITESPACE_RE.sub(" ", text).strip()


def normalize(text: str) -> str:
    """Full normalization: unicode → strip markdown/urls → collapse whitespace → lowercase."""
    text = normalize_unicode(text)
    text = strip_markdown(text)
    text = strip_urls(text)
    text = collapse_whitespace(text)
    return text.lower()


def tokenize(text: str) -> list[str]:
    """Tokenize normalized text into lowercase word tokens."""
    return [t for t in re.split(r"[^a-z0-9一-鿿]+", normalize(text)) if t]


def ngrams(tokens: list[str], n: int = 3) -> set[str]:
    """Character n-grams for fuzzy matching (robust to CJK and typos)."""
    joined = "".join(tokens)
    if len(joined) < n:
        return {joined}
    return {joined[i : i + n] for i in range(len(joined) - n + 1)}

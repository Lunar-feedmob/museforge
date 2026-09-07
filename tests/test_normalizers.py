"""Normalization tests."""

from __future__ import annotations

from museforge.normalizers.text import (
    ngrams,
    normalize,
    strip_markdown,
    strip_urls,
    tokenize,
)


def test_strip_markdown_link() -> None:
    assert strip_markdown("[text](https://x.com)") == "text"


def test_strip_markdown_emphasis() -> None:
    assert strip_markdown("**bold** and *italic*") == "bold and italic"


def test_strip_urls() -> None:
    result = strip_urls("see https://example.com/x now")
    assert "example.com" not in result
    assert "see" in result and "now" in result


def test_normalize_collapses_whitespace_and_case() -> None:
    assert normalize("  A   B\nC  ") == "a b c"


def test_normalize_strips_markdown_and_urls() -> None:
    assert normalize("**Hi** [there](https://x.com)") == "hi there"


def test_tokenize_cjk() -> None:
    tokens = tokenize("招聘 AI 工程师")
    assert "ai" in tokens
    assert "招聘" in tokens


def test_ngrams_short_text() -> None:
    assert ngrams(["ab"], 3) == {"ab"}

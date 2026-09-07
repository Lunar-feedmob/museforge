"""Parsers that turn raw repository content into raw records.

Parsers are format-specific (markdown, JSON, HTML). They produce *raw* dicts; the analyzers
and extractors turn raw dicts into typed knowledge entities.
"""

from __future__ import annotations

import json
import re
from typing import Any, Protocol


class Parser(Protocol):
    """A parser that turns raw text into a list of raw records."""

    def parse(self, text: str) -> list[dict[str, Any]]:
        ...


class JsonCaseParser:
    """Parse a JSON array of structured case objects (e.g. freestylefly's case format)."""

    def parse(self, text: str) -> list[dict[str, Any]]:
        data = json.loads(text)
        if isinstance(data, list):
            return [d for d in data if isinstance(d, dict)]
        if isinstance(data, dict):
            for key in ("cases", "results", "items", "data"):
                if isinstance(data.get(key), list):
                    return [d for d in data[key] if isinstance(d, dict)]
        return []


_HEADING_RE = re.compile(r"^#{1,6}\s+(.*)$", re.MULTILINE)
_FIELD_RE = re.compile(r"^\s*([A-Za-z_ ]+?)\s*[:：]\s*(.*)$")


class MarkdownCaseParser:
    """Parse markdown case files into raw records.

    Recognizes ``### Title`` as a case boundary and ``Field: value`` lines as fields. A
    ``Prompt:`` field (or a fenced code block) is treated as the prompt text.
    """

    def parse(self, text: str) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        current: dict[str, Any] | None = None
        in_code = False
        code_buf: list[str] = []

        def flush() -> None:
            nonlocal current
            if current is not None:
                if code_buf and not current.get("prompt"):
                    current["prompt"] = "\n".join(code_buf).strip()
                records.append(current)
            current = None
            code_buf.clear()

        for line in text.splitlines():
            if line.strip().startswith("```"):
                if in_code:
                    in_code = False
                else:
                    in_code = True
                    code_buf = []
                continue
            if in_code:
                code_buf.append(line)
                continue
            m = _HEADING_RE.match(line)
            if m:
                flush()
                current = {"title": m.group(1).strip()}
                continue
            if current is not None:
                fm = _FIELD_RE.match(line)
                if fm:
                    key = fm.group(1).strip().lower().replace(" ", "_")
                    val = fm.group(2).strip()
                    if key in current:
                        current[key] = f"{current[key]}\n{val}"
                    else:
                        current[key] = val
        flush()
        return records

"""Repository collectors.

A collector fetches raw content from a source repository (a local directory or a remote URL).
V0 collects a *curated subset*, not a full scrape — the goal is to validate the knowledge
model, not to ingest everything.
"""

from __future__ import annotations

import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass
class CollectedContent:
    """Raw content collected from a source."""

    source_id: str
    source_url: str
    files: dict[str, str]  # relative path -> text content


class Collector(Protocol):
    """A collector that fetches raw content from a source."""

    def collect(self, source_id: str, source_url: str) -> CollectedContent:
        ...


class LocalDirectoryCollector:
    """Read files from a local directory (for offline ingestion)."""

    def __init__(self, suffixes: tuple[str, ...] = (".md", ".json", ".jsonl", ".txt")) -> None:
        self.suffixes = suffixes

    def collect(self, source_id: str, source_url: str) -> CollectedContent:
        root = Path(source_url)
        files: dict[str, str] = {}
        if root.is_dir():
            for path in sorted(root.rglob("*")):
                if path.is_file() and path.suffix in self.suffixes:
                    files[str(path.relative_to(root))] = path.read_text(encoding="utf-8", errors="replace")
        return CollectedContent(source_id=source_id, source_url=source_url, files=files)


class UrlCollector:
    """Fetch a single remote URL (best-effort; many repos are better cloned locally)."""

    def collect(self, source_id: str, source_url: str) -> CollectedContent:
        try:
            with urllib.request.urlopen(source_url, timeout=20) as resp:  # noqa: S310
                text = resp.read().decode("utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001 - network is best-effort
            text = f"# fetch failed: {exc}"
        return CollectedContent(source_id=source_id, source_url=source_url, files={source_url: text})

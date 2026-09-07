"""KnowledgeStore — typed access to the JSON/JSONL knowledge base.

V0 uses plain JSON/JSONL on disk (no database). The store is a thin, typed access layer so a
real database can replace it later without touching the service or retrieval layers.

Layout::

    data/
      sources/     source.json, ...
      prompts/     prompt.json, ...
      cases/       case.json, ...
      recipes/     recipe.json, ...
      patterns/    pattern.json, ...
      styles/      style.json, ...
      techniques/  technique.json, ...
      dna/         dna.json, ...
      models/      model.json, ...
      features/    features.json   (a single JSON array)

Each entity directory holds ``*.json`` files (one entity per file) and/or ``*.jsonl`` files
(one entity per line). ``features.json`` is a single JSON array (see ``data/features/``).
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from museforge.knowledge.models import ENTITY_MODELS, model_for

# Entity types whose data lives as a single JSON array file (not a directory of entities).
_ARRAY_ENTITIES = {"feature"}

# Singular entity key -> plural on-disk directory name (matches the spec's data/ layout).
_DIR_NAMES = {
    "source": "sources",
    "prompt": "prompts",
    "case": "cases",
    "recipe": "recipes",
    "pattern": "patterns",
    "style": "styles",
    "technique": "techniques",
    "dna": "dna",
    "model": "models",
    "feature": "features",
    "creative-direction": "creative-directions",
}


class KnowledgeStore:
    """Loads and saves knowledge entities from a data directory."""

    def __init__(self, data_dir: str | Path = "data") -> None:
        self.data_dir = Path(data_dir)

    # -- paths -----------------------------------------------------------

    def entity_dir(self, entity: str) -> Path:
        return self.data_dir / _DIR_NAMES.get(entity, entity)

    def _iter_files(self, entity: str) -> Iterator[Path]:
        d = self.entity_dir(entity)
        if not d.is_dir():
            return
        for path in sorted(d.iterdir()):
            if path.suffix in {".json", ".jsonl"}:
                yield path

    # -- loading ---------------------------------------------------------

    def load(self, entity: str) -> list[BaseModel]:
        """Load all entities of a type, validated against the model."""
        model = model_for(entity)
        out: list[BaseModel] = []
        if entity in _ARRAY_ENTITIES:
            for data in self._load_array(entity):
                out.append(model.model_validate(data))
            return out
        for path in self._iter_files(entity):
            out.extend(self._load_file(path, model))
        return out

    def _load_array(self, entity: str) -> list[dict[str, Any]]:
        dir_name = _DIR_NAMES.get(entity, entity)
        path = self.entity_dir(entity) / f"{dir_name}.json"
        if not path.is_file():
            return []
        raw = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(raw, list):
            return raw
        if isinstance(raw, dict):
            for key in (entity, dir_name):
                if key in raw:
                    value = raw[key]
                    return value if isinstance(value, list) else []
        return []

    def _load_file(self, path: Path, model: type[BaseModel]) -> list[BaseModel]:
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".jsonl":
            return [model.model_validate(json.loads(line)) for line in text.splitlines() if line.strip()]
        data = json.loads(text)
        if isinstance(data, list):
            return [model.model_validate(item) for item in data]
        return [model.model_validate(data)]

    # -- saving ----------------------------------------------------------

    def save(self, entity: str, items: list[BaseModel]) -> None:
        """Save entities of a type (one JSON file per entity)."""
        d = self.entity_dir(entity)
        d.mkdir(parents=True, exist_ok=True)
        for item in items:
            data = item.model_dump(mode="json")
            ident = getattr(item, "id", None) or getattr(item, "name", None) or "item"
            safe = str(ident).replace("/", "_").replace("\\", "_")
            (d / f"{safe}.json").write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )

    # -- convenience -----------------------------------------------------

    def get(self, entity: str, ident: str) -> BaseModel | None:
        for item in self.load(entity):
            if getattr(item, "id", None) == ident or getattr(item, "name", None) == ident:
                return item
        return None

    def stats(self) -> dict[str, int]:
        return {entity: len(self.load(entity)) for entity in ENTITY_MODELS}

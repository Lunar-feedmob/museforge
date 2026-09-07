"""Generate JSON schemas from the Pydantic models.

Run from the repo root:  python scripts/generate_schemas.py

This keeps ``schemas/*.schema.json`` in lockstep with ``src/museforge/knowledge/models.py``.
"""

from __future__ import annotations

import json
from pathlib import Path

from museforge.knowledge.models import ENTITY_MODELS

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"


def main() -> None:
    SCHEMAS_DIR.mkdir(parents=True, exist_ok=True)
    for name, model in ENTITY_MODELS.items():
        schema = model.model_json_schema()
        # Pydantic emits a $defs section for enums; keep it self-contained.
        path = SCHEMAS_DIR / f"{name}.schema.json"
        path.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {path.relative_to(SCHEMAS_DIR.parent)}")


if __name__ == "__main__":
    main()

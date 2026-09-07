"""Knowledge linker — cross-reference entities by explicit IDs.

Links are explicit IDs (``pattern_ids``, ``style_ids``, …), not inferred similarity. This is
what makes MuseForge's recommendations explainable. The linker validates forward references
and builds reverse links (e.g. which cases instantiate a given pattern).
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any


def build_reverse_links(cases: list[Any]) -> dict[str, dict[str, list[str]]]:
    """Build reverse links from cases to the abstractions they reference.

    Returns ``{entity_type: {entity_id: [case_id, ...]}}``.
    """
    reverse: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for case in cases:
        cid = getattr(case, "id", "")
        for field, entity in (
            ("pattern_ids", "pattern"),
            ("style_ids", "style"),
            ("technique_ids", "technique"),
            ("recipe_ids", "recipe"),
        ):
            for ref in getattr(case, field, []) or []:
                reverse[entity][ref].append(cid)
    return {k: dict(v) for k, v in reverse.items()}


def validate_links(cases: list[Any], known_ids: dict[str, set[str]]) -> list[str]:
    """Return a list of dangling references (case → missing entity id)."""
    dangling: list[str] = []
    for case in cases:
        cid = getattr(case, "id", "")
        for field, entity in (
            ("pattern_ids", "pattern"),
            ("style_ids", "style"),
            ("technique_ids", "technique"),
            ("recipe_ids", "recipe"),
        ):
            for ref in getattr(case, field, []) or []:
                if ref not in known_ids.get(entity, set()):
                    dangling.append(f"{cid} -> {entity}:{ref}")
    return dangling

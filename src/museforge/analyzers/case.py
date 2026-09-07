"""Case analysis — decompose a raw case into its visual fields.

The CaseAnalyzer turns a raw prompt/case into a structured Case (subject, environment,
composition, lighting, camera, style, …). With an LLM it does a full decomposition; without
one it produces a best-effort Case from whatever fields the raw record already carries.
"""

from __future__ import annotations

from typing import Any

from museforge.knowledge.models import Case
from museforge.providers.llm import LLMProvider


class CaseAnalyzer:
    """Analyze a raw case record into a structured Case."""

    def __init__(self, llm: LLMProvider | None = None) -> None:
        self.llm = llm

    def analyze(self, raw: dict[str, Any], *, case_id: str | None = None) -> Case:
        if self.llm is not None:
            try:
                return self._llm_analyze(raw, case_id)
            except Exception:  # noqa: BLE001 - fall back to passthrough
                pass
        return self._passthrough(raw, case_id)

    def _passthrough(self, raw: dict[str, Any], case_id: str | None) -> Case:
        """Best-effort Case from whatever fields the raw record already carries."""
        ident = case_id or str(raw.get("id") or raw.get("title") or "case")
        return Case(
            id=ident,
            title=str(raw.get("title") or ident),
            category=str(raw.get("category") or ""),
            use_case=str(raw.get("use_case") or raw.get("scene") or ""),
            source=str(raw.get("source_repo") or raw.get("source") or ""),
            model=str(raw.get("model") or raw.get("target_model") or ""),
            original_prompt=str(raw.get("prompt") or raw.get("original_prompt") or ""),
            subject=str(raw.get("subject") or ""),
            environment=str(raw.get("environment") or ""),
            composition=str(raw.get("composition") or ""),
            lighting=str(raw.get("lighting") or ""),
            camera=str(raw.get("camera") or ""),
            lens=str(raw.get("lens") or ""),
            perspective=str(raw.get("perspective") or ""),
            style=str(raw.get("style") or ""),
            color=str(raw.get("color") or ""),
            typography=str(raw.get("typography") or ""),
            layout=str(raw.get("layout") or ""),
            tags=[str(t) for t in raw.get("tags", [])] if isinstance(raw.get("tags"), list) else [],
            techniques=[str(t) for t in raw.get("techniques", [])] if isinstance(raw.get("techniques"), list) else [],
        )

    def _llm_analyze(self, raw: dict[str, Any], case_id: str | None) -> Case:
        assert self.llm is not None
        system = (
            "You analyze an image-generation prompt. Respond with ONLY a JSON object with keys: "
            "subject, environment, composition, lighting, camera, lens, perspective, style, color, "
            "materials, typography, layout, visual_intent, techniques (array), constraints (array), "
            "negative_constraints (array). Use empty strings/arrays when unknown."
        )
        import json

        data = json.loads(self.llm.complete(str(raw.get("prompt", "")), system=system))
        base = self._passthrough(raw, case_id)
        for field in (
            "subject", "environment", "composition", "lighting", "camera", "lens",
            "perspective", "style", "color", "materials", "typography", "layout", "visual_intent",
        ):
            setattr(base, field, str(data.get(field, "")))
        for field in ("techniques", "constraints", "negative_constraints"):
            val = data.get(field, [])
            if isinstance(val, list):
                setattr(base, field, [str(v) for v in val])
        return base

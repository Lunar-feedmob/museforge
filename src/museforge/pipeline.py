"""The background knowledge pipeline.

Repository Discovery → Collector → Parser → Normalizer → License/Attribution Check →
Deduplicator → Case Analyzer → Prompt Analyzer → Recipe/Pattern/Style/Technique/DNA
Extractors → Knowledge Linker → Knowledge Store.

This is a *background* capability. It is not the user-facing product.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from museforge.analyzers.case import CaseAnalyzer
from museforge.collectors.base import Collector, LocalDirectoryCollector
from museforge.dedup.dedup import Deduplicator
from museforge.knowledge.models import Case, Prompt, Source
from museforge.knowledge.store import KnowledgeStore
from museforge.licensing.license import decide
from museforge.parsers.base import JsonCaseParser, Parser
from museforge.providers.llm import LLMProvider


@dataclass
class IngestReport:
    """Summary of an ingestion run."""

    source_id: str
    files_read: int = 0
    records_parsed: int = 0
    prompts_kept: int = 0
    prompts_skipped_license: int = 0
    duplicates_removed: int = 0
    cases_stored: int = 0
    errors: list[str] = field(default_factory=list)


class IngestionPipeline:
    """Orchestrates the ingestion of a source repository into the knowledge store."""

    def __init__(
        self,
        store: KnowledgeStore,
        *,
        collector: Collector | None = None,
        parser: Parser | None = None,
        llm: LLMProvider | None = None,
    ) -> None:
        self.store = store
        self.collector = collector or LocalDirectoryCollector()
        self.parser = parser or JsonCaseParser()
        self.dedup = Deduplicator()
        self.case_analyzer = CaseAnalyzer(llm)

    def ingest(self, source_id: str, source_url: str, *, license: str | None = None) -> IngestReport:
        report = IngestReport(source_id=source_id)
        content = self.collector.collect(source_id, source_url)
        report.files_read = len(content.files)

        decision = decide(license)
        raw_records: list[dict[str, Any]] = []
        for path, text in content.files.items():
            try:
                raw_records.extend(self.parser.parse(text))
            except Exception as exc:  # noqa: BLE001 - one bad file shouldn't kill the run
                report.errors.append(f"{path}: {exc}")

        report.records_parsed = len(raw_records)

        # License check: only keep prompt text when redistribution is allowed.
        prompts: list[Prompt] = []
        cases: list[Case] = []
        for i, rec in enumerate(raw_records):
            prompt_text = str(rec.get("prompt") or rec.get("original_prompt") or "")
            if prompt_text and not decision.can_redistribute:
                report.prompts_skipped_license += 1
                # Store metadata + analysis only (no prompt text).
                rec = {**rec, "prompt": "", "original_prompt": ""}
            if prompt_text and decision.can_redistribute:
                prompts.append(
                    Prompt(
                        id=f"{source_id}-p{i}",
                        title=str(rec.get("title") or f"prompt-{i}"),
                        original_prompt=prompt_text,
                        source_repo=source_id,
                        source_url=str(rec.get("source_url") or source_url),
                        author=str(rec.get("author") or rec.get("source_label") or ""),
                        license=license,
                        target_model=str(rec.get("model") or ""),
                        category=str(rec.get("category") or ""),
                        tags=[str(t) for t in rec.get("tags", [])] if isinstance(rec.get("tags"), list) else [],
                    )
                )
            cases.append(self.case_analyzer.analyze(rec, case_id=f"{source_id}-c{i}"))

        # Deduplicate prompts (normalized level) and cases (visual-intent level).
        prompt_result = self.dedup.dedup(prompts, level="normalized")
        case_result = self.dedup.dedup(cases, level="visual-intent")
        report.duplicates_removed = prompt_result.removed + case_result.removed

        report.prompts_kept = len(prompt_result.kept)
        report.cases_stored = len(case_result.kept)

        self.store.save("prompt", prompt_result.kept)
        self.store.save("case", case_result.kept)
        self.store.save(
            "source",
            [
                Source(
                    id=source_id,
                    name=source_id,
                    url=source_url,
                    license=license,
                    redistribution_status="allowed" if decision.can_redistribute else "restricted",
                    attribution_requirements=decision.note,
                )
            ],
        )
        return report

"""Shared fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest

from museforge.knowledge.store import KnowledgeStore
from museforge.services.assistant import MuseForgeAssistant

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@pytest.fixture(scope="session")
def store() -> KnowledgeStore:
    return KnowledgeStore(DATA_DIR)


@pytest.fixture(scope="session")
def assistant(store: KnowledgeStore) -> MuseForgeAssistant:
    return MuseForgeAssistant(store)

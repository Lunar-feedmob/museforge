"""LLM providers.

MuseForge is LLM-agnostic: the service layer depends on the ``LLMProvider`` protocol, never on
a specific vendor SDK. An Anthropic implementation is provided for convenience (this project
is developed in Claude Code), but the core never imports ``anthropic`` directly.

If no provider is configured, the Assistant falls back to deterministic heuristics.
"""

from __future__ import annotations

import os
from typing import Protocol


class LLMProvider(Protocol):
    """A minimal text-completion provider."""

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        """Return a completion for the given prompt."""
        ...


class AnthropicProvider:
    """Anthropic Messages API provider (requires the optional ``anthropic`` extra)."""

    def __init__(self, api_key: str | None = None, model: str = "claude-sonnet-5") -> None:
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.model = model

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        import anthropic  # type: ignore[import-not-found]  # optional dependency

        client = anthropic.Anthropic(api_key=self.api_key)
        kwargs: dict[str, object] = {
            "model": self.model,
            "max_tokens": 2048,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            kwargs["system"] = system
        message = client.messages.create(**kwargs)
        return "".join(block.text for block in message.content if getattr(block, "type", "") == "text")


def provider_from_env() -> LLMProvider | None:
    """Build an LLM provider from environment config, or None if unconfigured."""
    name = os.environ.get("MUSEFORGE_LLM_PROVIDER", "").lower()
    if name == "anthropic" and os.environ.get("ANTHROPIC_API_KEY"):
        return AnthropicProvider()
    return None

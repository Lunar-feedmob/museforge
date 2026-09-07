"""CLI tests using Typer's CliRunner."""

from __future__ import annotations

from typer.testing import CliRunner

from museforge.cli.main import app

runner = CliRunner()


def test_ask_returns_prompt() -> None:
    result = runner.invoke(app, ["ask", "Create a premium fintech card advertisement"])
    assert result.exit_code == 0
    assert "Super Prompt" in result.output


def test_ask_prompt_only() -> None:
    result = runner.invoke(app, ["ask", "Create a premium fintech card advertisement", "--prompt-only"])
    assert result.exit_code == 0
    assert "Product:" in result.output


def test_recipes_search() -> None:
    result = runner.invoke(app, ["recipes", "search", "poster"])
    assert result.exit_code == 0
    assert "Editorial Poster" in result.output


def test_patterns_search() -> None:
    result = runner.invoke(app, ["patterns", "search", "product hero"])
    assert result.exit_code == 0
    assert "Breakout Product Hero" in result.output


def test_stats() -> None:
    result = runner.invoke(app, ["stats"])
    assert result.exit_code == 0
    assert "recipe" in result.output


def test_sources() -> None:
    result = runner.invoke(app, ["sources"])
    assert result.exit_code == 0
    assert "awesome-gpt4o-images" in result.output


def test_analyze() -> None:
    result = runner.invoke(app, ["analyze", "帮我做一张 AI 公司招聘小红书封面"])
    assert result.exit_code == 0
    assert "recruitment marketing" in result.output


def test_normalize() -> None:
    result = runner.invoke(app, ["normalize", "**A** [link](https://x.com)  text"])
    assert result.exit_code == 0
    assert "a link text" in result.output


def test_dedup() -> None:
    result = runner.invoke(app, ["dedup", "normalized", "a b|a b|A B"])
    assert result.exit_code == 0
    assert "kept 1" in result.output

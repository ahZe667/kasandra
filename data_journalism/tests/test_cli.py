"""Smoke tests for the CLI surface."""

from __future__ import annotations

from typer.testing import CliRunner

from data_journalism.cli import app

runner = CliRunner()


def test_help_lists_pipeline_commands():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for command in ("acquire", "clean", "analyze", "publish", "run"):
        assert command in result.stdout

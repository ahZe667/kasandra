from typer.testing import CliRunner

from kasandra.cli.main import app

runner = CliRunner()


def test_root_help_lists_expected_commands() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "watchlist" in result.stdout
    assert "fetch" in result.stdout
    assert "diff" in result.stdout
    assert "digest" in result.stdout
    assert "run" in result.stdout


def test_fetch_command_is_wired() -> None:
    result = runner.invoke(app, ["fetch", "--source", "krs"])

    assert result.exit_code == 0
    assert "fetch krs: scaffold only" in result.stdout

"""CLI entry point for the Kasandra internal alpha."""

from __future__ import annotations

import typer

app = typer.Typer(
    help="Kasandra CLI for the internal alpha.",
    add_completion=False,
    no_args_is_help=True,
)

watchlist_app = typer.Typer(
    help="Manage the monitored companies watchlist.",
    add_completion=False,
    no_args_is_help=True,
)
app.add_typer(watchlist_app, name="watchlist")


def _scaffold_message(command_name: str) -> None:
    typer.echo(f"{command_name}: scaffold only, implementation pending.")


@watchlist_app.command("list")
def watchlist_list() -> None:
    """Show the current watchlist."""
    _scaffold_message("watchlist list")


@app.command()
def fetch(
    source: str = typer.Option(
        "all",
        "--source",
        help="Source to fetch: krs, crbr or all.",
    ),
) -> None:
    """Fetch data from external sources."""
    _scaffold_message(f"fetch {source}")


@app.command()
def diff() -> None:
    """Compute changes between snapshots."""
    _scaffold_message("diff")


@app.command()
def digest() -> None:
    """Render a digest from detected changes."""
    _scaffold_message("digest")


@app.command()
def run() -> None:
    """Run the end-to-end internal alpha pipeline."""
    _scaffold_message("run")


def main() -> None:
    """Run the Typer application."""
    app()

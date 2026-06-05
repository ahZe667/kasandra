"""CLI for the data journalism scaffold.

Each pipeline stage is its own command, plus ``run`` to chain them end to end.
"""

from __future__ import annotations

from typing import Optional

import typer

from data_journalism import config
from data_journalism.acquire import fetch_url, sample_dataset
from data_journalism.analyze import summarize
from data_journalism.clean import clean_csv
from data_journalism.publish import render_report

app = typer.Typer(
    help="Data journalism pipeline: acquire -> clean -> analyze -> publish.",
    add_completion=False,
    no_args_is_help=True,
)


@app.command()
def acquire(
    url: Optional[str] = typer.Option(
        None, "--url", "-u", help="URL to download. Omit to use the built-in sample."
    ),
    filename: str = typer.Option("sample.csv", "--name", "-n", help="Output filename."),
) -> None:
    """Pull source data into data/raw."""
    path = fetch_url(url, filename) if url else sample_dataset(filename)
    typer.echo(f"acquired: {path}")


@app.command()
def clean(
    source: str = typer.Option("data/raw/sample.csv", "--in", help="Raw input file."),
) -> None:
    """Normalize raw data into a tidy table in data/interim."""
    path = clean_csv(config.PROJECT_ROOT / source)
    typer.echo(f"cleaned: {path}")


@app.command()
def analyze(
    source: str = typer.Option("data/interim/clean.csv", "--in", help="Clean input file."),
) -> None:
    """Compute the findings and write them to data/processed."""
    path = summarize(config.PROJECT_ROOT / source)
    typer.echo(f"analyzed: {path}")


@app.command()
def publish(
    source: str = typer.Option("data/processed/summary.csv", "--in", help="Summary input file."),
) -> None:
    """Render a Markdown report and chart into outputs/."""
    outputs = render_report(config.PROJECT_ROOT / source)
    for label, path in outputs.items():
        typer.echo(f"{label}: {path}")


@app.command()
def run(
    url: Optional[str] = typer.Option(
        None, "--url", "-u", help="URL to download. Omit to use the built-in sample."
    ),
) -> None:
    """Run the full pipeline end to end."""
    raw = fetch_url(url, "sample.csv") if url else sample_dataset()
    typer.echo(f"acquired: {raw}")
    interim = clean_csv(raw)
    typer.echo(f"cleaned: {interim}")
    processed = summarize(interim)
    typer.echo(f"analyzed: {processed}")
    outputs = render_report(processed)
    for label, path in outputs.items():
        typer.echo(f"{label}: {path}")
    typer.echo("\nDone. See the outputs/ directory.")


def main() -> None:
    """Run the Typer application."""
    app()

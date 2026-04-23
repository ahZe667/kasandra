"""CLI entry point for the Kasandra internal alpha."""

from __future__ import annotations

import subprocess
import sys
from datetime import date as _today_type
from typing import Optional

import typer

from kasandra.config.paths import REPO_ROOT
from kasandra.storage.sqlite import connect, init_db, list_companies

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

_SCRIPTS = REPO_ROOT / "dev_ms_data" / "scripts"


def _run_script(script: str, *args: str) -> None:
    subprocess.run([sys.executable, str(_SCRIPTS / script)] + list(args), check=True)


def _do_fetch(source: str, run_date: str) -> None:
    snap_dir = REPO_ROOT / "dev_ms_data" / "snapshots" / run_date
    norm_dir = REPO_ROOT / "dev_ms_data" / "normalized" / run_date
    sources = ["krs", "crbr"] if source == "all" else [source]

    for src in sources:
        if src == "krs":
            typer.echo(f"\n=== Fetch KRS ({run_date}) ===")
            _run_script("fetch_krs.py", str(snap_dir))
            typer.echo(f"\n=== Extract KRS ({run_date}) ===")
            _run_script("extract_krs.py", str(snap_dir / "krs"), str(norm_dir))
        elif src == "crbr":
            typer.echo(f"\n=== Fetch CRBR ({run_date}) ===")
            _run_script("fetch_crbr_playwright.py", str(snap_dir))
            typer.echo(f"\n=== Extract CRBR ({run_date}) ===")
            _run_script("extract_crbr.py", str(snap_dir / "crbr"), str(norm_dir))
        else:
            typer.echo(f"Nieznane źródło: {src}. Użyj krs, crbr lub all.", err=True)
            raise typer.Exit(1)

    typer.echo(f"\n=== Import do DB ({run_date}) ===")
    _run_script("import_today.py", run_date)


def _do_diff() -> None:
    from kasandra.processing.diff import run_diff

    typer.echo("=== Diff snapshotów ===\n")
    conn = connect()
    init_db(conn)
    run_diff(conn)
    conn.close()


def _do_digest() -> None:
    from kasandra.processing.alerts import generate_alerts, render_digest

    conn = connect()
    init_db(conn)
    new_alerts = generate_alerts(conn)
    if new_alerts:
        typer.echo(f"Wygenerowano {new_alerts} nowych alertów.\n")
    typer.echo(render_digest(conn))
    conn.close()


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------

@watchlist_app.command("list")
def watchlist_list() -> None:
    """Show the current watchlist."""
    conn = connect()
    init_db(conn)
    companies = list_companies(conn)
    conn.close()

    if not companies:
        typer.echo("Brak spółek w watchliście.")
        return

    typer.echo(f"{'Slug':<14} {'KRS':<12} {'NIP':<14} {'CRBR':>9}  Uwagi")
    typer.echo("-" * 76)
    for c in companies:
        crbr_status = "zwolniona" if c["crbr_exempt"] else "monitorowana"
        typer.echo(
            f"{c['slug']:<14} {c['krs']:<12} {c['nip'] or '—':<14} {crbr_status:>9}  {c['notes'] or ''}"
        )


@app.command()
def fetch(
    source: str = typer.Option("all", "--source", "-s", help="krs | crbr | all"),
    run_date: Optional[str] = typer.Option(
        None, "--date", "-d", help="Data YYYY-MM-DD (domyślnie: dziś)"
    ),
) -> None:
    """Fetch snapshots from external sources, normalize, and import to DB."""
    d = run_date or str(_today_type.today())
    _do_fetch(source, d)
    typer.echo(f"\nGotowe: {source} ({d})")


@app.command()
def diff() -> None:
    """Detect changes between latest snapshots and write to the changes table."""
    _do_diff()


@app.command()
def digest() -> None:
    """Generate alerts from changes and render a prioritised text digest."""
    _do_digest()


@app.command()
def run(
    source: str = typer.Option("all", "--source", "-s", help="krs | crbr | all"),
    run_date: Optional[str] = typer.Option(
        None, "--date", "-d", help="Data YYYY-MM-DD (domyślnie: dziś)"
    ),
) -> None:
    """Run the full pipeline: fetch → diff → digest."""
    d = run_date or str(_today_type.today())
    _do_fetch(source, d)
    _do_diff()
    _do_digest()


def main() -> None:
    """Run the Typer application."""
    app()

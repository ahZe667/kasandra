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
    # CRBR zawieszone od 2026-04-28 (dostep publiczny konczy sie 2026-07-01)
    sources = ["krs", "vat"] if source == "all" else [source]

    for src in sources:
        if src == "krs":
            typer.echo(f"\n=== Fetch KRS ({run_date}) ===")
            _run_script("fetch_krs.py", str(snap_dir))
            typer.echo(f"\n=== Extract KRS ({run_date}) ===")
            _run_script("extract_krs.py", str(snap_dir / "krs"), str(norm_dir))
        elif src == "vat":
            typer.echo(f"\n=== Fetch VAT ({run_date}) ===")
            _run_script("fetch_vat.py", str(snap_dir), run_date)
            typer.echo(f"\n=== Extract VAT ({run_date}) ===")
            _run_script("extract_vat.py", str(snap_dir / "vat"), str(norm_dir), run_date)
        else:
            typer.echo(f"Nieznane zrodlo: {src}. Uzyj krs, vat lub all.", err=True)
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
    from kasandra.config.paths import VAR_LOGS_DIR

    conn = connect()
    init_db(conn)
    new_alerts = generate_alerts(conn)
    if new_alerts:
        typer.echo(f"Wygenerowano {new_alerts} nowych alertow.\n")
    text = render_digest(conn)
    typer.echo(text)
    conn.close()

    VAR_LOGS_DIR.mkdir(parents=True, exist_ok=True)
    digest_path = VAR_LOGS_DIR / f"digest_{_today_type.today()}.txt"
    digest_path.write_text(text, encoding="utf-8")


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
            f"{c['slug']:<14} {c['krs']:<12} {c['nip'] or '-':<14} {crbr_status:>9}  {c['notes'] or ''}"
        )


@app.command()
def fetch(
    source: str = typer.Option("all", "--source", "-s", help="krs | vat | all"),
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
def history(
    slug: str = typer.Argument(..., help="Slug spolki (np. zabka)"),
) -> None:
    """Show full change history for a company."""
    from kasandra.storage.sqlite import list_changes

    conn = connect()
    init_db(conn)
    company = conn.execute(
        "SELECT id, krs, nazwa FROM companies WHERE slug = ?", (slug,)
    ).fetchone()
    if company is None:
        typer.echo(f"Nie znaleziono spolki: {slug}", err=True)
        raise typer.Exit(1)

    changes = list_changes(conn, company["id"])
    conn.close()

    if not changes:
        typer.echo(f"{slug}: brak zmian w historii.")
        return

    typer.echo(f"=== Historia zmian: {slug} ({company['krs']}) ===\n")
    for ch in changes:
        date = ch["change_date"] or "?"
        rule = ch["alert_rule"]
        before = ch["value_before"] or ""
        after = ch["value_after"] or ""
        if len(before) > 70:
            before = before[:67] + "..."
        if len(after) > 70:
            after = after[:67] + "..."
        typer.echo(f"  {date}  [{rule}]")
        if before and before not in ("null", "[]", "false", "true"):
            typer.echo(f"    przed: {before}")
        if after and after not in ("null", "[]", "false", "true"):
            typer.echo(f"    po:    {after}")


@app.command()
def review() -> None:
    """Show new alerts and mark them as seen."""
    from kasandra.storage.sqlite import mark_alerts_seen

    _do_digest()
    conn = connect()
    init_db(conn)
    marked = mark_alerts_seen(conn)
    conn.close()
    if marked:
        typer.echo(f"\n({marked} alertow oznaczono jako seen)")


@app.command()
def run(
    source: str = typer.Option("all", "--source", "-s", help="krs | vat | all"),
    run_date: Optional[str] = typer.Option(
        None, "--date", "-d", help="Data YYYY-MM-DD (domyślnie: dziś)"
    ),
) -> None:
    """Run the full pipeline: fetch -> diff -> digest."""
    d = run_date or str(_today_type.today())
    _do_fetch(source, d)
    _do_diff()
    _do_digest()


def main() -> None:
    """Run the Typer application."""
    app()

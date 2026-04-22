"""SQLite helpers for the Kasandra internal alpha."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any

from kasandra.config.paths import SQL_DIR, VAR_SQLITE_DIR, ensure_runtime_dirs

DEFAULT_DB_PATH = VAR_SQLITE_DIR / "kasandra.sqlite3"
_SCHEMA_SQL = SQL_DIR / "schema" / "001_init.sql"


def connect(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    ensure_runtime_dirs()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# kept for backwards-compat with any existing callers
connect_sqlite = connect


def init_db(conn: sqlite3.Connection) -> None:
    """Create tables from schema SQL if they don't exist yet."""
    sql = _SCHEMA_SQL.read_text(encoding="utf-8")
    conn.executescript(sql)


def payload_hash(payload: dict[str, Any] | None) -> str | None:
    if payload is None:
        return None
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode()).hexdigest()


# --------------------------------------------------------------------------
# companies
# --------------------------------------------------------------------------

def upsert_company(
    conn: sqlite3.Connection,
    *,
    krs: str,
    nip: str | None = None,
    regon: str | None = None,
    slug: str,
    nazwa: str | None = None,
    crbr_exempt: bool = False,
    notes: str | None = None,
) -> int:
    """Insert or update a company; return its id."""
    conn.execute(
        """
        INSERT INTO companies (krs, nip, regon, slug, nazwa, crbr_exempt, notes)
        VALUES (:krs, :nip, :regon, :slug, :nazwa, :crbr_exempt, :notes)
        ON CONFLICT(krs) DO UPDATE SET
            nip         = excluded.nip,
            regon       = excluded.regon,
            nazwa       = excluded.nazwa,
            crbr_exempt = excluded.crbr_exempt,
            notes       = excluded.notes
        """,
        {
            "krs": krs,
            "nip": nip,
            "regon": regon,
            "slug": slug,
            "nazwa": nazwa,
            "crbr_exempt": int(crbr_exempt),
            "notes": notes,
        },
    )
    row = conn.execute("SELECT id FROM companies WHERE krs = ?", (krs,)).fetchone()
    return row["id"]


def get_company_by_krs(conn: sqlite3.Connection, krs: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM companies WHERE krs = ?", (krs,)
    ).fetchone()


def get_company_by_nip(conn: sqlite3.Connection, nip: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM companies WHERE nip = ?", (nip,)
    ).fetchone()


def list_companies(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute("SELECT * FROM companies ORDER BY slug").fetchall()


# --------------------------------------------------------------------------
# snapshots
# --------------------------------------------------------------------------

def insert_snapshot(
    conn: sqlite3.Connection,
    *,
    company_id: int,
    source: str,
    collected_at: str,
    status: str = "ok",
    normalized_payload: dict[str, Any] | None = None,
    raw_path: str | None = None,
) -> int:
    """Insert a snapshot; skip silently if (company, source, date) already exists.

    Returns the snapshot id (existing or new).
    """
    existing = conn.execute(
        "SELECT id FROM snapshots WHERE company_id=? AND source=? AND collected_at=?",
        (company_id, source, collected_at),
    ).fetchone()
    if existing:
        return existing["id"]

    ph = payload_hash(normalized_payload)
    payload_json = (
        json.dumps(normalized_payload, ensure_ascii=False) if normalized_payload else None
    )
    cur = conn.execute(
        """
        INSERT INTO snapshots
            (company_id, source, collected_at, status, normalized_payload, payload_hash, raw_path)
        VALUES
            (:company_id, :source, :collected_at, :status, :payload, :hash, :raw_path)
        """,
        {
            "company_id": company_id,
            "source": source,
            "collected_at": collected_at,
            "status": status,
            "payload": payload_json,
            "hash": ph,
            "raw_path": raw_path,
        },
    )
    return cur.lastrowid  # type: ignore[return-value]


def get_latest_snapshot(
    conn: sqlite3.Connection, company_id: int, source: str
) -> sqlite3.Row | None:
    return conn.execute(
        """
        SELECT * FROM snapshots
        WHERE company_id = ? AND source = ?
        ORDER BY collected_at DESC
        LIMIT 1
        """,
        (company_id, source),
    ).fetchone()


def get_snapshots(
    conn: sqlite3.Connection, company_id: int, source: str
) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT * FROM snapshots
        WHERE company_id = ? AND source = ?
        ORDER BY collected_at ASC
        """,
        (company_id, source),
    ).fetchall()

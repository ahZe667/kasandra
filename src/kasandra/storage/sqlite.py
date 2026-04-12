"""SQLite helpers for the Kasandra internal alpha."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from kasandra.config.paths import VAR_SQLITE_DIR, ensure_runtime_dirs

DEFAULT_DB_PATH = VAR_SQLITE_DIR / "kasandra.sqlite3"


def connect_sqlite(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Open a SQLite connection for the local runtime."""
    ensure_runtime_dirs()
    return sqlite3.connect(db_path)

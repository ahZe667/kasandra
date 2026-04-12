"""Filesystem paths used by the Kasandra runtime."""

from __future__ import annotations

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = PACKAGE_DIR.parent
REPO_ROOT = SRC_DIR.parent

SQL_DIR = REPO_ROOT / "sql"
VAR_DIR = REPO_ROOT / "var"
VAR_SQLITE_DIR = VAR_DIR / "sqlite"
VAR_EXPORTS_DIR = VAR_DIR / "exports"
VAR_TMP_DIR = VAR_DIR / "tmp"


def ensure_runtime_dirs() -> None:
    """Ensure runtime directories exist locally."""
    for path in (VAR_DIR, VAR_SQLITE_DIR, VAR_EXPORTS_DIR, VAR_TMP_DIR):
        path.mkdir(parents=True, exist_ok=True)

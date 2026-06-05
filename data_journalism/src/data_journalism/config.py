"""Project paths and runtime configuration.

Values are read from environment variables (see ``.env.example``) and fall back
to sensible defaults rooted at the project directory.
"""

from __future__ import annotations

import os
from pathlib import Path

# Project root = two levels up from this file (src/data_journalism/config.py).
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _path_from_env(var: str, default: str) -> Path:
    raw = os.environ.get(var, default)
    path = Path(raw)
    return path if path.is_absolute() else PROJECT_ROOT / path


DATA_DIR = _path_from_env("DJ_DATA_DIR", "data")
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = _path_from_env("DJ_OUTPUT_DIR", "outputs")

HTTP_TIMEOUT = float(os.environ.get("DJ_HTTP_TIMEOUT", "30"))
LOG_LEVEL = os.environ.get("DJ_LOG_LEVEL", "INFO")


def ensure_dirs() -> None:
    """Create the data and output directories if they do not exist."""
    for directory in (RAW_DIR, INTERIM_DIR, PROCESSED_DIR, OUTPUT_DIR):
        directory.mkdir(parents=True, exist_ok=True)

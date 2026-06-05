"""Acquire stage: pull source data into ``data/raw``.

Replace :func:`fetch_url` / :func:`sample_dataset` with the real sources for
your story. The contract is simple: write a file into ``RAW_DIR`` and return
its path so later stages can pick it up.
"""

from __future__ import annotations

from pathlib import Path

import httpx

from data_journalism import config


def fetch_url(url: str, filename: str) -> Path:
    """Download ``url`` into ``data/raw/<filename>`` and return the path."""
    config.ensure_dirs()
    target = config.RAW_DIR / filename
    with httpx.Client(timeout=config.HTTP_TIMEOUT, follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()
        target.write_bytes(response.content)
    return target


def sample_dataset(filename: str = "sample.csv") -> Path:
    """Write a tiny built-in dataset so the pipeline runs without network access."""
    config.ensure_dirs()
    target = config.RAW_DIR / filename
    rows = [
        "region,year,value",
        "north,2023,120",
        "north,2024,135",
        "south,2023,98",
        "south,2024,110",
        "east,2023,77",
        "east,2024,_missing_",
        "west,2023,142",
        "west,2024,150",
    ]
    target.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return target

"""Clean stage: normalize raw data into a tidy table in ``data/interim``.

Cleaning is where most data journalism work hides: fixing types, dropping junk
rows, standardizing labels. Keep transformations explicit and reproducible.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from data_journalism import config


def clean_csv(source: Path, filename: str = "clean.csv") -> Path:
    """Read a raw CSV, coerce types, drop unusable rows, and save to interim."""
    config.ensure_dirs()
    frame = pd.read_csv(source)

    # Standardize text columns: strip whitespace, lowercase categorical labels.
    for column in frame.select_dtypes(include="object").columns:
        frame[column] = frame[column].astype(str).str.strip()
    if "region" in frame.columns:
        frame["region"] = frame["region"].str.lower()

    # Coerce the metric to numeric; sentinel/garbage values become NaN and drop.
    if "value" in frame.columns:
        frame["value"] = pd.to_numeric(frame["value"], errors="coerce")
        frame = frame.dropna(subset=["value"])

    target = config.INTERIM_DIR / filename
    frame.to_csv(target, index=False)
    return target

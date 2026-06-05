"""Analyze stage: turn the clean table into the findings behind the story.

Output a compact, story-ready summary into ``data/processed``. The example
computes per-region totals and year-over-year change; swap in the question
your reporting actually needs to answer.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from data_journalism import config


def summarize(source: Path, filename: str = "summary.csv") -> Path:
    """Compute per-region totals and year-over-year change; save to processed."""
    config.ensure_dirs()
    frame = pd.read_csv(source)

    totals = frame.groupby("region", as_index=False)["value"].sum()
    totals = totals.rename(columns={"value": "total"}).sort_values("total", ascending=False)

    if {"region", "year", "value"}.issubset(frame.columns):
        pivot = frame.pivot_table(index="region", columns="year", values="value", aggfunc="sum")
        years = sorted(pivot.columns)
        if len(years) >= 2:
            first, last = years[0], years[-1]
            change = ((pivot[last] - pivot[first]) / pivot[first] * 100).round(1)
            totals = totals.merge(
                change.rename("yoy_change_pct").reset_index(), on="region", how="left"
            )

    target = config.PROCESSED_DIR / filename
    totals.to_csv(target, index=False)
    return target

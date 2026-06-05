"""Publish stage: render findings into shareable outputs.

Produces a Markdown report and a bar chart in ``outputs/``. These are the
artifacts a newsroom hands to an editor or embeds in a story.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless backend; safe in CI and on servers.
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from data_journalism import config  # noqa: E402


def render_report(summary: Path, basename: str = "report") -> dict[str, Path]:
    """Render a Markdown table and a bar chart from the analysis summary."""
    config.ensure_dirs()
    frame = pd.read_csv(summary)

    report_path = config.OUTPUT_DIR / f"{basename}.md"
    table = frame.to_markdown(index=False) or ""
    report_path.write_text(f"# Findings\n\n{table}\n", encoding="utf-8")

    chart_path = config.OUTPUT_DIR / f"{basename}.png"
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(frame["region"], frame["total"])
    ax.set_title("Total value by region")
    ax.set_xlabel("region")
    ax.set_ylabel("total")
    fig.tight_layout()
    fig.savefig(chart_path, dpi=120)
    plt.close(fig)

    return {"report": report_path, "chart": chart_path}

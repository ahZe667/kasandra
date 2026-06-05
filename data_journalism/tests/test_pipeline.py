"""End-to-end smoke test for the pipeline, using the built-in sample dataset."""

from __future__ import annotations

import pandas as pd

from data_journalism.acquire import sample_dataset
from data_journalism.analyze import summarize
from data_journalism.clean import clean_csv
from data_journalism.publish import render_report


def test_pipeline_runs_end_to_end(tmp_path, monkeypatch):
    # Redirect all I/O into a temp project so the test leaves no artifacts.
    import data_journalism.config as config

    monkeypatch.setattr(config, "RAW_DIR", tmp_path / "raw")
    monkeypatch.setattr(config, "INTERIM_DIR", tmp_path / "interim")
    monkeypatch.setattr(config, "PROCESSED_DIR", tmp_path / "processed")
    monkeypatch.setattr(config, "OUTPUT_DIR", tmp_path / "outputs")

    raw = sample_dataset()
    interim = clean_csv(raw)
    processed = summarize(interim)
    outputs = render_report(processed)

    assert raw.exists()
    assert interim.exists()
    assert processed.exists()
    assert outputs["report"].exists()
    assert outputs["chart"].exists()

    summary = pd.read_csv(processed)
    # The "_missing_" sentinel row should have been dropped during cleaning,
    # so every region in the summary has a numeric total.
    assert summary["total"].notna().all()
    assert "west" in set(summary["region"])

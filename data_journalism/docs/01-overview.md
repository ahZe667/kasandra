# Overview

`data_journalism` is a starting point for turning public data into stories. It
is deliberately small: a pipeline, a convention for where data lives, and a
working example you can gut and replace.

## Why a pipeline

Data journalism repeats the same shape on every story. Naming the stages keeps
the work reproducible and reviewable:

| Stage   | Input          | Output           | Question it answers              |
| ------- | -------------- | ---------------- | -------------------------------- |
| acquire | a source/URL   | `data/raw`       | What did we pull, and from where?|
| clean   | `data/raw`     | `data/interim`   | Is the data trustworthy and tidy?|
| analyze | `data/interim` | `data/processed` | What does the data actually say? |
| publish | `data/processed`| `outputs/`      | How do we show it to readers?    |

## Data directory contract

- `data/raw/` — exactly as fetched, never edited by hand. Treated as immutable.
- `data/interim/` — cleaned, typed, deduplicated working tables.
- `data/processed/` — the final, story-ready summaries.
- `outputs/` — rendered artifacts (reports, charts) for editors and readers.

Contents of `data/` and `outputs/` are git-ignored; only the directory layout
is committed (via `.gitkeep`). Commit small, illustrative samples deliberately
if a story needs them.

## Extending the scaffold

1. Add a real source in `acquire/` (an API client, scraper, or download).
2. Encode the cleaning rules your data needs in `clean/`.
3. Replace the example aggregation in `analyze/` with your reporting question.
4. Shape the `publish/` output to match where the story will live.

Keep each stage independently runnable through the CLI so you can iterate on
one step without rerunning the whole pipeline.

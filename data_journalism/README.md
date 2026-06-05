# data_journalism

A generic, reusable scaffold for data journalism projects. It models the work
as a four-stage pipeline and ships a tiny working example so the whole thing
runs out of the box — no external data needed.

```
acquire  ->  clean  ->  analyze  ->  publish
data/raw    data/interim  data/processed   outputs/
```

## Pipeline stages

- **acquire** (`src/data_journalism/acquire/`) — pull source data into `data/raw`.
- **clean** (`src/data_journalism/clean/`) — normalize into a tidy table in `data/interim`.
- **analyze** (`src/data_journalism/analyze/`) — compute the findings into `data/processed`.
- **publish** (`src/data_journalism/publish/`) — render a Markdown report + chart into `outputs/`.

Each stage is a small module with one obvious entry point. Replace the example
logic with your story's sources and questions — the directory contract stays
the same.

## Setup

```bash
uv run poe bootstrap
```

## Run the demo pipeline

```bash
uv run dj run            # full pipeline on the built-in sample dataset
uv run dj run --url URL  # or point it at a real CSV

# or one stage at a time
uv run dj acquire
uv run dj clean
uv run dj analyze
uv run dj publish
```

Outputs land in `outputs/` (`report.md`, `report.png`).

## Layout

- application package: `src/data_journalism/`
- CLI: `uv run dj --help`
- data: `data/raw`, `data/interim`, `data/processed` (contents git-ignored)
- exploratory work: `notebooks/`
- docs: `docs/`

## Quality gates

```bash
uv run poe check   # pre-commit + ruff + ty + pytest
```

CI runs the same gates — see `.github/workflows/ci.yml`.

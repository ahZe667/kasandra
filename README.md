# Kasandra

Kasandra to wspolne repo dla dokumentacji, przykladow i implementacji systemu monitoringu polskich spolek opartego na danych publicznych.

## Glowne dokumenty

- [01-overview](docs/01-overview.md)
- [02-sources-and-alerts](docs/02-sources-and-alerts.md)
- [03-roadmap-and-gates](docs/03-roadmap-and-gates.md)
- [04-tech-stack](docs/04-tech-stack.md)
- [sample-alerts](docs/examples/sample-alerts.md)
- [sample-company-cases](docs/examples/sample-company-cases.md)

## Stan projektu

- etap: `faza 0-1`
- domyslny zakres `v0`: `KRS + CRBR`
- cel pierwszej wersji: prosty pipeline zmian i alertow, nie pelna platforma

## Agent-first workflow

Repo jest prowadzone w trybie agent-driven.

- [CLAUDE.md](CLAUDE.md) jest glownym kontraktem pracy w repo
- `.claude/commands/` to publiczne slash commands (`/slice`, `/source`, `/docs-sync`, `/concept`)
- `.claude/skills/` to procedury wykonawcze
- `.claude/project-memory/` to trwala pamiec wersjonowana

## Setup

```bash
uv run poe bootstrap
```

## Runtime

- pakiet aplikacyjny: `src/kasandra/`
- CLI: `uv run kasandra --help`
- SQL: `sql/schema`, `sql/queries`, `sql/migrations`
- runtime data: `var/sqlite`, `var/exports`, `var/tmp`
- task reports: `var/reports/task-runs/`

## CI

- GitHub Actions uruchamia te same bramki jakosci co praca lokalna
- workflow jest w `.github/workflows/ci.yml`

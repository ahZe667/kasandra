# Kasandra

Kasandra to wspólne repo dla dokumentacji, researchu, przykładów i implementacji systemu monitoringu polskich spółek opartego na danych publicznych. Punkt wyjścia to wąska `alpha wewnętrzna`: budowa użytecznego systemu i własnego IP, z opcją komercjalizacji później.

## Główne dokumenty

- [01-overview](docs/01-overview.md)
- [02-data-sources](docs/02-data-sources.md)
- [03-signals-and-alerts](docs/03-signals-and-alerts.md)
- [04-market-and-positioning](docs/04-market-and-positioning.md)
- [05-mvp](docs/05-mvp.md)
- [06-risks-and-open-questions](docs/06-risks-and-open-questions.md)
- [07-tech-stack](docs/07-tech-stack.md)

## Stan projektu

- etap: `pre-build / alpha wewnętrzna`
- domyślny zakres `v0`: `KRS + CRBR`
- cel pierwszej wersji: zbudować prosty pipeline zmian i alertów, a nie pełną platformę

## Agent-first workflow

- wspólne zasady pracy agentów: [AGENTS.md](AGENTS.md)
- cienka nakładka dla Claude Code: [CLAUDE.md](CLAUDE.md)
- vendor-neutral skills: `.agents/skills/`
- bootstrap repo: `powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1`
- pełne checki repo: `powershell -ExecutionPolicy Bypass -File scripts/repo-check.ps1`
- check zmienionych plików dla hooków Claude: `powershell -ExecutionPolicy Bypass -File scripts/check-changed.ps1`
- preferowana konwencja gałęzi: `task/<slug>`

## Środowisko i sekrety

- zależności Python: `uv`
- repo trackuje tylko `.env.example`
- lokalne `.env` i warianty lokalne są ignorowane przez Git
- sekretów nie zapisujemy w repo, tylko przez zmienne środowiskowe

## Kod i runtime

- pakiet aplikacyjny: `src/kasandra/`
- CLI: `uv run kasandra --help`
- SQL: `sql/schema`, `sql/queries`, `sql/migrations`
- runtime data: `var/sqlite`, `var/exports`, `var/tmp`
- testy: `tests/unit`, `tests/integration`

## CI

- GitHub Actions uruchamia te same bramki jakości co praca lokalna
- workflow jest w `.github/workflows/ci.yml`

## Katalogi pomocnicze

- `research/` - notatki researchowe
- `examples/` - przykładowe alerty i case'y
- `docs/roadmap.mmd` - roadmapa w Mermaid
- `docs/roadmap.png` - wygenerowany podgląd roadmapy

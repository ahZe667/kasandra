# Kasandra

Kasandra to wspólne repo dla dokumentacji, przykładów i implementacji systemu monitoringu polskich spółek opartego na danych publicznych. Punkt wyjścia to wąska `alpha wewnętrzna`: budowa użytecznego systemu i własnego IP, z opcją komercjalizacji później.

## Główne dokumenty

- [01-overview](docs/01-overview.md)
- [02-data-sources](docs/02-data-sources.md)
- [03-signals-and-alerts](docs/03-signals-and-alerts.md)
- [04-market-and-positioning](docs/04-market-and-positioning.md)
- [05-mvp](docs/05-mvp.md)
- [06-risks-and-open-questions](docs/06-risks-and-open-questions.md)
- [07-tech-stack](docs/07-tech-stack.md)

## Stan projektu

- etap: `faza 0-1` — scaffold kodu, agent-driven workflow skonfigurowany
- domyślny zakres `v0`: `KRS + CRBR`
- cel pierwszej wersji: zbudować prosty pipeline zmian i alertów, a nie pełną platformę

## Agent-first workflow

Repo jest prowadzone w trybie agent-driven — kod powstaje przez agentów, nie ręcznie.

### Dokumenty sterujące

- [AGENTS.md](AGENTS.md) — zasady pracy agentów, konwencja commitów, routing do skills
- [CLAUDE.md](CLAUDE.md) — cienka nakładka dla Claude Code
- `.agents/skills/` — vendor-neutral procedury operacyjne

### Setup

```bash
uv run poe bootstrap
```

Bootstrap instaluje zależności Python (`uv sync`), hooki pre-commit (linting, ruff, conventional commits) i hook commit-msg.

### Typowy flow pracy

1. **Start taska** — `/task-start <opis zadania>`
   - Agent tworzy branch `task/<slug>` z `main`
   - Czyta `AGENTS.md` i dobiera właściwy skill
   - Czyta wymagane dokumenty i rozpoczyna pracę

2. **Praca** — agent implementuje zmianę zgodnie ze skillem:
   - `/slice` — mały feature end-to-end
   - `/source` — nowe źródło danych lub zmiana integracji
   - `/schema-change` — zmiana SQLite lub modelu danych
   - `/docs-sync` — synchronizacja dokumentacji
   - `/concept` — praca koncepcyjna (bez kodu)

3. **Finish taska** — `/task-finish`
   - Agent uruchamia `uv run poe check` (pre-commit + ruff + pytest)
   - Commituje z konwencją `<typ>(<scope>): <opis>` (angielski)
   - Pokazuje podsumowanie: co dowiezione, jak zweryfikować, follow-upy

4. **Push** — ręczna decyzja użytkownika

### Bramki jakości

Przy każdym `git commit` automatycznie odpalają się:

- **pre-commit hook** — trailing whitespace, line endings, JSON/TOML/YAML, merge conflicts, large files, private keys, AST check, debug statements, ruff
- **commit-msg hook** — walidacja formatu conventional commits (`feat`, `fix`, `docs`, `refactor`, `test`, `chore`)

Pełne checki (z pytest) uruchamia `uv run poe check`:

```bash
uv run poe check
```

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

- `examples/` - przykładowe alerty i case'y
- `docs/roadmap.mmd` - roadmapa w Mermaid
- `docs/roadmap.png` - wygenerowany podgląd roadmapy

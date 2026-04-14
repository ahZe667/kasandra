# AGENTS.md

## Kasandra

Kasandra jest jednym repozytorium dla:

- dokumentacji produktowej i koncepcyjnej,
- przykładów alertów i case studies,
- researchu,
- implementacji systemu.

Repo nie jest już tylko dokumentacyjne. Dokumentacja nadal wyznacza kierunek, ale kod, testy i tooling są już częścią tego samego workflow.

## Źródła prawdy

Przed większą zmianą przeczytaj właściwe dokumenty z `docs/`, `examples/` i `research/`.

Najważniejsze dziś są:

- `docs/01-overview.md`
- `docs/02-data-sources.md`
- `docs/03-signals-and-alerts.md`
- `docs/05-mvp.md`
- `docs/06-risks-and-open-questions.md`
- `docs/07-tech-stack.md`

## Główne zasady repo

- Język dokumentacji i komunikacji w repo: `polski`
- Nie twórz nowych numerowanych dokumentów bez wyraźnej potrzeby.
- Gdy zmieniasz ważne założenie produktu, zsynchronizuj powiązane pliki w tym samym change secie.
- Gdy zmieniasz fazy, zakres źródeł albo kierunek techniczny, sprawdź też `docs/roadmap.mmd`.
- Nie wymyślaj danych rynkowych, prawnych ani technicznych, jeśli nie są potwierdzone.

## Obecny kierunek produktu i implementacji

- `Faza 0-1`: rdzeń oparty o `KRS + CRBR`
- `Faza 1`: `v0 / alpha wewnętrzna`
- `Faza 2`: rozszerzenie `distress-first`, przede wszystkim `KRZ`
- `Faza 3`: mały pilot zewnętrzny, domyślnie `email-first`

## Obecny kierunek techniczny

Do czasu świadomej zmiany dokumentacji zakładamy:

- Python jako domyślny język implementacji
- `sqlite3` jako pierwszy magazyn danych
- prosty CLI przed ciężką orkiestracją
- brak publicznego API przed `Fazą 3`

Nie dodawaj ciężkiej infrastruktury tylko "na zapas".

## Konwencja commitów

Język commit messages: angielski.

Format: `<typ>(<scope>): <opis>`

Dozwolone typy: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

Scope jest opcjonalny. Używaj gdy dodaje informację — najczęściej przy `feat` i `fix`, żeby zawęzić obszar zmiany. Nie ma zamkniętej listy scope'ów; dopasuj do kontekstu (np. `sources`, `storage`, `cli`, `docs`).

Body jest opcjonalne. Dodawaj je przy `feat` i `fix` żeby wyjaśnić "dlaczego", nie "co". Przy `docs`, `chore`, `test` — zwykle zbędne.

Granularność: jeden commit na task. Wyjątek: gdy zmiana naturalnie się dzieli (np. schema + kod).

Przykłady:

- `feat(sources): add KRS API data fetching`
- `fix(storage): prevent duplicate snapshots on reimport`
- `docs: sync 02-data-sources with KRS contract`
- `chore: add conventional-pre-commit hook`

Konwencja jest wymuszana przez hook `commit-msg` w pre-commit.

## Workflow agentów

- Jeden task = jeden mały slice = jedna gałąź lub worktree.
- Preferowana konwencja gałęzi: `task/<slug>`.
- Po wdrożeniu tego setupu pierwszym krokiem operacyjnym powinien być bazowy commit repo, bo diff-based workflow działa wtedy przewidywalnie.
- Przed pracą przeczytaj `AGENTS.md`, właściwe dokumenty i odpowiadający skill z `.agents/skills/`.
- Dowieź jeden mały, kończący się feature albo jedną spójną zmianę koncepcyjną.
- Jeśli zmienił się kontrakt, zachowanie albo ważne założenie, zsynchronizuj `docs/` i `examples/`.
- Po pracy uruchom `uv run poe check`.
- Nie rozszerzaj scope'u ponad aktualną fazę projektu bez wyraźnej decyzji użytkownika.

## Routing zadań do skills

Canonical location dla skills to `.agents/skills/`.

- feature end-to-end: `.agents/skills/vertical-slice/SKILL.md`
- nowe źródło lub zmiana integracji: `.agents/skills/source-integration/SKILL.md`
- zmiana SQLite lub plików w `sql/`: `.agents/skills/schema-change/SKILL.md`
- synchronizacja dokumentacji i przykładów: `.agents/skills/docs-sync/SKILL.md`
- aktualizacja researchu lub benchmarków: `.agents/skills/research-update/SKILL.md`

Skills są repo-local procedurami operacyjnymi dla agentów i ludzi. To jest źródło prawdy dla workflow, a nie obietnica natywnego auto-loadu we wszystkich narzędziach.

## Struktura repo

```text
kasandra/
|- .agents/skills/
|- .claude/commands/
|- docs/
|- examples/
|- research/
|- scripts/
|- sql/
|  |- schema/
|  |- queries/
|  `- migrations/
|- src/kasandra/
|  |- cli/
|  |- config/
|  |- outputs/
|  |- processing/
|  |- sources/
|  `- storage/
|- tests/
|  |- unit/
|  `- integration/
`- var/
   |- sqlite/
   |- exports/
   `- tmp/
```

Zasady:

- kod aplikacyjny trafia do `src/kasandra/`
- CLI jest `Typer`-based i jest preferowanym entry pointem dla `Fazy 1`
- SQL, jeśli potrzebny, trafia do top-level `sql/`
- runtime data trafiają do `var/` i nie są trackowane
- `scripts/` są na bootstrap, checki i tooling repo, nie na główną logikę aplikacji

## Środowisko i sekrety

- Repo trackuje tylko `.env.example`.
- Lokalny `.env` i warianty lokalne nie trafiają do repo.
- Nie zapisuj sekretów, tokenów ani haseł w kodzie, docs, examples ani configach repo.
- Przyszłe sekrety mają przechodzić wyłącznie przez zmienne środowiskowe o tych samych nazwach lokalnie i w CI.

## Python workflow

- środowisko i zależności: `uv`
- konfiguracja projektu: `pyproject.toml`
- pełne checki repo: `uv run poe check`
- bootstrap środowiska: `uv run poe bootstrap`

## Jakość i checki

- `uv run poe check` jest wspólną bramką jakości dla pracy lokalnej i CI.
- Po zmianach kodu repo musi przechodzić `pre-commit`, `ruff` i `pytest`.
- Zmiany w dokumentach mają być czytelne, rzeczowe i bez korpomowy.
- Zmiany w kodzie mają być małe, weryfikowalne i łatwe do cofnięcia.

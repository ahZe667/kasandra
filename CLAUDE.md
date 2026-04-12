# CLAUDE.md

This file is a thin adapter for Claude Code.

## Start here

1. Najpierw przeczytaj `AGENTS.md`.
2. Potem użyj właściwego repo skill z `.agents/skills/`.
3. Traktuj `.claude/commands/` jako skróty, nie jako źródło prawdy.

## Minimalne zasady pracy

- Jeden task = jeden mały slice = jedna gałąź lub worktree.
- Preferowana konwencja gałęzi: `task/<slug>`.
- Nie rozszerzaj scope'u ponad aktualną fazę projektu.
- Jeśli zmienia się kontrakt, zachowanie albo ważne założenie, zsynchronizuj `docs/` i `examples/`.
- Przed oddaniem pracy uruchom `powershell -ExecutionPolicy Bypass -File scripts/repo-check.ps1`.

## Routing do repo skills

- feature end-to-end: `.agents/skills/vertical-slice/SKILL.md`
- źródła danych: `.agents/skills/source-integration/SKILL.md`
- SQLite i SQL: `.agents/skills/schema-change/SKILL.md`
- dokumentacja i examples: `.agents/skills/docs-sync/SKILL.md`
- research: `.agents/skills/research-update/SKILL.md`

## Kontekst repo

- `Faza 0-1`: `KRS + CRBR`
- `Faza 2`: `KRZ`
- `Faza 3`: mały pilot zewnętrzny
- technicznie: Python + `sqlite3` + `Typer` CLI zanim pojawi się cięższa infrastruktura

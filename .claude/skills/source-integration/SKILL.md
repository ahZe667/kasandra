---
name: source-integration
description: Fires when the task adds a new data source or changes an existing integration (KRS, CRBR, later KRZ). Use proactively when user mentions a source name or `/source`.
---

# Source integration

## Cel

Dowiezc spojny kontrakt zrodla: wejscie, normalizacja, bledy, output — plus punkt integracji w `src/kasandra/sources/` i zsynchronizowane `docs/02-sources-and-alerts.md` oraz `docs/examples/`.

## Constraints

- warstwa pobierania nie miesza logiki domenowej z integracja zrodla
- rate limits, ograniczenia jakosci danych i znane pulapki prawne zapisuj jawnie, nie ukrywaj ich w kodzie
- `Faza 0-1` ogranicza scope do `KRS + CRBR`; `KRZ` dopiero w `Fazie 2`
- nowe zrodlo = dokumentacja kontraktu + minimalny test integracyjny, nie tylko kod

## Non-goals

- nie wprowadza frameworka plugin-system dla "dowolnego zrodla"
- nie buduje retry/backoff na zapas, jesli zrodlo realnie tego nie wymaga
- nie zmienia storage schema razem z integracja — to osobny change set

## Gotchas

- `KRS` ma publiczne API, ale `CRBR` praktycznie wymaga scrapingu — kontrakty roznia sie fundamentalnie
- znane zrodlo prawdy dla zakresu: `docs/02-sources-and-alerts.md`; roadmap w `docs/03-roadmap-and-gates.md`
- nie wymyslaj pol danych ktorych nie widzisz w zrodle — zapisz "unknown" i zostaw do researchu

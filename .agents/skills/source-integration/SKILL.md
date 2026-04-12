# source-integration

## Kiedy używać

Użyj tego skillu, gdy zadanie dotyczy nowego źródła danych albo zmiany istniejącej integracji, na przykład `KRS`, `CRBR` albo później `KRZ`.

## Wejścia i zależności

- `AGENTS.md`
- `docs/02-data-sources.md`
- `docs/03-signals-and-alerts.md`
- `docs/05-mvp.md`
- istniejący kod w `src/kasandra/sources/`, `processing/` i `storage/`

## Kroki wykonania

1. Sprawdź, czy źródło mieści się w aktualnej fazie projektu.
2. Zdefiniuj minimalny kontrakt integracji: wejście, normalizacja, błędy, output do dalszego przetwarzania.
3. Dodaj lub zmień kod źródła bez mieszania logiki domenowej w warstwie pobierania danych.
4. Zsynchronizuj testy oraz dokumentację źródeł i alertów, jeśli zmienia się zachowanie systemu.
5. Uruchom pełne checki repo.

## Checki końcowe

- `powershell -ExecutionPolicy Bypass -File scripts/repo-check.ps1`
- opisz ograniczenia źródła, jeśli są istotne dla dalszej pracy

## Czego nie robić

- nie dodawaj źródeł poza aktualną fazą bez decyzji użytkownika
- nie łącz zmian źródłowych z większym refaktorem architektury
- nie ukrywaj ograniczeń jakości danych ani rate limitów

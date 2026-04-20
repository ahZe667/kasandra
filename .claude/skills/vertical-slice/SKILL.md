---
name: vertical-slice
description: Fires when the user asks for a small end-to-end change across CLI/sources/processing/storage/outputs. Use proactively when scope is bounded and fits the current phase (faza 0-1, KRS+CRBR).
---

# Vertical slice

## Cel

Jeden maly slice end-to-end dowieziony w jednym branchu `task/<slug>`, zachowujacy spojnosc miedzy kodem, testami, `docs/` i `docs/examples/`.

## Constraints

- scope nie rozlewa sie poza warstwy ktore naprawde musza sie zmienic (`cli`, `sources`, `processing`, `storage`, `outputs`)
- zmiana kontraktu wymaga rownoleglej aktualizacji `docs/` i `docs/examples/` w tym samym change secie
- `uv run poe check` musi przechodzic zanim zamkniesz task
- commit w formacie `<typ>(<scope>): <opis>`, jeden commit na task (wyjatek: schema + kod)

## Non-goals

- nie dodaje nowego zrodla w ramach zwyklego slice'a — do tego jest `source-integration`
- nie staje sie szerokim refactorem architektury
- nie wprowadza ciezkiej infrastruktury "na zapas"

## Gotchas

- sources i storage w `src/kasandra/` sa dzis w wiekszosci stubami; przed zmiana sprawdz czy kontrakt juz istnieje, czy go wprowadzasz
- `var/` jest runtime — nie commituj niczego co tam trafi
- testy siedza w `tests/unit` i `tests/integration`; integration test dla CLI juz istnieje jako wzorzec

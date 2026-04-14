# vertical-slice

## Kiedy używać

Użyj tego skillu, gdy zadanie dotyczy małej, domkniętej zmiany end-to-end, która powinna skończyć się działającym zachowaniem, testami i czytelnym entry pointem.

## Wejścia i zależności

- `AGENTS.md`
- właściwe dokumenty z `docs/`, zwykle `05-mvp` i `08-tech-stack`
- istniejący kod w `src/kasandra/`
- testy w `tests/`

## Kroki wykonania

1. Zidentyfikuj najmniejszy sensowny slice zgodny z aktualną fazą projektu.
2. Sprawdź, które warstwy naprawdę muszą się zmienić: CLI, sources, processing, storage, outputs.
3. Zaimplementuj zmianę w najprostszej formie, bez dokładania architektury na zapas.
4. Dodaj lub popraw test jednostkowy i integracyjny, jeśli slice dotyka CLI albo przepływu end-to-end.
5. Jeśli zmienił się kontrakt lub założenie, zsynchronizuj `docs/` i `examples/`.
6. Uruchom pełne checki repo.

## Checki końcowe

- `uv run poe check`
- pokaż, jaki slice został dowieziony i jak go uruchomić

## Czego nie robić

- nie łącz kilku niezależnych slice'ów w jednym tasku
- nie dodawaj nowego źródła danych w ramach zwykłego slice'a
- nie rozszerzaj scope'u ponad aktualną fazę

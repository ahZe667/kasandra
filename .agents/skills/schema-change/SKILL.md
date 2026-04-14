# schema-change

## Kiedy używać

Użyj tego skillu, gdy zadanie dotyczy zmian w `SQLite`, plikach `sql/` albo modelu danych, który wpływa na snapshoty, diffy, alerty lub watchlistę.

## Wejścia i zależności

- `AGENTS.md`
- `docs/05-mvp.md`
- `docs/08-tech-stack.md`
- kod w `src/kasandra/storage/` i powiązanych warstwach
- pliki w `sql/`

## Kroki wykonania

1. Ustal, czy zmiana jest zgodna z prostotą `Fazy 1`.
2. Zdefiniuj minimalny kontrakt danych i wpływ na istniejące odczyty lub zapisy.
3. Wprowadź zmianę w kodzie i w `sql/`, jeśli repo utrzymuje jawny schemat pomocniczy.
4. Dodaj testy dla nowego zachowania i dla podstawowej kompatybilności.
5. Zsynchronizuj dokumentację, jeśli zmienia się model danych albo założenia techniczne.
6. Uruchom pełne checki repo.

## Checki końcowe

- `uv run poe check`
- opisz wpływ na istniejące dane i najprostszy rollback

## Czego nie robić

- nie wprowadzaj pełnego systemu migracji tylko dlatego, że pojawił się pierwszy schema change
- nie mieszaj zmian schematu z szerokim refaktorem niezwiązanych warstw
- nie psuj prostoty `SQLite` bez wyraźnej potrzeby

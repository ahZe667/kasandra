# Architecture Memory

## Stabilne zalozenia

- Produkt: monitoring polskich spolek na danych publicznych.
- Etap: `Faza 1 zamknieta (2026-05-05)`, aktywne zrodla: `KRS + Biala Lista VAT`, CRBR zawieszone.
- Python jako domyslny jezyk, `sqlite3` jako pierwszy storage.
- `Faza 1` preferuje prosty CLI nad ciezka orkiestracja.
- Brak publicznego API przed `Faza 3`.

## Check i tooling

- `uv run poe check` to wspolna bramka jakosci dla pracy lokalnej i CI.

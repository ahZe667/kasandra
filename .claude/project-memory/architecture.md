# Architecture Memory

## Stabilne zalozenia

- Produkt: monitoring polskich spolek na danych publicznych.
- Etap: `faza 0-1`, zakres `v0` to `KRS + CRBR`.
- Python jako domyslny jezyk, `sqlite3` jako pierwszy storage.
- `Faza 1` preferuje prosty CLI nad ciezka orkiestracja.
- Brak publicznego API przed `Faza 3`.

## Check i tooling

- `uv run poe check` to wspolna bramka jakosci dla pracy lokalnej i CI.

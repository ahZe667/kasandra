# docs-sync

## Kiedy używać

Użyj tego skillu, gdy zadanie dotyczy aktualizacji dokumentacji, przykładów albo synchronizacji docs po zmianie kodu lub założeń projektu.

## Wejścia i zależności

- `AGENTS.md`
- odpowiednie pliki z `docs/`, `examples/` i ewentualnie `research/`
- zmienione pliki kodu lub nowe ustalenia produktowe

## Kroki wykonania

1. Zidentyfikuj, które dokumenty są źródłami prawdy dla zmienianego obszaru.
2. Zaktualizuj treść tak, żeby zachować spójność między overview, źródłami, alertami, fazami i ryzykami.
3. Jeśli zmienia się zachowanie systemu, dopilnuj zgodności `examples/`.
4. Jeśli zmienia się kierunek techniczny lub fazy, sprawdź też roadmapę.
5. Uruchom pełne checki repo.

## Checki końcowe

- `uv run poe check`
- upewnij się, że dokumenty mówią jednym głosem

## Czego nie robić

- nie twórz nowych numerowanych dokumentów bez potrzeby
- nie zostawiaj sprzeczności między `docs/` i `examples/`
- nie dopisuj niepotwierdzonych faktów do researchu

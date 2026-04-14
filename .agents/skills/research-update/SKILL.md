# research-update

## Kiedy używać

Użyj tego skillu, gdy zadanie dotyczy aktualizacji researchu, konkurencji, notatek źródłowych albo przykładów opartych na researchu.

## Wejścia i zależności

- `AGENTS.md`
- pliki w `research/`
- powiązane przykłady w `examples/`, jeśli research wpływa na przykłady alertów lub case studies

## Kroki wykonania

1. Zbierz tylko potwierdzone informacje i oddziel fakty od wniosków.
2. Zapisz research w prosty, czytelny sposób, bez marketingowego tonu.
3. Jeśli research zmienia wnioski produktowe, zsynchronizuj odpowiednie dokumenty z `docs/`.
4. Jeśli research wnosi nowe przykłady, zaktualizuj `examples/`.
5. Uruchom pełne checki repo.

## Checki końcowe

- `uv run poe check`
- jasno wskaż, co jest potwierdzonym faktem, a co interpretacją

## Czego nie robić

- nie dopisuj niezweryfikowanych danych rynkowych, prawnych ani technicznych
- nie mieszaj researchu z implementacją, jeśli task jest czysto badawczy
- nie zostawiaj w researchu tez, których nie da się obronić źródłami

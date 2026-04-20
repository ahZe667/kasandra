# Tech Stack

## Zasady techniczne

- `v0` ma byc male i proste,
- priorytetem jest dzialajacy pipeline i czytelny diff,
- startujemy od `KRS + CRBR`,
- ciezsza infrastruktura wchodzi dopiero wtedy, gdy prostsza wersja realnie przestaje wystarczac.

## Domyslny stack dla v0

| Warstwa | Decyzja | Dlaczego |
| --- | --- | --- |
| jezyk | `Python` | wystarcza do pobierania danych, diffu i generowania alertow |
| HTTP | `httpx` | prosty klient do zrodel publicznych |
| parsowanie | `BeautifulSoup4` lub bezposredni `JSON` | najprostsza sciezka per zrodlo |
| magazyn danych | `sqlite3` | lokalny start bez osobnego serwera |
| interfejs | `Typer`-based CLI | wystarcza do runu, debugowania i iteracji |
| jakosc | `pytest`, `ruff`, `pre-commit` | lekka i czytelna bramka jakosci |

Nie potrzebujemy na start Scrapy, Airflow ani rozbudowanej platformy danych.

## Minimalny przeplyw techniczny

1. Pobierz snapshot zrodla.
2. Zapisz `raw_payload`.
3. Znormalizuj dane do `normalized_payload`.
4. Porownaj z poprzednim snapshotem i wykryj diff.
5. Zapisz historie zmian i wygeneruj alert albo digest.

## Czego swiadomie nie bierzemy na start

| Technologia | Dlaczego nie teraz |
| --- | --- |
| Airflow | za ciezki na pierwszy etap |
| PostgreSQL | niepotrzebny przed sprawdzeniem modelu danych |
| Docker jako wymog | nie jest warunkiem sensownego startu |
| pelny panel webowy | alert, digest i historia zmian wystarczaja na `v0` |
| ML / NLP do scoringu | za wczesnie, proste reguly sa lepsze na start |

## Kiedy mozna dokladac wiecej

| Decyzja | Trigger |
| --- | --- |
| `KRZ` | gdy `KRS + CRBR` daja juz stabilny rdzen i potrzeba silniejszych sygnalow distress |
| scheduler / retry / monitoring zdrowia | gdy manual run zaczyna byc realnym bottleneckiem |
| `PostgreSQL` | gdy `sqlite3` przestaje wystarczac pojemnosciowo albo operacyjnie |
| email-first delivery | gdy alert i digest sa juz wystarczajaco czytelne dla odbiorcy spoza zespolu |
| lekki panel lub API | gdy historia zmian i digest sa stabilne i faktycznie uzywane |

## Struktura repo

```text
src/kasandra/
  cli/
  sources/
  processing/
  storage/
  outputs/
  config/
sql/
  schema/
  queries/
  migrations/
tests/
  unit/
  integration/
var/
  sqlite/
  exports/
  tmp/
```

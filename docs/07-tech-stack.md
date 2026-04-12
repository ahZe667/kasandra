# Tech Stack — propozycja

## Założenia

- `v0` ma być małe i proste
- priorytet to działający pipeline i czytelny diff, nie architektura na zapas
- startujemy od `KRS + CRBR`
- cięższa infrastruktura ma wejść dopiero wtedy, gdy prostsza wersja przestanie wystarczać

## Propozycja dla v0

### Python jako rdzeń

Cały projekt w Pythonie. To wystarczy do pobierania danych, parsowania, zapisu snapshotów, diffu i generowania prostych alertów.

### Pobieranie danych

| Warstwa | Narzędzie | Dlaczego |
| --- | --- | --- |
| HTTP | `httpx` | prosty klient do pobierania danych |
| Parsowanie HTML | `BeautifulSoup4` | wystarczające tam, gdzie potrzebny będzie HTML |
| Parsowanie API | bezpośrednio JSON | najprostsza ścieżka dla źródeł API |

Nie potrzeba na start frameworka typu Scrapy. Proste moduły per źródło będą łatwiejsze do zrozumienia i utrzymania.

### Magazyn danych

**SQLite (`sqlite3`)**

- wystarczy do pierwszej watchlisty, snapshotów i historii zmian
- nie wymaga osobnego serwera
- dobrze pasuje do lokalnego i iteracyjnego startu
- pozwala sprawdzić model danych przed wejściem w cięższą bazę

### Uruchamianie

Na start:

- ręczne uruchamianie skryptów,
- ewentualnie prosty harmonogram później, jeśli pojawi się potrzeba.

Nie ma potrzeby wchodzić od razu w Airflow albo rozbudowaną orkiestrację.

### Wykrywanie zmian i scoring

Prosta logika w Pythonie:

- zapis kolejnego snapshotu,
- porównanie z poprzednim stanem,
- reguły priorytetu zapisane w kodzie lub prostym configu.

Na tym etapie ważniejsze jest, żeby reguły były czytelne niż bardzo rozbudowane.

### Format wyjścia

Pierwsza wersja może działać bez panelu:

- alert tekstowy w konsoli lub pliku,
- prosty digest,
- historia zmian dla spółki.

To wystarczy, żeby ocenić użyteczność systemu i jakość danych.

## Mapa techniczna per faza

### Faza 0 — definicja rdzenia

- brak właściwej automatyzacji
- ręczne snapshoty i ręczne case studies
- doprecyzowanie modelu spółki, snapshotu, zmiany i alertu
- zamrożenie listy pól monitorowanych z `KRS` i `CRBR`

### Faza 1 — v0 / alpha wewnętrzna

- Python
- `KRS + CRBR`
- `sqlite3`
- `Typer`-based CLI
- lokalne snapshoty, diff, historia zmian i digest

### Faza 2 — distress-first

- dołożenie `KRZ`
- lżejsza automatyzacja uruchomień
- retry, logowanie, monitoring zdrowia źródeł
- deduplikacja alertów i korelacja wielu sygnałów

### Faza 3 — pilot product

- `email-first` jako domyślny kanał dostawy
- minimalne konta i dostęp dla użytkowników zewnętrznych
- opcjonalny read-only widok historii zmian
- feedback loop do strojenia alertów

### Po Fazie 3 — dopiero jeśli skala to uzasadni

Do rozważenia później:

- `PostgreSQL`, jeśli SQLite przestanie wystarczać,
- lekka warstwa API,
- mocniejsza orkiestracja zadań,
- konteneryzacja i CI/CD,
- pełniejszy panel webowy.

## Czego świadomie nie używamy na start

| Technologia | Dlaczego nie |
| --- | --- |
| Airflow | za ciężki na pierwszy etap |
| PostgreSQL | niepotrzebny przed sprawdzeniem modelu danych |
| Docker | nie jest warunkiem sensownego startu |
| Panel webowy | digest i historia zmian wystarczą na `v0` |
| ML / NLP do scoringu | za wcześnie, proste reguły wystarczą |

## Struktura projektu (szkic)

```text
kasandra/
├── src/
│   └── kasandra/
│       ├── cli/           # komendy wejściowe
│       ├── sources/       # integracje źródeł
│       ├── processing/    # normalizacja, diff, scoring
│       ├── storage/       # SQLite i warstwa dostępu do danych
│       ├── outputs/       # alerty, digesty, eksport
│       └── config/        # ustawienia i stałe
├── sql/
│   ├── schema/
│   ├── queries/
│   └── migrations/
├── tests/
│   ├── unit/
│   └── integration/
└── var/
    ├── sqlite/
    ├── exports/
    └── tmp/
```

## Otwarte pytania techniczne

- jak przechowywać snapshoty, żeby diff był prosty i czytelny,
- jak daleko upraszczać model danych w `v0`,
- kiedy dokładnie przejść z Fazy 1 do Fazy 2 bez przedwczesnej automatyzacji,
- w którym momencie warto przenieść się z `sqlite3` na większą bazę,
- czy w Fazie 3 wystarczy sam digest z historią zmian, czy potrzebny będzie lekki panel pilotażowy.

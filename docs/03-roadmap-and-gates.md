# Roadmap And Gates

## Jak rozumiec fazy

Fazy sa `gate-based`, nie kalendarzowe. Przejscie dalej ma wynikac z jakosci systemu, a nie z samego uplywu czasu.

## Wspolne artefakty

Do konca `Fazy 0` trzeba zamrozic minimalne kontrakty:

| Artefakt | Minimalny zakres |
| --- | --- |
| model spolki | `internal_id`, `KRS`, `NIP`, `REGON`, `nazwa`, `status`, `notatki` |
| model snapshotu | `company_id`, `source`, `collected_at`, `raw_payload`, `normalized_payload`, `hash` |
| model zmiany | `company_id`, `source`, `field`, `previous_value`, `current_value`, `detected_at`, `change_type` |
| model alertu | `company_id`, `title`, `summary`, `evidence`, `priority`, `recommended_next_step`, `generated_at` |

Przed `Faza 3` glownymi interfejsami pozostaja alert tekstowy, digest i historia zmian. Publiczne API nie jest potrzebne.

## Fazy 0-3

| Faza | Cel | In scope | Gate wyjscia |
| --- | --- | --- | --- |
| `Faza 0` | zamrozic rdzen produktu i danych | seed watchlista `5-10` spolek, kontrakty danych, reczne case studies, pierwsze reguly priorytetu | da sie recznie przejsc `snapshot -> diff -> alert` bez duzej niejednoznacznosci |
| `Faza 1` | dowiezc `v0 / alpha wewnetrzna` | `KRS + CRBR`, lokalne snapshoty, `sqlite3`, diff, historia zmian, digest, prosty CLI, idempotentny rerun | kolejne runy wykrywaja tylko realne zmiany, a alerty sa czytelne |
| `Faza 2` | rozszerzyc system w kierunku distress-first | `KRZ`, retry, monitoring zrodel, deduplikacja alertow, watchlista `25-100` spolek | system dziala stabilnie i nadaje sie do pierwszych pilotowych rozmow |
| `Faza 3` | uruchomic maly pilot produktowy | onboarding watchlisty, regularny digest, minimalny dostep, feedback loop, podstawowe disclaimery | uzytkownicy wracaja do narzedzia przez kilka cykli i daja konkretny feedback |

## Na czym jestesmy teraz

**Faza 1 zamknieta (2026-05-05).** Aktualny punkt to granica Fazy 1 / Fazy 2:

- aktywne zrodla: `KRS + Biala Lista VAT` (scheduler pn-pt 09:00, Windows Task Scheduler),
- CRBR zawieszone — patrz `02-sources-and-alerts.md`,
- gate Fazy 1 spelniony: kolejne runy wykrywaja tylko realne zmiany, alerty sa czytelne,
- nastepny cel: start Fazy 2 — KRZ jako pierwsze rozszerzenie distress-first.

## Najwazniejsze ryzyka

| Ryzyko | Dlaczego boli | Jak ograniczamy |
| --- | --- | --- |
| za duzo scope'u na starcie | rozmywa `v0` i opoznia dzialajacy rdzen | trzymamy `KRS + CRBR` jako jedyny obowiazkowy zakres |
| slaby alert mimo poprawnego diffu | system nie daje realnej wartosci, tylko log zmian | budujemy case studies i prosty, czytelny priorytet |
| problemy z identyfikatorami | zmiany trafiaja do zlej spolki | zamrazamy kontrakt `KRS/NIP/REGON` juz w `Fazie 0` |
| falszywe diffy | reruny staja sie niewiarygodne | rozdzielamy `raw_payload` od `normalized_payload` i testujemy rerun bez zmian |
| niestabilnosc zrodel publicznych | runy przestaja byc powtarzalne | zaczynamy od malej liczby zrodel i dokladamy monitoring zdrowia |
| zbyt wczesna ciezka architektura | spowalnia nauke i rozwoj | `sqlite3`, prosty CLI i lekka orkiestracja pozostaja domyslne |
| rozjazd miedzy dokumentami | agent i czlowiek czytaja sprzeczne zalozenia | ten plik jest glownym zrodlem prawdy dla faz i gate'ow |
| zbyt wczesny pilot | latwo stracic zaufanie do projektu | pilot dopiero po ustabilizowaniu jakosci sygnalu |

## Otwarte pytania

### Teraz (Faza 2)

- czy KRZ ma publiczne API, czy wymaga scrapingu — zbadac przed startem implementacji,
- jak szeroka powinna byc watchlista w Fazie 2 (25-100 spolek) i wedlug jakich kryteriow doboru,
- co zrobic z CRBR przed deadline dostepnosci publicznej (2026-07-01).

### Pozniej

- kiedy KRZ realnie zwieksza wartosc systemu, a kiedy tylko zwieksza szum,
- jaki jest konkretny warunek gotowosci do pilota zewnetrznego,
- czy po Fazie 3 potrzebny jest tylko digest z historia zmian, czy lekki panel.

## Roadmapa wizualna

Szczegoly wizualne sa w:

- `docs/roadmap.mmd`
- `docs/roadmap.svg`
- `docs/roadmap.png`

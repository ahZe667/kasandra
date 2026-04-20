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

Aktualny punkt pracy to `faza 0-1`:

- zakres rdzenia: `KRS + CRBR`,
- priorytet: jakosc diffu, alertu i historii zmian,
- preferowany interfejs: CLI i lokalny run,
- brak zgody na rozlewanie scope'u przed ustabilizowaniem rdzenia.

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

### Teraz

- ktore pola `KRS` i `CRBR` wchodza do rdzenia, a ktore sa tylko kontekstem,
- jak prosty moze byc model danych, zeby nadal dobrze przechowywal historie zmian,
- czy domyslnym formatem `Fazy 1` ma byc digest, pojedynczy alert, czy oba rownolegle,
- jaki poziom recznej pracy w `Fazie 1` jest jeszcze akceptowalny.

### Pozniej

- kiedy `KRZ` realnie zwieksza wartosc systemu, a kiedy tylko zwieksza szum,
- jaki jest konkretny warunek gotowosci do pilota zewnetrznego,
- czy po `Fazie 3` potrzebny jest tylko digest z historia zmian, czy lekki panel.

## Roadmapa wizualna

Szczegoly wizualne sa w:

- `docs/roadmap.mmd`
- `docs/roadmap.svg`
- `docs/roadmap.png`

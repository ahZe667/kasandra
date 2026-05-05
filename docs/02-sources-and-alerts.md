# Sources And Alerts

## Cel

Ten dokument laczy dwie rzeczy, ktore w `v0` musza pozostac spojne:

- z jakich zrodel korzystamy,
- jakie sygnaly i alerty z tych zrodel chcemy wyprowadzac.

## Priorytety zrodel

| Zrodlo | Co monitorujemy | Etap | Uwagi |
| --- | --- | --- | --- |
| KRS | zarzad, prokura, adres, dane rejestrowe | `v0 must` | podstawowe zrodlo zmian formalnych |
| CRBR | beneficjenci rzeczywisci i zmiany wlascicielskie | `zawieszone` | patrz nizej |
| Biala Lista VAT | status VAT i rachunki bankowe | `v1 aktywne` | REST API MF bez autoryzacji; fetch_vat.py + extract_vat.py |
| KRZ | postepowania restrukturyzacyjne i upadlosciowe | `v1` | glowny kandydat do rozszerzenia distress-first |
| ESPI / PAP | raporty biezace i okresowe spolek publicznych | `later` | przydatne, ale zawaza projekt na rynek publiczny |
| GUS / BDL | dane finansowe i statystyczne | `later / context` | dobre jako tlo, slabe jako trigger |

Aktywne zrodla: `KRS` + `Biala Lista VAT`.

## Status CRBR — zawieszone

**Decyzja (2026-04-28):** CRBR zostaje zawieszone jako aktywne zrodlo danych.

**Uzasadnienie:**

Publiczny dostep do portalu CRBR (`crbr.podatki.gov.pl`) konczy sie **2026-07-01**. Po tej dacie dostep wymaga wykazania uzasadnionego interesu prawnego — warunek, ktorego system autonomiczny (CLI, batch run) nie spelnia.

Dotychczasowy mechanizm pobierania opierał sie na Playwright (headless browser omijajacy Imperva WAF), poniewaz:
- SOAP API MF zwraca HTTP 500 dla wszystkich zapytan (10/10 prob w 2026-04);
- REST API portalu jest blokowane przez WAF (zwraca `null` bez sesji JS).

Kontynuowanie integracji CRBR przed Faza 3 nie ma uzasadnienia:
- do 2026-07-01 dziala tylko kruchy scraper Playwright — nie nadaje sie na produkcje;
- po 2026-07-01 publiczny dostep odpada w calosci;
- dane historyczne z CRBR (snapshoty 2026-04) pozostaja w bazie i sa uzyteczne jako baseline.

**Co pozostaje:**
- Snapshoty CRBR z 2026-04 sa zaimportowane do SQLite i moga sluzyc jako tlo historyczne.
- Alerty CRBR (`A-CRBR-*`) pozostaja w kodzie jako usmipione — mozna je reaktywowac jesli pojawi sie legalne API (np. komercyjne).
- Przyszla integracja CRBR wymaga albo licencjonowanego dostepu, albo dostepu przez API z uzasadnieniem — do rozpatrzenia w Fazie 3.

## Kandydaci na kolejne zrodlo

### KRZ — glowny cel Fazy 2

KRZ (`krz.ms.gov.pl`) jest strategicznie wazniejszy niz VAT (distress-first): daje dostep do postepowania upadlosciowych, restrukturyzacyjnych i egzekucyjnych — zdarzen o najwyzszej wartosci operacyjnej dla kancelarii i compliance. Dostep wymaga prawdopodobnie scrapingu (portal oparty o Angular SPA). Warto zbadac dostepnosc API przed startem implementacji.

## Sygnaly v0

W `v0` interesuja nas tylko sygnaly, ktore da sie wiarygodnie wykryc i szybko zinterpretowac:

| Typ sygnalu | Zrodlo | Domyslny priorytet | Komentarz |
| --- | --- | --- | --- |
| postepowanie upadlosciowe / restrukturyzacyjne | `KRS dzial 6` | `krytyczny` | najsilniejszy sygnal distress |
| zaleglosci / egzekucja | `KRS dzial 4` | `krytyczny` | — |
| zmiana prezesa zarzadu | `KRS` | `wysoki` | mocny sygnal organizacyjny |
| zmiana skladu zarzadu | `KRS` | `sredni` | — |
| zmiana wlasciciela / akcjonariusza | `KRS` | `wysoki` | sygnalizuje zmiany struktury |
| zmiana statusu VAT | `Biala Lista VAT` | `wysoki` | utrata VAT to sygnal ostrzegawczy |
| nowe lub usuniete konto bankowe | `Biala Lista VAT` | `sredni` / `wysoki` | przydatne dla compliance |
| zmiana adresu lub danych rejestrowych | `KRS` | `niski` | wazna historycznie, zwykle niepilna |

Wazniejsze od szerokosci katalogu sygnalow jest dobre rozroznienie miedzy szumem a zmiana, ktora realnie zasluguje na uwage.

## Kontrakt alertu

Dobry alert w `v0` powinien zawierac minimum:

| Pole | Znaczenie |
| --- | --- |
| `company_id` | jednoznaczne wskazanie spolki |
| `title` | krotki opis zmiany |
| `summary` | zrozumiale streszczenie diffu |
| `evidence` | zrodlo i porownanie starego z nowym stanem |
| `priority` | `niski`, `sredni`, `podwyzszony` |
| `recommended_next_step` | co warto sprawdzic dalej |
| `generated_at` | kiedy alert powstal |

Alert ma byc interpretacyjny, ale nie kategoryczny. System wskazuje sygnaly do sprawdzenia, nie wydaje formalnej opinii.

## Format dostarczenia

Pierwsza wersja powinna uzywac prostych formatow:

- pojedynczy alert tekstowy,
- digest z lista zmian,
- historia zmian dla konkretnej spolki.

Panel webowy nie jest potrzebny przed udowodnieniem, ze alert i historia zmian sa praktycznie uzyteczne.

## Referencyjne przyklady

- [05-sample-alerts](05-sample-alerts.md)

## Czego nie dokladamy na start

- wielu nowych zrodel tylko po to, zeby zwiekszyc szerokosc projektu,
- scoringu opartego na ciezkiej logice lub ML,
- zrodel, ktore komplikuja model danych bez wzmacniania rdzenia `KRS + VAT`.

# MVP

## Punkt wyjścia

Pierwsza wersja powinna być celowo wąska. Jej celem nie jest budowa pełnej platformy ani szybkie sprawdzanie sprzedaży, tylko dowiezienie działającego rdzenia i zbudowanie użytecznego assetu.

Najlepsze określenie dla tej ścieżki to `v0 / alpha wewnętrzna`, a nie klasyczne MVP sprzedażowe.

## Jak rozumieć fazy 0-3

- fazy są `gate-based`, a nie kalendarzowe,
- każda faza ma własny cel, deliverables i kryterium wyjścia,
- przejście do kolejnej fazy ma wynikać z jakości systemu, a nie z samego upływu czasu,
- ciężar prac opisujemy względnie: `S`, `M`, `M/L`, `L`.

## Kluczowe artefakty i interfejsy

Do końca `Fazy 0` trzeba zamrozić wspólny model dla podstawowych obiektów:

| Artefakt | Minimalny zakres |
| --- | --- |
| Model spółki | `internal_id`, `KRS`, `NIP`, `REGON`, `nazwa`, `status`, `notatki` |
| Model snapshotu | `company_id`, `source`, `collected_at`, `raw_payload`, `normalized_payload`, `hash` |
| Model zmiany | `company_id`, `source`, `field`, `previous_value`, `current_value`, `detected_at`, `change_type` |

Do końca `Fazy 1` trzeba mieć też wspólny model alertu:

| Artefakt | Minimalny zakres |
| --- | --- |
| Model alertu | `company_id`, `title`, `summary`, `evidence`, `priority`, `recommended_next_step`, `generated_at` |

Przed `Fazą 3` nie planujemy publicznego API. Głównym interfejsem pozostają:

- digest,
- historia zmian,
- ewentualnie lekki read-only panel pilotażowy.

## Faza 0 — Definicja rdzenia

| Pole | Ustalenie |
| --- | --- |
| Cel | Usunąć niejasności produktowe i techniczne zanim zacznie się właściwe budowanie. |
| W scope | Seed watchlista `5-10` spółek, lista pól monitorowanych z `KRS` i `CRBR`, modele danych, `2-3` ręczne case studies, pierwsze reguły priorytetu. |
| Deliverables | Lista monitorowanych pól, karta alertu, karta digestu, przykładowa historia zmian, seed watchlista, opis co uznajemy za istotną zmianę. |
| Gate wyjścia | Dla seed watchlisty da się ręcznie przejść od snapshotu do diffu i od diffu do alertu bez dużej niejednoznaczności; zespół ma jedną wersję prawdy dla modelu danych i alertu. |
| Out of scope | Automatyzacja, scheduler, panel, kolejne źródła, rozbudowany scoring. |
| Ryzyka | Zbyt ogólny model danych, brak wspólnej definicji istotnej zmiany, zbyt szeroka watchlista już na starcie. |
| Owner | `product / domain owner` + `tech owner` |
| Relative size | `S` |

## Faza 1 — v0 / alpha wewnętrzna

| Pole | Ustalenie |
| --- | --- |
| Cel | Zautomatyzować rdzeń `KRS + CRBR` i dowieźć działający pipeline do codziennego lub ręcznego użycia wewnętrznego. |
| W scope | Watchlista `10-25` spółek, pobieranie danych z `KRS` i `CRBR`, normalizacja identyfikatorów, zapis snapshotów w `SQLite`, diff zmian, proste priorytety, digest i historia zmian, podstawowe logowanie, idempotentny rerun. |
| Deliverables | Działający CLI/manual run, lokalna baza snapshotów, raport zmian per spółka, digest zbiorczy, kilka powtarzalnych runów bez ręcznego sklejania danych. |
| Gate wyjścia | Dwa-trzy kolejne uruchomienia na tej samej watchliście wykrywają tylko realne zmiany; alerty są czytelne; historia zmian ma wartość praktyczną; pipeline nie rozpada się przy braku zmian lub częściowym błędzie źródła. |
| Out of scope | `KRZ`, API, pełny panel, rozbudowane uprawnienia, ciężka orkiestracja. |
| Ryzyka | Fałszywe diffy, słabe mapowanie identyfikatorów, zbyt ręczne operowanie pipeline'em, za duży koszt utrzymania przy prostych zmianach źródeł. |
| Owner | `tech owner` |
| Relative size | `M` |

## Faza 2 — Rozszerzenie distress-first

| Pole | Ustalenie |
| --- | --- |
| Cel | Pogłębić wartość systemu i zwiększyć jego stabilność bez przeskoku w ciężką architekturę. |
| W scope | Integracja `KRZ`, korelacja zmian z wielu źródeł w krótkim czasie, lżejsza automatyzacja uruchomień, retry i lepsze logowanie, deduplikacja alertów, bardziej użyteczna historia zmian, watchlista `25-100` spółek. |
| Deliverables | Stabilny run półautomatyczny, alerty łączące `KRS + CRBR + KRZ`, wyraźne sygnały kryzysowe, prosty monitoring zdrowia źródeł i jakości danych. |
| Gate wyjścia | System działa bez ręcznego pilnowania każdego runu; `KRZ` wnosi realną wartość sygnałową; liczba alertów jest kontrolowalna; materiał nadaje się do pokazania pierwszym pilotowym użytkownikom. |
| Out of scope | `ESPI/PAP`, Biała Lista VAT jako domyślna ścieżka, public API, pełna aplikacja produktowa. |
| Ryzyka | Nadmierny wzrost szumu po dołożeniu `KRZ`, zbyt szybkie wejście w automatyzację, problemy z deduplikacją sygnałów i stabilnością runów. |
| Owner | `tech owner` + `data / operations owner` |
| Relative size | `M/L` |

## Faza 3 — Pilot product

| Pole | Ustalenie |
| --- | --- |
| Cel | Wypuścić mały produkt pilotażowy dla wąskiej grupy użytkowników zewnętrznych, bez rozlewania scope'u. |
| Docelowy odbiorca | `1-2` organizacje albo `3-5` użytkowników z obszaru restrukturyzacji, prawa lub analizy specjalistycznej. |
| W scope | Onboarding watchlisty, regularny digest, historia zmian dostępna poza zespołem, minimalne konta i dostęp, feedback loop do strojenia alertów, podstawowe disclaimery i opis interpretacji danych. |
| Deliverables | Działający pilot z prawdziwymi użytkownikami, regularna dostawa alertów, kanał feedbacku, lista najczęstszych braków i decyzji potrzebnych do wejścia w pełniejszy produkt. |
| Gate wyjścia | Pilotowi użytkownicy wracają do narzędzia przez kilka cykli; feedback jest wystarczająco konkretny, żeby podjąć decyzję o dalszej produktizacji, a nie tylko o dalszym eksperymencie. |
| Out of scope | Szeroka sprzedaż, marketplace integracji, duży frontend, wieloźródłowy kombajn danych. |
| Ryzyka | Rozlanie scope'u pod pierwszych użytkowników, budowa zbyt dużego panelu, próba wejścia w sprzedaż przed ustabilizowaniem jakości alertów. |
| Owner | `product owner` + `pilot owner` + `tech owner` |
| Relative size | `L` |

## Jak oceniamy Fazę 0 i Fazę 1

Na tym etapie ocena postępu nie dotyczy głównie ceny ani sprzedaży. Chodzi raczej o sprawdzenie, czy rdzeń systemu jest faktycznie użyteczny i czy buduje sensowny asset.

Najważniejsze pytania na tym etapie:

- czy pipeline działa powtarzalnie,
- czy diff zmian jest czytelny,
- czy alert daje sensowny kontekst interpretacyjny,
- czy historia zmian zaczyna być użyteczna sama w sobie,
- czy projekt buduje know-how i IP warte dalszego rozwijania.

Pozytywny sygnał dla `Fazy 0-1`:

- system wykrywa zmiany bez dużej ręcznej korekty,
- alerty da się czytać szybko i bez wracania do źródeł za każdym razem,
- kolejne uruchomienia dają porównywalne wyniki,
- zebrane dane i logika interpretacji mają wartość także poza pojedynczym eksperymentem.

Walidacja zewnętrzna pojawia się później, dopiero gdy system zacznie działać sensownie także jako narzędzie wewnętrzne.

## Test plan i scenariusze

### Faza 0

- ręcznie przejść pojedynczą zmianę `KRS`,
- ręcznie przejść pojedynczą zmianę `CRBR`,
- ręcznie przejść zmianę łączoną `KRS + CRBR`.

### Faza 1

- rerun bez zmian,
- rerun z jedną zmianą,
- brak odpowiedzi jednego źródła,
- duplikat identyfikatora,
- spółka z niepełnymi danymi.

### Faza 2

- scenariusz `KRZ` bez zmian w `KRS/CRBR`,
- scenariusz skorelowany `KRS + CRBR + KRZ`,
- awaria runu i odzyskanie stanu,
- deduplikacja podobnych alertów.

### Faza 3

- onboarding nowej watchlisty,
- poprawność dostawy digestu,
- dostęp użytkownika do historii zmian,
- obsługa feedbacku i aktualizacja reguł alertowych bez rozbijania wcześniejszych danych.

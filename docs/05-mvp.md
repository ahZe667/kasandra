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

### Backlog wykonawczy Fazy 0

Faza 0 powinna zostać dowieziona jako seria małych, domkniętych slice'ów dokumentacyjno-analitycznych. Na tym etapie nie budujemy jeszcze automatyzacji, schedulera ani docelowych integracji produkcyjnych. Celem jest zamrożenie kontraktów i ręczne przejście ścieżki `snapshot -> diff -> alert` dla `KRS + CRBR`.

#### Zasady operacyjne

- jeden slice = jeden mały commit
- priorytet mają źródła prawdy w `docs/` i `examples/`
- każdy slice musi kończyć się artefaktem, który będzie bezpośrednio użyty w `Fazie 1`
- jeśli zmienia się kontrakt alertu, digestu albo historii zmian, trzeba zsynchronizować `examples/`

#### Epic 0.1 — Zamrożenie zakresu źródeł i pól

Cel: ustalić minimalny, stabilny zakres `KRS + CRBR`, bez dokładania pól tylko "na wszelki wypadek".

Taski:

- zamrozić listę pól monitorowanych z `KRS`
- zamrozić listę pól monitorowanych z `CRBR`
- dopisać, które pola są tylko kontekstem i nie wchodzą jeszcze do diffu
- opisać, co uznajemy za istotną zmianę, a co tylko za zmianę historyczną o niskim priorytecie

Definition of done:

- `docs/02-data-sources.md`, `docs/03-signals-and-alerts.md` i `docs/05-mvp.md` mówią jednym głosem o zakresie `Fazy 0`
- zespół potrafi wskazać, które pola wchodzą do rdzenia bez odwoływania się do interpretacji ad hoc

Proponowany commit:

- `docs(sources): freeze phase-0 monitored fields`

#### Epic 0.2 — Seed watchlista i identyfikatory

Cel: przygotować małą watchlistę referencyjną i jedną wersję prawdy dla identyfikatorów spółki.

Taski:

- wybrać seed watchlistę `5-10` spółek
- dopisać kryteria doboru spółek do watchlisty
- ustalić minimalny kontrakt identyfikatorów: `KRS`, `NIP`, `REGON`, `nazwa`, `status`, `notatki`
- opisać zasady pracy z brakami albo rozjazdami identyfikatorów między źródłami

Definition of done:

- istnieje jedna referencyjna watchlista do `Fazy 0`
- wiadomo, jak przypisać snapshot i zmianę do właściwej spółki bez ręcznej interpretacji w każdym case'ie

Proponowany commit:

- `docs(scope): define phase-0 seed watchlist`

#### Epic 0.3 — Model danych i kontrakt snapshotu

Cel: zamrozić minimalne encje rdzenia, zanim powstanie kod i SQLite schema dla `Fazy 1`.

Taski:

- doprecyzować model spółki
- doprecyzować model snapshotu z rozdzieleniem `raw_payload` i `normalized_payload`
- doprecyzować model zmiany z polami potrzebnymi do historii i evidence trail
- opisać rolę `hash` oraz zasady normalizacji danych przed porównaniem

Definition of done:

- model spółki, snapshotu i zmiany jest jednoznaczny dla warstw `sources`, `processing`, `storage` i `outputs`
- wiadomo, które dane mają być przechowywane surowo, a które w formie znormalizowanej

Proponowany commit:

- `docs(models): freeze phase-0 core entities`

#### Epic 0.4 — Diff, priorytet i formaty wyjściowe

Cel: ustalić, jak z ręcznie zebranych snapshotów powstaje czytelna zmiana, alert i digest.

Taski:

- opisać reguły diffu dla `KRS` i `CRBR`
- zamrozić podstawowe `change_type`
- opisać pierwsze reguły priorytetu: `niski`, `średni`, `podwyższony`
- doprecyzować kartę alertu, kartę digestu i minimalny format historii zmian
- zsynchronizować przykłady alertów z ustalonym kontraktem

Definition of done:

- dla każdej zmiany z rdzenia da się wskazać pole, źródło, poprzednią wartość, nową wartość i priorytet
- alert nie brzmi jak suchy log i nie wpada w nadinterpretację

Proponowany commit:

- `docs(alerts): define phase-0 diff and priority rules`

#### Epic 0.5 — Ręczne case studies i gate do Fazy 1

Cel: przejść ręcznie pełny przepływ dla reprezentatywnych przypadków i zamknąć niejasności przed automatyzacją.

Taski:

- przygotować case `KRS-only`
- przygotować case `CRBR-only`
- przygotować case łączony `KRS + CRBR`
- opisać wynik w formacie: stan poprzedni, stan nowy, diff, alert, rekomendowany następny krok
- zamknąć listę otwartych pytań, które realnie blokują wejście do `Fazy 1`

Definition of done:

- dla seed watchlisty da się ręcznie przejść `snapshot -> diff -> alert` bez dużej niejednoznaczności
- istnieją co najmniej `2-3` case studies, które da się wykorzystać później jako testy referencyjne i przykłady repo

Proponowany commit:

- `docs(examples): add phase-0 validation cases`

#### Proponowana kolejność slice'ów

1. `docs(sources): freeze phase-0 monitored fields`
2. `docs(scope): define phase-0 seed watchlist`
3. `docs(models): freeze phase-0 core entities`
4. `docs(alerts): define phase-0 diff and priority rules`
5. `docs(examples): add phase-0 validation cases`

#### Gate review przed wejściem do Fazy 1

Przed startem `Fazy 1` trzeba umieć odpowiedzieć twierdząco na wszystkie pytania:

- czy lista pól `KRS + CRBR` jest zamrożona i nie ma w niej oczywistego szumu
- czy model spółki, snapshotu i zmiany jest wystarczająco prosty do wdrożenia w `SQLite`
- czy seed watchlista daje `2-3` sensowne case studies
- czy alert, digest i historia zmian mają już czytelny kontrakt
- czy ręczny rerun tych samych danych nie generuje sztucznych różnic na poziomie definicji
- czy otwarte pytania po `Fazie 0` nie blokują rozpoczęcia automatyzacji w `Fazie 1`

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

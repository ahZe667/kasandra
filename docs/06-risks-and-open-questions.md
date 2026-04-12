# Risks and Open Questions

## Ryzyka

### Produktowe

#### 1. Za dużo scope'u już na starcie

To ryzyko jest istotne, bo projekt ma sens tylko wtedy, gdy najpierw dowiezie wąski, działający rdzeń. Zbyt szybkie dokładanie źródeł, formatów i use-case'ów może rozmyć `v0`.

Jak ograniczamy:

- trzymamy `KRS + CRBR` jako jedyny obowiązkowy zakres rdzenia,
- oceniamy nowe pomysły przez pryzmat wpływu na diff, alert i historię zmian,
- odkładamy rzeczy "nice to have", jeśli nie poprawiają rdzenia.

Sygnały ostrzegawcze:

- backlog rośnie szybciej niż liczba działających scenariuszy end-to-end,
- dokumentacja zaczyna mówić o wielu kierunkach naraz,
- zespół nie umie jasno powiedzieć, co dokładnie musi wejść do `Fazy 1`.

#### 2. Niska jakość interpretacji zmian mimo poprawnego diffu

Sam diff nie wystarczy, jeśli alert nie odpowiada na pytanie, czy zmiana jest warta uwagi. To jedno z głównych ryzyk dla całego sensu projektu.

Jak ograniczamy:

- budujemy ręczne case studies już w `Fazie 0`,
- upraszczamy scoring do kilku czytelnych reguł,
- opis alertu opieramy na faktach i krótkiej interpretacji, nie na silnych tezach.

Sygnały ostrzegawcze:

- alerty brzmią jak suche logi zmian,
- użytkownik nadal musi wracać do źródeł, żeby zrozumieć sens sygnału,
- kilka zmian wygląda podobnie, mimo że mają inną wartość praktyczną.

#### 3. Budowanie demo zamiast użytecznego narzędzia

Jest pokusa, żeby optymalizować pod wygląd i prezentację, zanim system stanie się naprawdę użyteczny. To byłby zły trade-off na obecnym etapie.

Jak ograniczamy:

- priorytet dajemy historii zmian, jakości snapshotu i powtarzalności runu,
- panel i cięższe elementy interfejsu zostają poza `Fazą 1`,
- kryterium jakości to użyteczność pipeline'u, nie efekt demo.

Sygnały ostrzegawcze:

- więcej czasu idzie w warstwę prezentacyjną niż w dane i diff,
- pojawiają się funkcje potrzebne głównie "żeby dobrze pokazać produkt",
- dokumentacja produktu zaczyna wyprzedzać realne możliwości systemu.

### Operacyjne

#### 1. Problemy z łączeniem identyfikatorów spółek między źródłami

Jeśli mapowanie `KRS`, `NIP`, `REGON` i nazwy będzie słabe, to historia zmian i alerty szybko stracą wiarygodność.

Jak ograniczamy:

- zamrażamy wspólny model spółki w `Fazie 0`,
- pilnujemy jednej wersji prawdy dla identyfikatorów,
- testujemy przypadki niepełnych lub rozjechanych danych już w `Fazie 1`.

Sygnały ostrzegawcze:

- jedna spółka pojawia się pod kilkoma rekordami,
- zmiany trafiają do złej historii spółki,
- ręczne poprawki identyfikatorów stają się częste.

#### 2. Słaba jakość snapshotów utrudniająca porównywanie stanów

Jeśli snapshot jest niestabilny albo zbyt surowy, system będzie generował fałszywe różnice albo gubił istotne zmiany.

Jak ograniczamy:

- rozdzielamy `raw_payload` od `normalized_payload`,
- pilnujemy spójnego modelu snapshotu i hashowania,
- testujemy rerun bez zmian jako obowiązkowy scenariusz.

Sygnały ostrzegawcze:

- system pokazuje zmiany przy danych, które faktycznie się nie zmieniły,
- kolejne uruchomienia dają niespójne wyniki,
- diff staje się trudny do czytania i debugowania.

#### 3. Duża ilość ręcznej pracy mimo rosnącej automatyzacji

Na początku ręczna praca jest akceptowalna, ale jeśli pozostanie wysoka zbyt długo, to projekt nie zbuduje skali ani stabilności.

Jak ograniczamy:

- w `Fazie 1` pilnujemy idempotentnego rerunu i prostego manual run / CLI,
- w `Fazie 2` dokładamy lekką automatyzację dopiero tam, gdzie naprawdę usuwa tarcie,
- obserwujemy, które czynności są powtarzalne i nadają się do automatyzacji.

Sygnały ostrzegawcze:

- każdy run wymaga ręcznego doglądania,
- poprawki operacyjne zabierają więcej czasu niż rozwój systemu,
- wdrożenie nowej spółki na watchlistę jest kosztowne i podatne na błędy.

#### 4. Niestabilność źródeł publicznych

To ryzyko jest fundamentalne: layouty, odpowiedzi i dostępność źródeł publicznych mogą się zmieniać bez ostrzeżenia.

Jak ograniczamy:

- zaczynamy od małej liczby źródeł,
- dodajemy proste logowanie i kontrolę jakości odpowiedzi,
- w `Fazie 2` dokładamy retry i monitoring zdrowia źródeł.

Sygnały ostrzegawcze:

- nagły wzrost błędów pobierania,
- puste lub niekompletne snapshoty,
- częste ręczne poprawki parserów.

### Rozwojowe

#### 1. Zbyt wczesne wejście w ciężką architekturę

Projekt na obecnym etapie nie potrzebuje jeszcze dużej infrastruktury. Za wczesne wejście w cięższe rozwiązania zwiększy koszt i spowolni uczenie się.

Jak ograniczamy:

- `sqlite3`, manual run i prosty CLI pozostają domyślną ścieżką na `Fazę 1`,
- cięższe elementy wchodzą dopiero po realnym bólu skali lub stabilności,
- dokumentacja techniczna pozostaje podporządkowana fazom 0-3.

Sygnały ostrzegawcze:

- pojawia się potrzeba wdrażania infrastruktury, której system jeszcze nie uzasadnia,
- architektura zaczyna być bardziej rozbudowana niż katalog realnych use-case'ów,
- decyzje techniczne są podejmowane "na zapas".

#### 2. Rozjazd między dokumentacją a faktycznym zakresem faz

Im bardziej szczegółowy robi się plan, tym łatwiej o niespójności między `Overview`, `MVP`, `Tech Stack`, roadmapą i faktycznym działaniem systemu.

Jak ograniczamy:

- traktujemy `05-mvp` jako główną definicję faz 0-3,
- aktualizujemy roadmapę i dokumenty towarzyszące przy większych zmianach zakresu,
- nie dodajemy nowych kierunków bez jasnego umieszczenia ich w fazach.

Sygnały ostrzegawcze:

- dwa dokumenty inaczej opisują ten sam etap,
- nie wiadomo, czy coś należy do `Fazy 1`, `Fazy 2` czy jest tylko pomysłem,
- roadmapa staje się bardziej aspiracyjna niż operacyjna.

#### 3. Rozbudowa w wielu kierunkach naraz bez jasnego rdzenia

Po `Fazie 1` łatwo wejść jednocześnie w `KRZ`, pilot, panel, automatyzację i nowe persony. To grozi utratą priorytetów.

Jak ograniczamy:

- pierwszy obowiązkowy kierunek po rdzeniu to `distress-first` i `KRZ`,
- pilot zewnętrzny pojawia się dopiero po ustabilizowaniu jakości sygnału,
- nowe źródła oceniamy przez wpływ na konkretny use-case, nie przez atrakcyjność listy funkcji.

Sygnały ostrzegawcze:

- zespół pracuje równolegle nad wieloma niezależnymi torami,
- brakuje jasnego kryterium wejścia do `Fazy 2` i `Fazy 3`,
- liczba niedomkniętych eksperymentów rośnie.

### Prawne i źródłowe

#### 1. Nadinterpretacja alertów

System ma wskazywać sygnały, a nie wydawać formalne oceny prawne lub finansowe. Jeśli komunikacja będzie zbyt kategoryczna, ryzyko reputacyjne i prawne rośnie.

Jak ograniczamy:

- opieramy alerty na faktach i zmianach,
- unikamy zbyt daleko idących ocen sytuacji spółki,
- w `Fazie 3` dodajemy proste disclaimery i opis charakteru informacji.

Sygnały ostrzegawcze:

- alert brzmi jak gotowy wniosek, a nie hipoteza do sprawdzenia,
- użytkownik może odczytać komunikat jako formalną opinię,
- opis interpretacji wykracza poza to, co wynika z danych.

#### 2. Ograniczenia źródeł, regulaminów i dostępu

Nawet publiczne źródła mogą mieć ograniczenia praktyczne lub regulaminowe dotyczące intensywności odpytywania, sposobu wykorzystania danych albo dalszego udostępniania.

Jak ograniczamy:

- traktujemy źródła jako obszar do bieżącej weryfikacji, nie jako stałe założenie,
- zaczynamy od małej skali i małej częstotliwości runów,
- przed pilotem sprawdzamy, czy sposób wykorzystania danych nie wymaga dodatkowych założeń lub ograniczeń.

Sygnały ostrzegawcze:

- pojawiają się blokady, rate limiting albo niestandardowe odpowiedzi,
- źródła przestają reagować stabilnie przy większej częstotliwości,
- pojawia się wątpliwość, czy dane można bezpiecznie pokazywać dalej w pilocie.

#### 3. Ryzyko błędnego alertu

Fałszywy lub źle przypisany alert może podważyć zaufanie do systemu szybciej niż brak kolejnej funkcji.

Jak ograniczamy:

- priorytetem jest poprawność przypisania zmiany do spółki i czytelny evidence trail,
- testujemy scenariusze z brakami danych i błędami źródeł,
- przed pilotem przygotowujemy możliwość szybkiej korekty lub wycofania alertu.

Sygnały ostrzegawcze:

- użytkownik nie widzi, skąd wynika alert,
- trudno odtworzyć drogę od źródła do interpretacji,
- pojedynczy błąd alertu wymaga ręcznego dochodzenia bez śladu w systemie.

### Pilotowe i reputacyjne

#### 1. Wejście w pilot zbyt wcześnie

Pilot ma sens dopiero wtedy, gdy system jest wystarczająco stabilny i czytelny. Zbyt wczesne pokazanie narzędzia na zewnątrz może dać zły sygnał o jakości projektu.

Jak ograniczamy:

- trzymamy się gate'ów z `Fazy 2`,
- nie pokazujemy pilota, jeśli alerty są nadal zbyt szumne,
- najpierw domykamy jakość historii zmian, digestu i powtarzalności runu.

Sygnały ostrzegawcze:

- zespół nadal ręcznie tłumaczy każdy alert,
- pilot wymagałby ukrywania wielu ograniczeń systemu,
- nie ma jeszcze jasnego kryterium gotowości do użycia zewnętrznego.

#### 2. Rozlanie scope'u pod pierwszych użytkowników

Pierwsi użytkownicy zewnętrzni łatwo wygenerują listę życzeń, która może rozbić spójność produktu.

Jak ograniczamy:

- pilot opisujemy jako wąski i eksperymentalny,
- feedback zbieramy, ale nie zamieniamy go automatycznie w roadmapę,
- pilnujemy jednego głównego use-case'u i jednego domyślnego formatu dostawy.

Sygnały ostrzegawcze:

- każdy użytkownik dostaje inny wariant produktu,
- pojawia się wiele wyjątków i ręcznych obejść,
- backlog pilota zaczyna dominować nad rdzeniem systemu.

#### 3. Utrata zaufania przez niską jakość dostawy

Nawet dobry alert traci wartość, jeśli digest dochodzi nieregularnie, historia zmian jest trudna do odczytania albo feedback znika bez reakcji.

Jak ograniczamy:

- `email-first` traktujemy jako świadomie prosty, ale stabilny kanał,
- pilnujemy powtarzalności dostawy,
- w `Fazie 3` budujemy prosty feedback loop i reagujemy na najważniejsze błędy jakościowe.

Sygnały ostrzegawcze:

- użytkownicy przestają wracać do digestów,
- feedback dotyczy głównie niezawodności i nieczytelności,
- trudno powiedzieć, które alerty rzeczywiście miały wartość.

## Otwarte pytania

### Na teraz (Fazy 0-1)

- jak dokładnie wyznaczyć granicę między użytecznym sygnałem a nadinterpretacją,
- które pola z `KRS` i `CRBR` naprawdę warto monitorować już w rdzeniu, a które tylko komplikują model,
- jak prosty może być model danych, żeby nadal dobrze przechowywał historię zmian,
- czy domyślnym formatem `Fazy 1` ma być digest, pojedynczy alert, czy oba równolegle,
- jaki poziom ręcznej pracy w `Fazie 1` jest jeszcze akceptowalny.

### Przed Fazą 2

- jaki jest konkretny warunek przejścia z `Fazy 1` do `Fazy 2`,
- kiedy `KRZ` rzeczywiście zwiększa wartość systemu, a kiedy tylko zwiększa szum,
- jak łączyć sygnały z wielu źródeł bez budowania zbyt złożonego scoringu,
- jaki poziom automatyzacji jest sensowny, zanim pojawi się potrzeba cięższej infrastruktury,
- jak mierzyć jakość alertów po dołożeniu `KRZ` i deduplikacji.

### Przed Fazą 3

- jaki jest konkretny warunek gotowości do pilota zewnętrznego,
- czy pilot powinien być `digest-only`, czy jednak potrzebuje lekkiego widoku historii zmian,
- jakie zasady korzystania z danych i ich dalszego udostępniania trzeba przyjąć przed pilotem,
- jak opisać interpretacyjny charakter alertów, żeby nie brzmiały jak formalna opinia,
- jakiego rodzaju feedback z pilota uznamy za wystarczający do wejścia w dalszą produktizację.

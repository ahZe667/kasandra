# Sample Company Cases

## Jak czytać te case'y

Case'y nie mają udowadniać, że system już "wie", co dzieje się ze spółką. Ich celem jest pokazanie:

- jaki był stan wyjściowy,
- co system wykrył,
- jak wygląda różnica między snapshotami,
- jak może brzmieć notatka interpretacyjna,
- jaki alert albo digest z tego powstaje.

## Case 1 — zmiana formalna i właścicielska w krótkim odstępie

### Case 1: stan wyjściowy

Na watchliście znajduje się `ABC Sp. z o.o.`. W poprzednim snapshotcie:

- w `KRS` widniał jednoosobowy zarząd,
- w `CRBR` wpisany był jeden beneficjent rzeczywisty,
- historia zmian dla spółki była pusta.

### Case 1: wykryta zmiana

W kolejnym uruchomieniu systemu:

- `KRS` pokazuje nowy skład zarządu,
- `CRBR` pokazuje zmianę beneficjenta rzeczywistego,
- oba zdarzenia pojawiają się w krótkim odstępie czasu.

### Case 1: notatka interpretacyjna

Pojedyncza zmiana formalna nie musi znaczyć wiele. Połączenie zmiany zarządu i beneficjenta rzeczywistego jest jednak warte odnotowania, bo może oznaczać istotną zmianę właścicielską albo reorganizację spółki.

W `v0` nie chodzi jeszcze o kategoryczny wniosek, tylko o to, żeby taki zestaw zmian został:

- poprawnie wykryty,
- zapisany w historii,
- podniesiony w priorytecie względem zwykłego, pojedynczego eventu.

### Case 1: wynikowy alert

> ABC Sp. z o.o. - wykryto zmianę zarządu w KRS oraz nowego beneficjenta rzeczywistego w CRBR. Zestaw zmian o podwyższonym priorytecie do dalszej weryfikacji.

### Case 1: wynik w digescie

W tygodniowym digescie spółka pojawia się jako jedna pozycja z dwoma powiązanymi zmianami i krótkim komentarzem: `zmiana formalna + właścicielska w krótkim czasie`.

## Case 2 — zmiana niskiego priorytetu, która ma wartość głównie historyczną

### Case 2: stan wyjściowy

Na watchliście znajduje się `Nova Sp. z o.o.`. W historii zmian są już wcześniejsze wpisy dotyczące zarządu i prokury, ale od kilku tygodni nie było istotnych aktualizacji.

### Case 2: wykryta zmiana

W nowym snapshotcie:

- `KRS` pokazuje zmianę adresu siedziby,
- `CRBR` pozostaje bez zmian.

### Case 2: notatka interpretacyjna

To typ zmiany, który sam w sobie rzadko powinien uruchamiać pilną reakcję. Mimo to warto go zachować, bo:

- domyka historię zmian spółki,
- może być kontekstem dla późniejszych zdarzeń,
- pokazuje, że system nie gubi drobniejszych, ale realnych aktualizacji.

### Case 2: wynikowy alert

> Nova Sp. z o.o. - w KRS wykryto aktualizację adresu siedziby. Zmiana formalna o niskim priorytecie, do zapisania w historii bez potrzeby pilnej reakcji.

### Case 2: wynik w digescie

W digescie ta spółka może pojawić się w sekcji `niski priorytet` albo zostać pokazana dopiero w pełnej historii zmian.

## Case 3 — zmiana właścicielska bez równoległej aktualizacji w KRS

### Case 3: stan wyjściowy

Na watchliście jest `Delta Sp. z o.o.`. Poprzedni snapshot nie pokazywał żadnych zmian w ostatnich dwóch runach.

### Case 3: wykryta zmiana

W kolejnym uruchomieniu:

- `CRBR` pokazuje zmianę beneficjenta rzeczywistego,
- `KRS` nie pokazuje jeszcze odpowiadającej temu zmiany formalnej.

### Case 3: notatka interpretacyjna

To dobry case pokazujący, że źródła nie muszą aktualizować się synchronicznie. System nie powinien traktować tego jako sprzeczności, tylko jako zmianę wartą obserwacji w następnym cyklu.

### Case 3: wynikowy alert

> Delta Sp. z o.o. - w CRBR wykryto zmianę beneficjenta rzeczywistego, ale w aktualnym snapshotcie KRS nie widać jeszcze zmian formalnych. Zmiana o średnim priorytecie; warto obserwować kolejne uruchomienie.

### Case 3: wynik w digescie

Digest może opisać ten przypadek komentarzem: `zmiana właścicielska wykryta wcześniej niż odpowiadająca jej aktualizacja formalna`.

## Case 4 — kilka zmian w jednej spółce w ramach tygodnia

### Case 4: stan wyjściowy

Na watchliście znajduje się `Omega Sp. z o.o.`. System uruchamiany jest kilka razy w tygodniu, a historia zmian ma już kilka starszych wpisów.

### Case 4: wykryta zmiana

W jednym tygodniu system wykrywa:

- nowego prokurenta w `KRS`,
- później zmianę beneficjenta rzeczywistego w `CRBR`.

### Case 4: notatka interpretacyjna

Pojedynczo te zmiany nie muszą być alarmujące, ale razem są już dobrym kandydatem do zagregowania w jeden wpis digestu. To ważny case dla późniejszej logiki grupowania alertów.

### Case 4: wynikowy alert

> Omega Sp. z o.o. - w ostatnim tygodniu wykryto nowego prokurenta w KRS oraz zmianę beneficjenta rzeczywistego w CRBR. Zbiorczy alert o podwyższonym priorytecie do dalszej analizy.

### Case 4: wynik w digescie

Spółka pojawia się jako jedna pozycja z krótkim podsumowaniem tygodnia: `zmiana organizacyjna + zmiana właścicielska`.

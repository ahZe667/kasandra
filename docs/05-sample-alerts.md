# Sample Alerts

## Cel

Ten dokument zbiera referencyjne przyklady alertow dla `Fazy 1 / v0`, czyli dla systemu opartego glownie na `KRS` i `CRBR`.

W tej fazie interesuje nas nie tylko finalna tresc alertu, ale tez krotkie przejscie od `snapshot -> diff -> alert`, zeby bylo jasne, dlaczego dany komunikat ma taki priorytet i sugerowany dalszy krok.

Przyklady dla dalszych faz sa w trakcie prac.

## Jak czytac te przyklady

Kazdy przyklad zawiera:

- finalny alert, czyli docelowy output dla uzytkownika,
- `Case`, czyli minimalny kontekst zmiany miedzy poprzednim a nowym stanem,
- `Interpretacja`, czyli dlaczego alert ma taki priorytet albo trafia do digesta.

Kazdy alert w `Fazie 1` powinien:

- wskazywac spolke,
- pokazywac zrodlo zmiany,
- streszczac diff wzgledem poprzedniego stanu,
- sugerowac priorytet i dalszy krok.

## Przyklad 1 - pojedyncza zmiana formalna

> ABC Sp. z o.o. - KRS: ze skladu zarzadu usunieto Jana Kowalskiego, dodano Anne Nowak. Priorytet: sredni. Dalszy krok: sprawdzic, czy zmiana wplywa na reprezentacje spolki i uprawnienia do podpisu.

- `Case`: poprzedni stan to jednoosobowy zarzad z Janem Kowalskim; nowy stan zawiera Anne Nowak zamiast Jana Kowalskiego.
- `Interpretacja`: to konkretna zmiana formalna z `KRS`, istotna operacyjnie, ale bez podstaw do automatycznej eskalacji ponad poziom `sredni`.

## Przyklad 2 - pojedyncza zmiana wlascicielska

> XYZ Sp. z o.o. - CRBR: dodano nowego beneficjenta rzeczywistego, Piotra Wisniewskiego; w poprzednim snapshotcie nie wystepowal. Priorytet: sredni. Dalszy krok: zapisac zmiane w historii i porownac ja z kolejnym snapshotem KRS.

- `Case`: poprzedni stan zawieral jednego beneficjenta rzeczywistego; nowy snapshot `CRBR` pokazuje dodatkowa osobe.
- `Interpretacja`: sama zmiana wlascicielska jest istotna, ale bez rownoleglego sygnalu z `KRS` nie ma jeszcze podstaw do priorytetu `podwyzszony`.

## Przyklad 3 - zmiana laczona

> Firma 123 Sp. z o.o. - KRS i CRBR: w KRS dodano nowego czlonka zarzadu, a w CRBR zmienil sie beneficjent rzeczywisty. Priorytet: podwyzszony. Dalszy krok: zweryfikowac, czy zmiany sa powiazane i czy nie oznaczaja przejecia kontroli nad spolka.

- `Case`: poprzedni stan byl stabilny; nowy stan pokazuje zmiane zarzadu w `KRS` i zmiane beneficjenta rzeczywistego w `CRBR` w krotkim odstepie.
- `Interpretacja`: korelacja zmian z dwoch zrodel wzmacnia sygnal i uzasadnia szybsza weryfikacje.

## Przyklad 4 - zmiana niskiego priorytetu

> Nova Sp. z o.o. - KRS: zmieniono adres siedziby z ul. A 10, Warszawa na ul. B 12, Warszawa. Priorytet: niski. Dalszy krok: zapisac zmiane w historii bez eskalacji.

- `Case`: brak innych zmian w ostatnich runach; nowy snapshot `KRS` zawiera tylko aktualizacje danych rejestrowych.
- `Interpretacja`: zmiana jest wazna historycznie, ale zwykle nie oznacza istotnej zmiany ryzyka ani kontroli nad spolka.

## Przyklad 5 - niespojnosc miedzy zrodlami

> Delta Sp. z o.o. - CRBR i KRS: w CRBR pojawil sie nowy beneficjent rzeczywisty, ale w aktualnym snapshotcie KRS brak odpowiadajacej zmiany formalnej. Priorytet: podwyzszony. Dalszy krok: obserwowac kolejny run i oznaczyc alert jako oczekujacy na potwierdzenie.

- `Case`: poprzedni stan nie zawieral istotnych zmian; nowy `CRBR` pokazuje zmiane beneficjenta, a `KRS` pozostaje bez zmian formalnych.
- `Interpretacja`: niesynchronicznosc zrodel sama w sobie nie jest bledem, ale jest dobrym sygnalem do obserwacji i recznej weryfikacji.

## Przyklad 6 - kandydat do digesta

> Omega Sp. z o.o. - w ostatnim tygodniu wykryto nowego prokurenta w KRS oraz pozniejsza zmiane beneficjenta rzeczywistego w CRBR. Zbiorczy wpis do digesta o podwyzszonym priorytecie do dalszej analizy.

- `Case`: spolka ma juz historie starszych wpisow; w biezacym tygodniu pojawily sie dwie rozne zmiany w dwoch kolejnych runach.
- `Interpretacja`: to dobry kandydat do zagregowanego wpisu, bo wartosc wynika z sekwencji zmian, a nie z pojedynczego zdarzenia.

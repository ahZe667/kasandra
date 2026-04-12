# Sample Alerts

## Jak czytać te przykłady

Poniższe alerty są przykładami dla `v0 / Fazy 1`, czyli dla systemu opartego głównie na `KRS` i `CRBR`.

Każdy alert powinien:

- wskazywać spółkę,
- pokazywać źródło zmiany,
- streszczać różnicę względem poprzedniego stanu,
- sugerować priorytet i dalszy krok.

## Przykład 1 — pojedyncza zmiana formalna

> ABC Sp. z o.o. - w KRS wykryto zmianę składu zarządu. Poprzednio spółka miała jednego członka zarządu, obecnie widoczna jest nowa osoba. Zmiana formalna o średnim priorytecie do dalszego sprawdzenia.

Dlaczego to jest sensowny alert:

- zmiana jest konkretna,
- wiadomo, z którego źródła pochodzi,
- priorytet nie jest przesadzony,
- jest sugestia dalszej weryfikacji.

## Przykład 2 — pojedyncza zmiana właścicielska

> XYZ Sp. z o.o. - w CRBR pojawił się nowy beneficjent rzeczywisty. Zmiana właścicielska, która może być istotna i powinna trafić do historii zmian spółki.

Dlaczego to jest sensowny alert:

- pokazuje zmianę o wyższej wartości interpretacyjnej niż zwykły update formalny,
- nie sugeruje jeszcze zbyt mocnego wniosku,
- dobrze nadaje się do digestu i historii zmian.

## Przykład 3 — zmiana łączona

> Firma 123 Sp. z o.o. - jednocześnie wykryto zmianę zarządu w KRS i zmianę beneficjenta rzeczywistego w CRBR. To nie musi oznaczać problemu, ale jest to zestaw zmian o podwyższonym priorytecie do szybkiej weryfikacji.

Dlaczego to jest sensowny alert:

- łączy dwa źródła,
- podnosi priorytet nie przez dramatyczny język, tylko przez korelację zdarzeń,
- dobrze pokazuje logikę `distress-first`, która może być rozwijana później.

## Przykład 4 — zmiana o niskim priorytecie

> Nova Sp. z o.o. - w KRS zaktualizowano adres siedziby spółki. Zmiana formalna o niskim priorytecie, do zapisania w historii bez potrzeby pilnej reakcji.

Dlaczego to jest sensowny alert:

- nie każda zmiana jest ważna,
- system pokazuje też niski priorytet, zamiast robić szum z każdego eventu,
- historia zmian pozostaje pełna, ale priorytet jest rozsądny.

## Przykład 5 — alert z rekomendowanym następnym krokiem

> Delta Sp. z o.o. - w CRBR wykryto zmianę beneficjenta rzeczywistego, a w ostatnim snapshotcie KRS nie widać jeszcze zmian formalnych. Zmiana właścicielska o średnim priorytecie; warto sprawdzić, czy pojawi się odpowiadająca jej aktualizacja w KRS przy kolejnym runie.

Dlaczego to jest sensowny alert:

- nie tylko opisuje zmianę, ale sugeruje sensowny następny krok,
- pokazuje, że źródła mogą aktualizować się w różnym tempie,
- uczy, jak alert może wspierać workflow bez przesadnej pewności.

## Przykład 6 — alert do digestu zbiorczego

> Omega Sp. z o.o. - w tym tygodniu wykryto dwie zmiany: nowy prokurent w KRS oraz aktualizację beneficjenta rzeczywistego w CRBR. Spółka trafia do digestu tygodniowego jako pozycja o podwyższonym priorytecie.

Dlaczego to jest sensowny alert:

- pokazuje przypadek, w którym system grupuje kilka zmian w jedną pozycję,
- jest czytelny dla formatu `digest-first`,
- nadaje się jako przykład dla późniejszego modelu alertu zbiorczego.

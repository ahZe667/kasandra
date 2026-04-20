# Overview

## Teza

Kasandra nie ma byc kolejna baza danych o firmach. Ma byc malym systemem, ktory zamienia publiczne dane o spolkach w uzyteczne sygnaly i przy okazji buduje wlasne IP.

Na tym etapie projekt ma najwiekszy sens jako `alpha wewnetrzna`: narzedzie, ktore pozwala sprawdzic, czy da sie regularnie zbierac zmiany ze zrodel publicznych, porzadkowac je i wyciagac z nich sensowny alert.

Teza robocza:

> Jesli polaczymy kilka publicznych rejestrow i zamienimy zmiany w spolkach na krotki, trafny alert z priorytetem, to zbudujemy uzyteczny system monitoringu i wartosciowy asset, ktory pozniej moze stac sie produktem.

Przewaga systemu ma wynikac z czterech rzeczy: prostoty, waskiego zakresu startowego, jakosci diffu i alertu oraz budowy wlasnej logiki interpretacji — zamiast zaleznosci od gotowych raportow. To ostatnie jest kluczowe: wlasne IP to nie dane, ale sposob ich przetwarzania — reguly priorytetowania, slownik interpretacji zmian i logika alertowa, ktore rosna razem z projektem.

## Problem

Informacje o spolkach sa publiczne, ale w praktyce:

- sa rozproszone miedzy wieloma zrodlami,
- trudno je monitorowac regularnie,
- surowe dane nie odpowiadaja szybko na pytanie, czy zmiana jest istotna,
- reczne sprawdzanie kilku rejestrow zabiera czas i latwo prowadzi do przeoczen.

Projekt rozwiazuje nie tyle problem dostepu do danych, co problem ich interpretacji i uporzadkowania.

Grupy, ktore ten problem odczuwaja najdotkliwiej, to przede wszystkim kancelarie restrukturyzacyjne i prawnicy biznesowi — sledza zmiany formalne i wlascicielskie w wielu spolkach jednoczesnie i kazde opoznienie w informacji ma konsekwencje. Podobna potrzeba pojawia sie u analitykow gospodarczych oraz zespolow due diligence i compliance, gdzie regularny monitoring jest warunkiem pracy, a nie opcja.

## Job To Be Done

Pierwsza wersja systemu ma dawac prosta odpowiedz:

- co sie zmienilo,
- skad pochodzi zmiana,
- czy zmiana wyglada istotnie,
- co warto sprawdzic dalej.

W `v0` wazniejsze od szerokosci funkcji sa jakosc diffu, historia zmian i czytelny alert.

## Pozycjonowanie

Projekt nie powinien byc opisywany jako:

- pelna baza informacji gospodarczej,
- zamiennik duzych wywiadowni,
- szeroka platforma danych o firmach.

Lepsze pozycjonowanie:

- lekkie narzedzie wczesnego ostrzegania,
- monitoring zmian w spolkach,
- system lead qualification oparty o publiczne dane.

## Funkcjonalnosc

Zeby pokazac co system robi w praktyce, najlatwiej przesledzic przyklad.

**Scenariusz:** uzytkownik monitoruje 15 spolek. Uruchamia pipeline (lub dostaje go automatycznie). System porownuje aktualny stan KRS i CRBR z poprzednim snapshotem.

Jesli nic sie nie zmienilo — brak alertu.

Jesli wykryje zmiane, generuje krotki alert:

```
[PODWYZSZONY] ABC Sp. z o.o. | KRS + CRBR | 2025-04-14

KRS: zmiana w skladzie zarzadu — usunieto Jana Kowalskiego, dodano Anne Nowak
CRBR: zmiana beneficjenta rzeczywistego — nowy udzial 30%: Anna Nowak

Interpretacja: korelacja zmian w zarzadzie i beneficjencie w tej samej spolce
w krotkim czasie sugeruje istotna zmiane struktury wlascicielskiej.
Warte sprawdzenia.
```

Po zakonczeniu runu uzytkownik dostaje **digest** — zbiorczy przeglad wszystkich zmian z danego dnia, posortowany wedlug priorytetu. Kazda spolka ze zmiana ma swoj wpis z krotkim podsumowaniem i ocena pilnosci.

Dla kazdej spolki system prowadzi **historie zmian** — kolejne snapshoty z datami, dzieki czemu widac nie tylko co sie wlasnie zmienilo, ale tez jak wygladal stan poprzedni i kiedy doszlo do poprzedniej zmiany.

Trzy glowne wyjscia systemu:

- **alert** — pojedyncze zdarzenie z interpretacja i priorytetem,
- **digest** — dzienny przeglad wszystkich alertow dla watchlisty,
- **historia** — pelny log zmian per spolka.

Naturalnym pierwszym workflow jest praca osoby, ktora chce szybko wiedziec:

- co jest nowe,
- co jest wazne,
- co warto sprawdzic dzis, a nie za tydzien.

## Roadmap

- `Faza 0` — definicja rdzenia, modeli danych i recznych case studies,
- `Faza 1` — `v0 / alpha wewnetrzna` na `KRS + CRBR`,
- `Faza 2` — rozszerzenie `distress-first`, przede wszystkim o `KRZ`,
- `Faza 3` — maly pilot produktowy dla waskiej grupy uzytkownikow zewnetrznych.

`Alpha wewnetrzna` (Faza 1) to przede wszystkim narzedzie do pracy wlasnej: obserwowania wybranych spolek, wychwytywania zmian formalnych i wlascicielskich, szybkiego rozumienia co sie zmienilo i czy warto to dalej sprawdzic. Na tym etapie budujemy know-how, pipeline i logike alertowa — zewnetrzni odbiorcy sa wazni, ale jako cel pozniejszy.

`Distress-first` (Faza 2) to konkretna strategia rozszerzenia: zamiast dodawac kolejne zrodla ogolnie, priorytetyzujemy sygnaly zwiazane z zagrozeniem finansowym. `KRZ` (Krajowy Rejestr Zadluzonych) daje dostep do postepowania upadlosciowych, restrukturyzacyjnych i egzekucyjnych — czyli zdarzen, ktore dla kancelarii restrukturyzacyjnych i compliance maja najwieksza wartosc operacyjna.

## Zakres v0

Pierwszy rdzen jest swiadomie waski:

- zrodla: `KRS + CRBR`,
- formaty wyjscia: alert tekstowy, digest, historia zmian,
- interfejs: prosty CLI i lokalny run,
- magazyn danych: `sqlite3`.

Nie budujemy jeszcze publicznego API, ciezkiej orkiestracji ani pelnego panelu.

## Jak czytac docs

Ten dokument odpowiada za kierunek produktu.

- [02-sources-and-alerts](02-sources-and-alerts.md) opisuje zrodla, sygnaly i kontrakt alertu.
- [03-roadmap-and-gates](03-roadmap-and-gates.md) jest glownym zrodlem prawdy dla faz, gate'ow, ryzyk i otwartych pytan.
- [04-tech-stack](04-tech-stack.md) opisuje decyzje techniczne i granice architektury.
- `docs/examples/` trzyma referencyjne alerty i case studies.

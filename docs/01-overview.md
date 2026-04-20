# Overview

## Teza

Kasandra nie ma byc kolejna baza danych o firmach. Ma byc malym systemem, ktory zamienia publiczne dane o spolkach w uzyteczne sygnaly i przy okazji buduje wlasne IP.

Na obecnym etapie najlepszym punktem odniesienia jest `alpha wewnetrzna`, nie pelny produkt. Najpierw trzeba dowiezc powtarzalny przeplyw `snapshot -> diff -> alert`, a dopiero potem myslec o szerszej produktizacji.

## Problem

Informacje o spolkach sa publiczne, ale w praktyce:

- sa rozproszone miedzy wieloma zrodlami,
- trudno je monitorowac regularnie,
- surowe dane nie odpowiadaja szybko na pytanie, czy zmiana jest istotna,
- reczne sprawdzanie kilku rejestrow zabiera czas i latwo prowadzi do przeoczen.

Projekt rozwiazuje nie tyle problem dostepu do danych, co problem ich interpretacji i uporzadkowania.

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

Naturalnym pierwszym workflow jest praca osoby, ktora chce szybko wiedziec:

- co jest nowe,
- co jest wazne,
- co warto sprawdzic dzis, a nie za tydzien.

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

# Overview

## Teza

Najmocniejsza teza dla tego projektu jest prosta: nie budować kolejnej bazy danych o firmach, tylko mały system, który zamienia publiczne dane o spółkach w użyteczne sygnały i przy okazji buduje własne IP.

Na tym etapie projekt ma największy sens jako `alpha wewnętrzna`: narzędzie, które pozwala nam sprawdzić, czy da się regularnie zbierać zmiany ze źródeł publicznych, porządkować je i wyciągać z nich sensowny alert.

Teza robocza:

> Jeśli połączymy kilka publicznych rejestrów i zamienimy zmiany w spółkach na krótki, trafny alert z priorytetem, to zbudujemy użyteczny system monitoringu i wartościowy asset, który później może stać się produktem.

Przewaga systemu ma wynikać z czterech rzeczy: prostoty, wąskiego zakresu startowego, jakości diffu i alertu oraz budowy własnej logiki interpretacji — zamiast zależności od gotowych raportów. To ostatnie jest kluczowe: własne IP to nie dane, ale sposób ich przetwarzania — reguły priorytetowania, słownik interpretacji zmian i logika alertowa, które rosną razem z projektem.

## Problem

Informacje o spółkach są publiczne, ale w praktyce:

- są rozproszone między wieloma źródłami,
- trudno je monitorować regularnie,
- surowe dane nie dają szybkiej odpowiedzi, czy coś się realnie zmieniło,
- ręczne sprawdzanie kilku serwisów zabiera czas i powoduje, że łatwo coś przegapić.

Problem jest więc podwójny: z jednej strony chodzi o wygodę pracy, z drugiej o zbudowanie własnego sposobu zamiany publicznych danych w uporządkowany sygnał.

Grupy, które ten problem odczuwają najdotkliwiej, to przede wszystkim kancelarie restrukturyzacyjne i prawnicy biznesowi — śledzą zmiany formalne i właścicielskie w wielu spółkach jednocześnie i każde opóźnienie w informacji ma konsekwencje. Podobna potrzeba pojawia się u analityków gospodarczych oraz zespołów due diligence i compliance, gdzie regularny monitoring jest warunkiem pracy, a nie opcją.

## Rozwiązanie

Pierwsza wersja to lekki system alertów oparty głównie na `KRS` i `CRBR`, który daje prostą odpowiedź na cztery pytania: co się zmieniło, skąd pochodzi zmiana, co to może znaczyć i czy warto to dalej sprawdzić.

System:

- zbiera snapshot danych dla wybranych spółek,
- normalizuje podstawowe identyfikatory,
- wykrywa różnice względem poprzedniego stanu,
- zapisuje historię zmian,
- generuje prosty alert lub digest z krótką interpretacją.

`v0` ma przede wszystkim dowieźć działający rdzeń. Nie musi jeszcze być pełnym produktem dla szerokiego rynku — wystarczy, że pipeline i alerty będą wystarczająco sensowne, żeby używanie ich miało praktyczny sens i żeby rosła wartość projektu jako assetu. Docelowo zakres może się rozszerzać o kolejne źródła i bardziej złożone sygnały.

## Funkcjonalność

Żeby pokazać co system robi w praktyce, najłatwiej prześledzić przykład.

**Scenariusz:** użytkownik monitoruje 15 spółek. Uruchamia pipeline (lub dostaje go automatycznie). System porównuje aktualny stan KRS i CRBR z poprzednim snapshotem.

Jeśli nic się nie zmieniło — brak alertu.

Jeśli wykryje zmianę, generuje krótki alert:

```
[PODWYŻSZONY] ABC Sp. z o.o. | KRS + CRBR | 2025-04-14

KRS: zmiana w składzie zarządu — usunięto Jana Kowalskiego, dodano Annę Nowak
CRBR: zmiana beneficjenta rzeczywistego — nowy udział 30%: Anna Nowak

Interpretacja: korelacja zmian w zarządzie i beneficjencie w tej samej spółce
w krótkim czasie sugeruje istotną zmianę struktury właścicielskiej.
Warte sprawdzenia.
```

Po zakończeniu runu użytkownik dostaje **digest** — zbiorczy przegląd wszystkich zmian z danego dnia, posortowany według priorytetu. Każda spółka ze zmianą ma swój wpis z krótkim podsumowaniem i oceną pilności.

Dla każdej spółki system prowadzi **historię zmian** — kolejne snapshoty z datami, dzięki czemu widać nie tylko co się właśnie zmieniło, ale też jak wyglądał stan poprzedni i kiedy doszło do poprzedniej zmiany.

Trzy główne wyjścia systemu:

- **alert** — pojedyncze zdarzenie z interpretacją i priorytetem,
- **digest** — dzienny przegląd wszystkich alertów dla watchlisty,
- **historia** — pełny log zmian per spółka.

Szczegółowa specyfikacja sygnałów i formatu alertów znajduje się w [03-signals-and-alerts](03-signals-and-alerts.md).

## Logika rozwoju

Projekt jest rozpisany na cztery fazy:

- `Faza 0` — definicja rdzenia, modeli danych i ręcznych case studies,
- `Faza 1` — `v0 / alpha wewnętrzna` na `KRS + CRBR`,
- `Faza 2` — rozszerzenie `distress-first`, przede wszystkim o `KRZ`,
- `Faza 3` — mały pilot produktowy dla wąskiej grupy użytkowników zewnętrznych.

Fazy są bramkami jakościowymi, a nie sztywnym harmonogramem. Dokładniejszy opis znajduje się w [05-mvp](05-mvp.md).

`Alpha wewnętrzna` (Faza 1) to przede wszystkim narzędzie do pracy własnej: obserwowania wybranych spółek, wychwytywania zmian formalnych i właścicielskich, szybkiego rozumienia co się zmieniło i czy warto to dalej sprawdzić. Na tym etapie budujemy know-how, pipeline i logikę alertową — zewnętrzni odbiorcy są ważni, ale jako cel późniejszy.

`Distress-first` (Faza 2) to konkretna strategia rozszerzenia: zamiast dodawać kolejne źródła ogólnie, priorytetyzujemy sygnały związane z zagrożeniem finansowym. `KRZ` (Krajowy Rejestr Zadłużonych) daje dostęp do postępowań upadłościowych, restrukturyzacyjnych i egzekucyjnych — czyli zdarzeń, które dla kancelarii restrukturyzacyjnych i compliance mają największą wartość operacyjną. Budujemy logikę alertową wokół sygnałów wysokiego priorytetu, zanim rozszerzymy zakres na bardziej ogólny monitoring.
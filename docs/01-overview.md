# Overview

## Teza

Najmocniejsza teza dla tego projektu jest prosta: nie budować kolejnej bazy danych o firmach, tylko mały system, który zamienia publiczne dane o spółkach w użyteczne sygnały i przy okazji buduje własne IP.

Na tym etapie projekt ma największy sens jako `alpha wewnętrzna`: narzędzie, które pozwala nam sprawdzić, czy da się regularnie zbierać zmiany ze źródeł publicznych, porządkować je i wyciągać z nich sensowny alert.

Teza robocza:

> Jeśli połączymy kilka publicznych rejestrów i zamienimy zmiany w spółkach na krótki, trafny alert z priorytetem, to zbudujemy użyteczny system monitoringu i wartościowy asset, który później może stać się produktem.

## Punkt odniesienia v0

Pierwsza wersja nie musi od razu powstawać z myślą o sprzedaży. Punktem odniesienia jest wewnętrzny workflow:

- obserwowanie wybranych spółek,
- wychwytywanie zmian formalnych i właścicielskich,
- szybkie rozumienie, co się zmieniło i czy warto to dalej sprawdzić,
- budowa własnego know-how, pipeline'u i logiki alertowej.

Potencjalni odbiorcy zewnętrzni pozostają ważni, ale na późniejszym etapie. Najbardziej naturalne kierunki to:

- kancelarie restrukturyzacyjne,
- prawnicy biznesowi,
- analitycy gospodarczy,
- zespoły due diligence i compliance.

## Problem

Informacje o spółkach są publiczne, ale w praktyce:

- są rozproszone między wieloma źródłami,
- trudno je monitorować regularnie,
- surowe dane nie dają szybkiej odpowiedzi, czy coś się realnie zmieniło,
- ręczne sprawdzanie kilku serwisów zabiera czas i powoduje, że łatwo coś przegapić.

Problem jest więc podwójny: z jednej strony chodzi o wygodę pracy, z drugiej o zbudowanie własnego sposobu zamiany publicznych danych w uporządkowany sygnał.

## Job to Be Done

W pierwszej wersji system ma dawać prostą odpowiedź:

- co się zmieniło,
- skąd pochodzi zmiana,
- co to może znaczyć,
- czy warto to dalej sprawdzić.

To nie musi jeszcze być pełny produkt dla szerokiego rynku. Wystarczy, że pipeline i alerty będą wystarczająco sensowne, żeby używanie ich miało praktyczny sens i żeby rosła wartość projektu jako assetu.

## Rozwiązanie

Pierwsza wersja to lekki system alertów oparty głównie na `KRS` i `CRBR`.

System:

- zbiera snapshot danych dla wybranych spółek,
- normalizuje podstawowe identyfikatory,
- wykrywa różnice względem poprzedniego stanu,
- zapisuje historię zmian,
- generuje prosty alert lub digest z krótką interpretacją.

Docelowo zakres może się rozszerzać o kolejne źródła i bardziej złożone sygnały, ale `v0` ma przede wszystkim dowieźć działający rdzeń.

## Logika rozwoju

Projekt jest rozpisany na cztery fazy:

- `Faza 0` - definicja rdzenia, modeli danych i ręcznych case studies,
- `Faza 1` - `v0 / alpha wewnętrzna` na `KRS + CRBR`,
- `Faza 2` - rozszerzenie `distress-first`, przede wszystkim o `KRZ`,
- `Faza 3` - mały pilot produktowy dla wąskiej grupy użytkowników zewnętrznych.

Fazy są bramkami jakościowymi, a nie sztywnym harmonogramem. Dokładniejszy opis znajduje się w [05-mvp](05-mvp.md).

## Propozycja wartości

To nie ma być kolejna baza firm. To ma być filtr i silnik zmian, który:

- porządkuje rozproszone dane,
- pokazuje tylko to, co rzeczywiście się zmieniło,
- buduje własną logikę interpretacji,
- daje fundament pod dalszy rozwój produktu albo komercjalizację.

Przewaga rozwiązania ma wynikać z:

- prostoty,
- wąskiego zakresu startowego,
- jakości diffu i alertu,
- budowy własnego IP zamiast zależności od gotowych raportów.

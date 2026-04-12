# Signals and Alerts

## Jakie sygnały mają znaczenie w v0

Pierwsza wersja powinna skupiać się tylko na takich sygnałach, które da się wiarygodnie wykryć z `KRS` i `CRBR` oraz szybko zinterpretować.

Typy sygnałów dla `v0`:

- zmiana zarządu,
- zmiana prokury,
- zmiana adresu lub danych rejestrowych,
- zmiana beneficjenta rzeczywistego,
- zestaw kilku zmian naraz w krótkim czasie.

W tej wersji ważniejsza od szerokości katalogu alertów jest jakość odpowiedzi na pytanie: `co się zmieniło i czy to wygląda istotnie?`

## Cechy dobrego alertu

Dobry alert nie może być tylko surowym eventem. Minimum:

- identyfikacja spółki,
- źródło zmiany,
- porównanie poprzedniego i nowego stanu,
- data wykrycia,
- krótka interpretacja,
- priorytet lub prosty scoring,
- wskazanie, czy warto sprawdzić temat dalej.

## Przykład alertu

> ABC Sp. z o.o. - w KRS wykryto zmianę zarządu, a w CRBR pojawił się nowy beneficjent rzeczywisty. To nie przesądza o problemie, ale jest to zestaw zmian wart dalszej weryfikacji.

## Kierunek dla scoringu

Na start scoring powinien być prosty i zrozumiały:

- niski priorytet dla pojedynczych, mało istotnych zmian formalnych,
- średni priorytet dla zmian właścicielskich,
- podwyższony priorytet dla kilku zmian z `KRS` i `CRBR` naraz.

Nie chodzi jeszcze o doskonały model oceny, tylko o zbudowanie pierwszej sensownej logiki interpretacji.

## Format dostarczenia

Pierwsza wersja powinna używać prostych formatów:

- pojedynczy alert tekstowy,
- digest z listą zmian,
- historia zmian dla konkretnej spółki.

Panel webowy nie jest potrzebny w `v0`, jeśli digest i historia zmian dają wystarczającą użyteczność.

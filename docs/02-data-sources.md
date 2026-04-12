# Data Sources

## Cel

Zbudować pierwszy zestaw źródeł, który jest wystarczająco mały, żeby szybko postawić działającą `alpha v0`, a jednocześnie daje sensowną wartość poznawczą i alertową.

## Priorytety źródeł

| Źródło | Co monitorujemy | Priorytet | Trudność | Uwagi |
| --- | --- | --- | --- | --- |
| KRS | zarząd, prokurenci, adres, statut, kapitał | v0 must | łatwa | podstawowe źródło zmian formalnych i dobry fundament pod diff |
| CRBR | beneficjenci rzeczywiści i zmiany właścicielskie | v0 must | łatwa | mocny sygnał właścicielski, dobrze uzupełnia KRS |
| KRZ | postępowania upadłościowe i restrukturyzacyjne | v1 | średnia | ważne źródło, ale niepotrzebne do zbudowania pierwszego rdzenia |
| ESPI / PAP | raporty bieżące i okresowe spółek publicznych | v1 | łatwa | przydatne później, ale zawęża zakres do rynku publicznego |
| Biała Lista VAT | status VAT i rachunki bankowe | v1 | łatwa | wartościowe rozszerzenie po ustabilizowaniu rdzenia |
| Monitor Sądowy | ogłoszenia sądowe i upadłościowe | v2 | średnia | warto rozważyć po KRZ |
| Przetargi UZP | przetargi i wyniki | v2 | łatwa | osobny kierunek, niepotrzebny na start |
| GUS / BDL | dane finansowe, zatrudnienie, PKD | v2 / kontekst | średnia | dobre jako tło, słabe jako trigger alertów |
| BIG / KRD | wpisy o zaległościach | v2 / płatne | trudna | raczej późniejszy, komercyjny etap |

## Rekomendacja dla v0

Na start:

1. `KRS`
2. `CRBR`

Ten zestaw daje:

- zmiany formalne,
- zmiany właścicielskie,
- prosty i czytelny model danych,
- mały zakres techniczny, dobry do budowy pierwszego assetu.

## Co dodać po v0

- `KRZ`, gdy będziemy chcieli wejść mocniej w sygnały kryzysowe,
- `ESPI / PAP`, jeśli pojawi się potrzeba monitoringu spółek publicznych,
- `Biała Lista VAT`, jeśli będziemy chcieli wzbogacić alerty o sygnały operacyjne.

## Czego nie wrzucać do pierwszej wersji

- wielu źródeł naraz tylko po to, żeby zwiększyć szerokość projektu,
- źródeł, które komplikują model danych bez budowy rdzenia,
- `GUS / BDL` jako trigger alertów,
- `BIG / KRD` jako element pierwszej darmowej lub lekkiej wersji.

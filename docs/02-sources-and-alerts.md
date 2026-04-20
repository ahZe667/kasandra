# Sources And Alerts

## Cel

Ten dokument laczy dwie rzeczy, ktore w `v0` musza pozostac spojne:

- z jakich zrodel korzystamy,
- jakie sygnaly i alerty z tych zrodel chcemy wyprowadzac.

## Priorytety zrodel

| Zrodlo | Co monitorujemy | Etap | Uwagi |
| --- | --- | --- | --- |
| KRS | zarzad, prokura, adres, dane rejestrowe | `v0 must` | podstawowe zrodlo zmian formalnych |
| CRBR | beneficjenci rzeczywisci i zmiany wlascicielskie | `v0 must` | podstawowe zrodlo zmian wlascicielskich |
| KRZ | postepowania restrukturyzacyjne i upadlosciowe | `v1` | glowny kandydat do rozszerzenia distress-first |
| ESPI / PAP | raporty biezace i okresowe spolek publicznych | `later` | przydatne, ale zawaza projekt na rynek publiczny |
| Biala Lista VAT | status VAT i rachunki bankowe | `later` | raczej sygnal uzupelniajacy niz rdzen |
| GUS / BDL | dane finansowe i statystyczne | `later / context` | dobre jako tlo, slabe jako trigger |

W pierwszej wersji obowiazkowy zakres to tylko `KRS + CRBR`.

## Sygnaly v0

W `v0` interesuja nas tylko sygnaly, ktore da sie wiarygodnie wykryc i szybko zinterpretowac:

| Typ sygnalu | Zrodlo | Domyslny priorytet | Komentarz |
| --- | --- | --- | --- |
| zmiana zarzadu | `KRS` | `sredni` | mocny sygnal organizacyjny |
| zmiana prokury | `KRS` | `niski` albo `sredni` | zalezy od kontekstu |
| zmiana adresu lub danych rejestrowych | `KRS` | `niski` | wazna historycznie, zwykle niepilna |
| zmiana beneficjenta rzeczywistego | `CRBR` | `sredni` | mocniejszy sygnal interpretacyjny |
| kilka zmian w krotkim czasie | `KRS + CRBR` | `podwyzszony` | priorytet wynika z korelacji zdarzen |

Wazniejsze od szerokosci katalogu sygnalow jest dobre rozroznienie miedzy szumem a zmiana, ktora realnie zasluguje na uwage.

## Kontrakt alertu

Dobry alert w `v0` powinien zawierac minimum:

| Pole | Znaczenie |
| --- | --- |
| `company_id` | jednoznaczne wskazanie spolki |
| `title` | krotki opis zmiany |
| `summary` | zrozumiale streszczenie diffu |
| `evidence` | zrodlo i porownanie starego z nowym stanem |
| `priority` | `niski`, `sredni`, `podwyzszony` |
| `recommended_next_step` | co warto sprawdzic dalej |
| `generated_at` | kiedy alert powstal |

Alert ma byc interpretacyjny, ale nie kategoryczny. System wskazuje sygnaly do sprawdzenia, nie wydaje formalnej opinii.

## Format dostarczenia

Pierwsza wersja powinna uzywac prostych formatow:

- pojedynczy alert tekstowy,
- digest z lista zmian,
- historia zmian dla konkretnej spolki.

Panel webowy nie jest potrzebny przed udowodnieniem, ze alert i historia zmian sa praktycznie uzyteczne.

## Referencyjne przyklady

- [05-sample-alerts](05-sample-alerts.md)

## Czego nie dokladamy na start

- wielu nowych zrodel tylko po to, zeby zwiekszyc szerokosc projektu,
- scoringu opartego na ciezkiej logice lub ML,
- zrodel, ktore komplikuja model danych bez wzmacniania rdzenia `KRS + CRBR`.

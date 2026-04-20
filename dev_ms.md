# dev_ms — notes robocze Mateusz

Plik prywatny, nie idzie na main. Służy do zbierania obserwacji, decyzji i surowych wyników
zanim coś będzie gotowe do review lub merge'a.

---

## Co tu trzymać

- **Obserwacje z ręcznych testów** — co zobaczyłem w KRS/CRBR, jak wygląda surowy response, co jest dziwne
- **Decyzje i uzasadnienia** — dlaczego wybrałem dane pole, dlaczego odrzuciłem inne podejście
- **Otwarte pytania** — rzeczy, które trzeba ustalić zanim zacommituję logikę
- **Scratchpad modeli danych** — drafty schematów przed zamrożeniem kontraktu
- **Wyniki case studies** — 5-10 spółek testowych: co zmieniło się, jak to wyglądało
- **Braki i gotchas źródeł** — niespójności API, brakujące pola, edge case'y identyfikatorów
- **TODO do następnego posiedzenia** — żeby nie tracić wątku między sesjami

---

## Faza 0 — aktywny sprint

### Watchlista startowa (do wypełnienia)

| Spółka | KRS | NIP | REGON | Forma | Uwagi |
|--------|-----|-----|-------|-------|-------|
| ŻABKA POLSKA SP. Z O.O. | 0000636642 | 5223071241 | 365388398 | Sp. z o.o. | duży retail, dużo zmian operacyjnych |
| DRUTEX SPÓŁKA AKCYJNA | 0000140428 | 8421622720 | 771564493 | SA | producent okien/drzwi, stabilna |
| GRUPA MASPEX SP. Z O.O. | 0000898248 | 5512617657 | 122948517 | Sp. z o.o. | FMCG, Tymbark — holding |
| DINO POLSKA SPÓŁKA AKCYJNA | 0000408273 | 6211766191 | 300820828 | SA | retail, notowana GPW |
| ASSECO POLAND SPÓŁKA AKCYJNA | 0000033391 | 5220003307 | 010337520 | SA | IT, notowana GPW |
| FAME MMA SPÓŁKA AKCYJNA | 0000883491 | 7773370464 | 388181156 | SA | młoda SA, dynamiczne zmiany |
| MENTZEN SPÓŁKA AKCYJNA | 0001008036 | 5273032556 | 523923895 | SA | nowa SA, Mentzen — ciekawy CRBR |
| "STRONG MAN" SP. Z O.O. | 0000055656 | 5862021333 | 191892935 | Sp. z o.o. | stara spółka, logistyka Malbork |
| "TENCZYNEK DYSTRYBUCJA" SA | 0000864032 | 9462683417 | 381368271 | SA | Palikot, strata, ciekawy profil ryzyka |
| JANUSZEX SP. Z O.O. | 0000779880 | 5272889007 | 382903625 | Sp. z o.o. | mała spółka, 100% właściciel = prezes |

### Ręczne case studies — postęp

Snapshot KRS pobrany dla wszystkich 10 spółek 2026-04-20. Plik podsumowujący:
[dev_ms_data/snapshot_summary_2026-04-20.md](dev_ms_data/snapshot_summary_2026-04-20.md).
Surowe JSON: [dev_ms_data/snapshots/2026-04-20/krs/](dev_ms_data/snapshots/2026-04-20/krs/).

| Spółka | KRS | CRBR | Diff | Alert |
|--------|-----|------|------|-------|
| Żabka Polska              | OK  | brak | [ ] | [ ] |
| Drutex                    | OK  | brak | [ ] | [ ] |
| Grupa Maspex              | OK  | brak | [ ] | [ ] |
| Dino Polska               | OK  | brak | [ ] | [ ] |
| Asseco Poland             | OK  | brak | [ ] | [ ] |
| FAME MMA                  | OK  | brak | [ ] | [ ] |
| Mentzen                   | OK  | brak | [ ] | [ ] |
| Strong Man                | OK  | brak | [ ] | [ ] |
| Tenczynek Dystrybucja     | OK  | brak | [ ] | [ ] |
| Januszex                  | OK  | brak | [ ] | [ ] |

### Pytania otwarte (Faza 0)

- [ ] Które pola KRS wchodzą do rdzenia, które zostają jako kontekst?
- [ ] Które pola CRBR są kluczowe dla wykrywania zmiany beneficjenta?
- [ ] Format przechowywania `raw_payload` — JSON dump czy coś znormalizowanego?
- [ ] Jak identyfikować spółkę gdy nie ma NIP lub REGON w odpowiedzi?

---

## Kontrakty danych — robocze drafty

### model_spolki (draft)

```python
# internal_id, KRS, NIP, REGON, nazwa, status, notatki
```

### model_snapshotu (draft)

```python
# company_id, source, collected_at, raw_payload, normalized_payload, hash
```

### model_zmiany (draft)

```python
# company_id, source, field, previous_value, current_value, detected_at, change_type
```

### model_alertu (draft)

```python
# company_id, title, summary, evidence, priority, recommended_next_step, generated_at
```

---

## Wzór wyciąganych danych — KRS normalized_payload (v0.1)

Schemat `normalized_payload` dla snapshotu KRS. Wyciągamy tylko te pola, których zmiana generuje alert lub daje istotny kontekst. Reszta zostaje w `raw_payload`.

### Źródłowe ścieżki → pola znormalizowane

| Pole wyjściowe | Ścieżka w JSON | Uwagi |
|---|---|---|
| `company.krs` | `odpis.naglowekA.numerKRS` | stabilny identyfikator |
| `company.nazwa` | `odpis.dane.dzial1.danePodmiotu.nazwa` | |
| `company.forma` | `odpis.dane.dzial1.danePodmiotu.formaPrawna` | |
| `company.nip` | `odpis.dane.dzial1.danePodmiotu.identyfikatory.nip` | |
| `company.regon` | `odpis.dane.dzial1.danePodmiotu.identyfikatory.regon` | |
| `snapshot_meta.stan_z_dnia` | `odpis.naglowekA.stanZDnia` | meta — nie alertujemy |
| `snapshot_meta.nr_ostatniego_wpisu` | `odpis.naglowekA.numerOstatniegoWpisu` | proxy "coś się zmieniło" |
| `snapshot_meta.data_ostatniego_wpisu` | `odpis.naglowekA.dataOstatniegoWpisu` | |
| `adres` | `odpis.dane.dzial1.siedzibaIAdres.adres` | ulica, nrDomu, kodPocztowy, miejscowosc, kraj |
| `kapital.wartosc` | `odpis.dane.dzial1.kapital.wysokoscKapitaluZakladowego.wartosc` | string "5000,00" |
| `kapital.waluta` | `odpis.dane.dzial1.kapital.wysokoscKapitaluZakladowego.waluta` | |
| `zarzad.nazwa_organu` | `odpis.dane.dzial2.reprezentacja.nazwaOrganu` | |
| `zarzad.sposob_reprezentacji` | `odpis.dane.dzial2.reprezentacja.sposobReprezentacji` | |
| `zarzad.sklad[]` | `odpis.dane.dzial2.reprezentacja.sklad[]` | patrz `osoba_key` niżej |
| `wlasciciele.typ` | — | `wspolnicy_spzoo` \| `jedyny_akcjonariusz` \| `brak_w_krs` |
| `wlasciciele.lista[]` | `dzial1.wspolnicySpzoo[]` **lub** `dzial1.jedynyAkcjonariusz[]` | |
| `pkd_glowny.kod` | `dzial3.przedmiotDzialalnosci.przedmiotPrzewazajacejDzialalnosci[0].kodDzial+Klasa+Podklasa` | |
| `pkd_glowny.opis` | j.w. `.opis` | |
| `distress.dzial4` | `dzial4` niepuste? | bool |
| `distress.dzial5` | `dzial5` niepuste? | bool |
| `distress.dzial6` | `dzial6` niepuste? | bool |
| `distress.dzial6_typy[]` | klucze w `dzial6` (np. `polaczeniePodzialPrzeksztalcenie`) | lista stringów |

### Identyfikator osoby (osoba_key)

Bez deanonimizacji — stabilny klucz osoby budujemy jako:

- **osoba prawna:** `"LE:" + nazwa + (krs || regon)` — pełna nazwa i ID są jawne
- **osoba fizyczna:** `"NAT:" + maska_nazwisko + "|" + maska_imie + "|" + maska_pesel`

Maski są deterministyczne (długość = długość oryginału), więc ten sam człowiek daje ten sam klucz między snapshotami. Zmiana któregokolwiek członu = inna osoba.

### Reprezentacja członka zarządu / wspólnika

```python
{
  "osoba_key": "NAT:J************|K********|4**********",
  "typ": "fizyczna",   # lub "prawna"
  "display": "K******** J************",   # do alertu
  "funkcja": "PREZES ZARZĄDU",   # tylko zarząd
  "posiadane_udzialy": "100 UDZIAŁÓW O ŁĄCZNEJ WARTOŚCI 5.000,00 ZŁ",   # tylko wspólnicy
  "calosc": true   # tylko wspólnicy / jedyny_akcjonariusz
}
```

### Pola pomijane w v0.1

- `dzial1.umowaStatut` (zmiany umowy — za szczegółowe na start)
- `dzial1.emisjeAkcji` (potrzebne dla SA, ale skomplikowane — odłożyć)
- `dzial1.pozostaleInformacje` (czas trwania spółki, rok obrotowy — kontekst)
- pełna historia wpisów, daty każdej zmiany
- adresy korespondencyjne oddziałów

---

## Alerty — propozycje v0.1

Każdy alert = reguła na diffie dwóch `normalized_payload`. Priorytet orientacyjny: `N / Ś / W / K` (niski / średni / wysoki / krytyczny).

### Sygnały binarne (distress — najsilniejsze)

| ID | Trigger | Priorytet | Uzasadnienie |
|---|---|---|---|
| `A-DZ6-NEW` | `distress.dzial6` przeszedł `false → true` lub przybył nowy typ | **K** | pojawiła się upadłość / połączenie / przekształcenie / podział |
| `A-DZ4-NEW` | `distress.dzial4` przeszedł `false → true` | **K** | pojawili się wierzyciele / hipoteki |
| `A-DZ5-NEW` | `distress.dzial5` przeszedł `false → true` | **W** | pojawił się kurator |

### Zmiany struktury (klasyczne sygnały kontroli)

| ID | Trigger | Priorytet | Uwagi |
|---|---|---|---|
| `A-ZARZAD-PREZES` | zmiana osoby na funkcji `PREZES ZARZĄDU` | **W** | najsilniejsza rotacja w zarządzie |
| `A-ZARZAD-SKLAD` | zmiana liczby lub składu `zarzad.sklad[]` (bez prezesa) | Ś | dodanie/usunięcie członka |
| `A-ZARZAD-REPR` | zmiana `sposob_reprezentacji` | Ś | zmiana zasad podpisywania |
| `A-WLASC-NOWY` | nowy `osoba_key` w `wlasciciele.lista[]` | **W** | nowy wspólnik / akcjonariusz |
| `A-WLASC-USUN` | zniknął `osoba_key` z `wlasciciele.lista[]` | **W** | exit wspólnika |
| `A-WLASC-50PC` | udział wspólnika przekroczył 50% (lub spadł poniżej) | **W** | zmiana kontroli — heurystyka na `posiadane_udzialy` |
| `A-KAPITAL` | zmiana `kapital.wartosc` | Ś | podwyższenie / obniżenie kapitału |

### Zmiany kontekstowe (słabszy sygnał, ale warto odnotować)

| ID | Trigger | Priorytet |
|---|---|---|
| `A-NAZWA` | zmiana `company.nazwa` | Ś |
| `A-FORMA` | zmiana `company.forma` | **W** |
| `A-ADRES` | zmiana `adres.miejscowosc` lub pełnego adresu | N |
| `A-PKD` | zmiana `pkd_glowny.kod` | Ś |

### Reguły kompozycyjne (v0.2, wymagają historii kilku snapshotów)

| ID | Trigger | Priorytet |
|---|---|---|
| `A-KOMP-ZAR-WLASC` | `A-ZARZAD-*` i `A-WLASC-*` w tej samej spółce w oknie ≤30 dni | **K** |
| `A-SWIEZA-ROTACJA` | spółka < 12 mies. od rejestracji + jakakolwiek zmiana zarządu | **W** |

### Co z osobami fizycznymi?

Wszystkie powyższe reguły **działają na `osoba_key`** (maski), nie na pełnych danych. Alert powie *"zmiana PREZESA ZARZĄDU: K\*\*\*\*\*\*\*\* J\*\*\*\*\*\*\*\*\*\*\*\* → M\*\*\*\*\*\*\* N\*\*\*\*\*\*\*"* — wystarczy jako sygnał, pełna identyfikacja = ręczna weryfikacja w KRS online.

### Dataset testowy (baseline)

Znormalizowane snapshoty dla 10 spółek są w:

- [dev_ms_data/normalized/2026-04-20/krs/](dev_ms_data/normalized/2026-04-20/krs/) — per spółka
- [dev_ms_data/normalized/2026-04-20/dataset.json](dev_ms_data/normalized/2026-04-20/dataset.json) — zbiorczy plik

To baseline dla pierwszego diffu — kolejny run (za ~tydzień) pozwoli sprawdzić, czy reguły alertowe faktycznie wychwytują to, co powinny.

---

## Gotchas i znaleziska — źródła

### KRS API (api-krs.ms.gov.pl)

- **Endpoint:** `GET https://api-krs.ms.gov.pl/api/krs/OdpisAktualny/{KRS}?rejestr=P&format=json`
- **Bez autoryzacji**, działa od ręki, zwraca pełny odpis aktualny w JSON
- **Rozmiary:** od ~3.6 KB (Januszex, mała spółka, 3 wpisy) do ~62 KB (Asseco, 169 wpisów)
- **Struktura:** `odpis.dane.dzial1..dzial6` — standardowe działy KRS
  - dz1: dane podmiotu, adres, kapitał, wspólnicy (dla sp. z o.o.)
  - dz2: skład zarządu, sposób reprezentacji
  - dz3: PKD, rok obrotowy
  - dz4: wierzyciele, hipoteki (puste dla naszych 10)
  - dz5: kuratorzy (puste dla naszych 10)
  - dz6: połączenia, podziały, przekształcenia, upadłość — Żabka, Maspex, Dino, Asseco mają wpisy

#### KRYTYCZNE: maskowanie danych osobowych

Publiczne API maskuje imiona, nazwiska i PESEL osób fizycznych:
- `nazwiskoICzlon: "J************"`
- `imie: "K********"`
- `pesel: "4**********"`

**Implikacje dla projektu:**
- Możemy wykryć **zmianę** w zarządzie (liczba osób, długość masek, dodanie/usunięcie pozycji)
- **Nie możemy zidentyfikować** kto konkretnie wszedł/wyszedł
- Osoby prawne (np. `MASPEX HOLDING SA`, `ZABKA GROUP S.A.`) — pełne dane + KRS
- Pole `posiadaneUdzialy` (np. "100 UDZIAŁÓW O ŁĄCZNEJ WARTOŚCI 5.000,00 ZŁ") — **nie jest maskowane**

To zmienia myślenie o sygnale: dla zmian zarządu/wspólników osób fizycznych wartość = "coś się zmieniło, sprawdź źródło"; pełna nazwa wymaga ręcznej weryfikacji w KRS online.

### CRBR (crbr.podatki.gov.pl)

- Próbowane endpointy 404: `/api/wyszukaj/{NIP}`, `/api/wyszukaj/zgloszenie-aktualne/{NIP}`, POST z body
- **Brak otwartego REST API** — system wymaga kwalifikowanego dostępu lub interakcji przez interfejs
- Do podjęcia decyzji w Fazie 0:
  - czy ręcznie zaciągać przez frontend (web-scraping/Selenium),
  - czy zgłosić się o oficjalny dostęp,
  - czy odłożyć CRBR do Fazy 1 i Fazę 0 robić tylko na KRS

---

## Log sesji

### 2026-04-20

- Projekt wszedł w Fazę 0
- Branch Mat założony jako osobna przestrzeń robocza
- Watchlista 10 spółek skompletowana
- Snapshot KRS pobrany dla wszystkich 10 (`dev_ms_data/snapshots/2026-04-20/krs/`)
- Wygenerowane podsumowanie: `dev_ms_data/snapshot_summary_2026-04-20.md`
- **Znalezisko:** KRS publiczne API maskuje dane osób fizycznych
- **Blokada:** CRBR nie ma otwartego API — wymaga decyzji jak dalej

---

## Scratchpad / surowe notatki

<!-- Tu wrzucaj bez formatowania: fragmenty JSON, linki, cytaty z docs, pomysły -->

### KRS — pełne dane wspólników (przykłady osób prawnych)

```
Żabka:  ZABKA GROUP SOCIÉTÉ ANONYME — 100% (Luxembourg, brak KRS PL)
Maspex: MASPEX HOLDING SA [KRS 0000725647] — większość udziałów
```

### KRS — przykład osoby fizycznej (Januszex, zarząd)

```json
{
  "nazwisko": {"nazwiskoICzlon": "J************"},
  "imiona": {"imie": "K********"},
  "identyfikator": {"pesel": "4**********"},
  "funkcjaWOrganie": "PREZES ZARZĄDU"
}
```

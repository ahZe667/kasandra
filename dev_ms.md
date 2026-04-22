# dev_ms — notatki robocze Mateusz

Plik prywatny, nie idzie na main. Obserwacje, decyzje techniczne i wyniki Fazy 0 / Fazy 1.

---

## Status projektu

**Faza 0 — ZAMKNIĘTA** (2026-04-22)
Wszystkie snapshoty Fazy 0 zebrane, ekstraktor KRS gotowy, CRBR Playwright działa.

**Faza 1 — W TOKU** (od 2026-04-23)

| Blok | Opis | Status |
|------|------|--------|
| B1 | Fundament storage — SQLite, importer, hashe snapshotów | DONE |
| B2 | Diff engine KRS — porównanie snapshotów, reguły alertów | TODO |
| B3 | Normalizacja CRBR + alerty CRBR-specyficzne | DONE |
| B4 | CLI — `kasandra fetch / diff / alerts` | TODO |
| B5 | Harmonogram pobierania + automatyzacja | TODO |

**Deadline krytyczny:** CRBR publiczny dostęp kończy się **2026-07-01**.

---

---

## Watchlista Faza 0

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

**Uwaga NIP Asseco:** seed watchlisty ma `5220003307`, KRS API w odpisie zwraca `5220003782`. Do wyjaśnienia przy normalizacji — nieistotne dla CRBR (spółka zwolniona jako GPW).

---

## Postęp — snapshoty i dane

| Spółka | KRS 20.04 | KRS 22.04 | CRBR 22.04 |
|--------|-----------|-----------|------------|
| Żabka Polska | OK | OK | OK (7 beneficjentów) |
| Drutex | OK | OK | OK (1 beneficjent) |
| Grupa Maspex | OK | OK | OK (12 beneficjentów) |
| FAME MMA | OK | OK | OK (2 beneficjentów) |
| Mentzen | OK | OK | OK (2 beneficjentów) |
| Tenczynek Dystrybucja | OK | OK | OK (1 beneficjent) |
| Dino Polska | OK | OK | brak wpisów — zwolnienie GPW |
| Asseco Poland | OK | OK | brak wpisów — zwolnienie GPW |
| Strong Man | OK | OK | brak wpisów — brak zgłoszenia |
| Januszex | OK | OK | brak wpisów — brak zgłoszenia |

**Ścieżki danych:**
- KRS surowe: `dev_ms_data/snapshots/{data}/krs/`
- CRBR surowe: `dev_ms_data/snapshots/2026-04-22/crbr/`
- KRS znormalizowane (baseline): `dev_ms_data/normalized/2026-04-20/krs/`

---

## Model danych — robocze drafty

```python
# model_spolki
# internal_id, KRS, NIP, REGON, nazwa, status, notatki

# model_snapshotu
# company_id, source, collected_at, raw_payload, normalized_payload, hash

# model_zmiany
# company_id, source, field, previous_value, current_value, detected_at, change_type

# model_alertu
# company_id, title, summary, evidence, priority, recommended_next_step, generated_at
```

---

## KRS normalized_payload v0.1

Schemat `normalized_payload` dla snapshotu KRS. Tylko pola których zmiana generuje alert lub daje istotny kontekst.

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
| `wlasciciele.lista[]` | `dzial1.wspolnicySpzoo[]` lub `dzial1.jedynyAkcjonariusz[]` | |
| `pkd_glowny.kod` | `dzial3.przedmiotDzialalnosci.przedmiotPrzewazajacejDzialalnosci[0]` | |
| `distress.dzial4` | `dzial4` niepuste? | bool |
| `distress.dzial5` | `dzial5` niepuste? | bool |
| `distress.dzial6` | `dzial6` niepuste? | bool |
| `distress.dzial6_typy[]` | klucze w `dzial6` | lista stringów |

### Identyfikator osoby (osoba_key)

- **osoba prawna:** `"LE:" + nazwa + (krs || regon)`
- **osoba fizyczna:** `"NAT:" + maska_nazwisko + "|" + maska_imie + "|" + maska_pesel`

Maski deterministyczne (długość = długość oryginału) — ten sam człowiek daje ten sam klucz między snapshotami.

```python
{
  "osoba_key": "NAT:J************|K********|4**********",
  "typ": "fizyczna",
  "display": "K******** J************",
  "funkcja": "PREZES ZARZĄDU",          # tylko zarząd
  "posiadane_udzialy": "100 UDZIAŁÓW",  # tylko wspólnicy
  "calosc": True
}
```

### Pola pomijane w v0.1

- `dzial1.umowaStatut`, `dzial1.emisjeAkcji`, `dzial1.pozostaleInformacje`
- pełna historia wpisów, daty każdej zmiany
- adresy korespondencyjne oddziałów

---

## CRBR normalized_payload v0.1

Schemat `normalized_payload` dla snapshotu CRBR. Produkuje `extract_crbr.py`.

**KRYTYCZNE — maskowanie PESEL:** CRBR zwraca pełne numery PESEL. Skrypt maskuje je przed zapisem (ten sam sposób co KRS API: `pesel[0] + '*' * 10`).

### Status spółki w CRBR

| Wartość | Znaczenie |
|---|---|
| `ok` | Spółka ma wpisy w CRBR, XML pobrany |
| `brak_wpisow` | Portal zwrócił brak wyników |

Dino i Asseco: `brak_wpisow` z powodu zwolnienia GPW (rejestr regulowany).
Strong Man i Januszex: `brak_wpisow` bez oczywistego zwolnienia — potencjalny alert `A-CRBR-BRAK`.

### Typy `charakterUdzialu`

| Kod | Opis | Pole danych |
|---|---|---|
| `1` | bezpośrednia własność | `udzial_ilosc` + `udzial_jednostka_opis` + `rodzaj_wlasnosci_opis` |
| `2` | pośrednia własność / fundacja | `posrednie_opis` (tekst wolny) |
| `3` | inne uprawnienia (senior manager AML) | `inne_uprbo_opis` |

### `osoba_key` w CRBR

Format identyczny jak KRS: `"NAT:{mask_nazwisko}|{mask_imie}|{mask_pesel}"`.
Masking deterministyczny → ten sam beneficjent między snapshotami = ten sam klucz.

---

## Alerty — reguły v0.1

Każdy alert = reguła na diffie dwóch `normalized_payload`. Priorytety: `N / Ś / W / K`.

### Sygnały binarne (distress)

| ID | Trigger | Priorytet |
|---|---|---|
| `A-DZ6-NEW` | `distress.dzial6` przeszedł `false → true` lub nowy typ | **K** |
| `A-DZ4-NEW` | `distress.dzial4` przeszedł `false → true` | **K** |
| `A-DZ5-NEW` | `distress.dzial5` przeszedł `false → true` | **W** |

### Zmiany struktury

| ID | Trigger | Priorytet |
|---|---|---|
| `A-ZARZAD-PREZES` | zmiana osoby na funkcji `PREZES ZARZĄDU` | **W** |
| `A-ZARZAD-SKLAD` | zmiana liczby lub składu `zarzad.sklad[]` | Ś |
| `A-ZARZAD-REPR` | zmiana `sposob_reprezentacji` | Ś |
| `A-WLASC-NOWY` | nowy `osoba_key` w `wlasciciele.lista[]` | **W** |
| `A-WLASC-USUN` | zniknął `osoba_key` z `wlasciciele.lista[]` | **W** |
| `A-WLASC-50PC` | udział wspólnika przekroczył / spadł poniżej 50% | **W** |
| `A-KAPITAL` | zmiana `kapital.wartosc` | Ś |

### Zmiany kontekstowe

| ID | Trigger | Priorytet |
|---|---|---|
| `A-NAZWA` | zmiana `company.nazwa` | Ś |
| `A-FORMA` | zmiana `company.forma` | **W** |
| `A-ADRES` | zmiana adresu | N |
| `A-PKD` | zmiana `pkd_glowny.kod` | Ś |

### Reguły kompozycyjne (v0.2)

| ID | Trigger | Priorytet |
|---|---|---|
| `A-KOMP-ZAR-WLASC` | `A-ZARZAD-*` i `A-WLASC-*` w tej samej spółce w oknie ≤30 dni | **K** |
| `A-SWIEZA-ROTACJA` | spółka < 12 mies. od rejestracji + jakakolwiek zmiana zarządu | **W** |

Wszystkie reguły działają na `osoba_key` (maski), nie pełnych danych. Alert mówi *"zmiana PREZESA: K\*\*\*\*\*\*\*\* → M\*\*\*\*\*\*\*"* — wystarczy jako sygnał, identyfikacja = ręczna weryfikacja w KRS online.

### Alerty CRBR (v0.1)

Reguły specyficzne dla źródła CRBR. Działają na `normalized_payload` z `extract_crbr.py`.

| ID | Trigger | Priorytet | Uwagi |
|---|---|---|---|
| `A-CRBR-BRAK` | `status == "brak_wpisow"` dla sp. z o.o. lub SA niebędącej na GPW | **W** | Strong Man, Januszex — gotowe do zaalertowania |
| `A-CRBR-BEN-NOWY` | nowy `osoba_key` w `beneficjenci[]` między snapshotami | **W** | porównanie po `osoba_key` |
| `A-CRBR-BEN-USUN` | zniknął `osoba_key` z `beneficjenci[]` między snapshotami | **W** | |
| `A-CRBR-BEN-UDZIAL` | zmiana `udzial_ilosc` lub `udzial_jednostka_opis` dla istniejącego beneficjenta | **Ś** | tylko `charakterUdzialu == 1` |
| `A-CRBR-KOREKTA` | `snapshot_meta.korekta == true` w nowym snapshocie | **Ś** | korekta zgłoszenia = coś się zmieniło wstecz |
| `A-CRBR-CHARAKTER` | zmiana `charakter_udzialu_kod` dla istniejącego beneficjenta | **W** | np. 1→2: akcjonariusz → fundacja |

**Spółki zwolnione z CRBR (nie alertujemy `A-CRBR-BRAK`):**
Lista w seedzie watchlisty — obecnie: Dino (GPW), Asseco (GPW).

---

## Gotchas — źródła

### KRS API

- **Endpoint:** `GET https://api-krs.ms.gov.pl/api/krs/OdpisAktualny/{KRS}?rejestr=P&format=json`
- Bez autoryzacji, działa od ręki
- Rozmiary: ~3.6 KB (Januszex) do ~62 KB (Asseco, 169 wpisów)
- Struktura: `odpis.dane.dzial1..dzial6`

**KRYTYCZNE — maskowanie danych osobowych:**  
Publiczne API maskuje imiona, nazwiska i PESEL osób fizycznych (`"J************"`, `"K********"`, `"4**********"`).  
Osoby prawne (np. `MASPEX HOLDING SA`) — pełne dane + KRS.  
Pole `posiadaneUdzialy` — **nie jest maskowane**.

```
Żabka:  ZABKA GROUP SOCIÉTÉ ANONYME — 100% (Luxembourg, brak KRS PL)
Maspex: MASPEX HOLDING SA [KRS 0000725647] — większość udziałów
```

```json
{
  "nazwisko": {"nazwiskoICzlon": "J************"},
  "imiona": {"imie": "K********"},
  "identyfikator": {"pesel": "4**********"},
  "funkcjaWOrganie": "PREZES ZARZĄDU"
}
```

### CRBR

**Portal:** `crbr.podatki.gov.pl/adcrbr/` — Angular SPA chroniona przez Imperva WAF.

**SOAP API (`bramka-crbr.mf.gov.pl:5058`) — niedziałające:**  
Próba 2026-04-21: 10/10 żądań → HTTP 500 `env:Receiver Internal Error`, w tym przykładowy NIP ze specyfikacji MF. Przetestowano: SOAP 1.1/1.2, WS-Addressing, oba endpointy (2020/2022). Diagnoza: backend ESB niedostępny publicznie lub wymaga IP whitelist.

**REST API (`/adcrbr/api/`) — blokowane przez WAF:**  
Zwraca HTTP 200 + `null` dla wszystkich zapytań bez JS (Imperva silent block).

**Playwright — działa:**  
Skrypt `dev_ms_data/scripts/fetch_crbr_playwright.py` uruchamia headless Chrome, przechodzi Imperva challenge, pobiera XML.  
Wyniki dla Fazy 0: 6/10 spółek ma wpisy, 4 nie (2× zwolnienie GPW, 2× brak zgłoszenia).  
Dostęp publiczny CRBR ważny do **2026-07-01** (potem wymagany uzasadniony interes).

**Spółki zwolnione z CRBR:** notowane na regulowanym rynku (GPW) → Dino, Asseco.  
**Brak zgłoszenia sp. z o.o.:** Strong Man, Januszex — potencjalny sygnał alertowy.

---

## Log sesji

### 2026-04-20
- Projekt wszedł w Fazę 0, branch Mat założony
- Watchlista 10 spółek skompletowana
- Snapshot KRS pobrany dla wszystkich 10 (`snapshots/2026-04-20/krs/`)
- Znalezisko: KRS API maskuje dane osób fizycznych
- Blokada: CRBR bez działającego API — odłożone do Fazy 1

### 2026-04-21
- Próba CRBR przez SOAP API MF — 10/10 HTTP 500, wszystkie wariacje
- Skrypt `scripts/fetch_crbr.py` — dokumentacja nieudanej próby
- Decyzja: CRBR odłożona, Faza 0 zamyka się na KRS

### 2026-04-22
- Snapshot KRS odświeżony (`snapshots/2026-04-22/krs/`) — brak zmian merytorycznych vs 20.04
- Znaleziono REST API portalu CRBR (`/adcrbr/api/`) — blokowane przez Imperva WAF (zwraca null bez JS)
- Wdrożony Playwright scraper (`scripts/fetch_crbr_playwright.py`) — działa
- Snapshot CRBR pobrany (`snapshots/2026-04-22/crbr/`): 6 XMLi + log brak_wpisow dla 4
- Rozbieżność NIP Asseco: seed=`5220003307`, KRS API=`5220003782` — do wyjaśnienia
- Strong Man i Januszex: sp. z o.o. bez wpisu w CRBR — potencjalny alert

### 2026-04-23 — Faza 1 start, Blok 3
- Zamknięto Fazę 0, otwarto Fazę 1 — plan bloków B1–B5 w sekcji "Status projektu"
- Napisano `scripts/extract_crbr.py` — normalizacja XML → JSON, PESEL maskowany
- Obsługiwane typy: `karakterUdzialu` 1 (własność), 2 (pośrednia/fundacja), 3 (senior manager)
- Uruchomiono na `snapshots/2026-04-22/crbr/`: 6 OK + 4 brak_wpisow → `normalized/2026-04-22/crbr/`
- Dodano schemat CRBR normalized_payload v0.1 i reguły alertów CRBR (A-CRBR-*) do dev_ms.md
- B3 zamknięty

### 2026-04-23 — Blok 1: SQLite storage
- Zaprojektowano schemat 4 tabel: `companies`, `snapshots`, `changes`, `alerts` (`sql/schema/001_init.sql`)
- Tabela `snapshots.source` TEXT — otwarte na nowe źródła bez migracji struktury
- Rozszerzono `src/kasandra/storage/sqlite.py`: `init_db`, `upsert_company`, `insert_snapshot`, query helpers
- Znormalizowano KRS 2026-04-22 (`normalized/2026-04-22/krs/`)
- Wgrano dane do `var/sqlite/kasandra.sqlite3`: 10 spółek, 30 snapshotów (20 KRS + 10 CRBR)
- Weryfikacja hash: KRS 20.04 vs 22.04 — brak zmian we wszystkich 10 (zgodne z obserwacją z Fazy 0)
- B1 zamknięty

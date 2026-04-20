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

| Spółka | Snapshot KRS | Snapshot CRBR | Diff zrobiony | Alert napisany |
|--------|-------------|---------------|---------------|----------------|
|        | [ ]         | [ ]           | [ ]           | [ ]            |

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

## Log sesji

### 2026-04-20

- Projekt wszedł w Fazę 0
- Branch Mat założony jako osobna przestrzeń robocza

---

## Scratchpad / surowe notatki

<!-- Tu wrzucaj bez formatowania: fragmenty JSON, linki, cytaty z docs, pomysły -->

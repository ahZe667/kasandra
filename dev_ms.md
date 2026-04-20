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

| Spółka | KRS | NIP | REGON | Uwagi |
|--------|-----|-----|-------|-------|
|        |     |     |       |       |

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

---
name: concept-work
description: Fires when the user wants to think through a product/architecture question without touching code. Use proactively for `/concept`, scoping decisions, or when a task is really a docs/decision, not implementation.
---

# Concept work

## Cel

Rozstrzygnac pytanie koncepcyjne albo decyzje produktowa w zgodzie z aktualna faza projektu i istniejacymi `docs/`. Wynik to jawna decyzja, ryzyka i follow-upy — nie kod.

## Constraints

- odpowiedz musi byc osadzona w `docs/` i `docs/examples/`, nie w wyobraznii
- nie wymyslaj danych rynkowych, prawnych ani technicznych bez zrodla
- gdy decyzja zmienia dokumenty lub przyklady, zamknij to przez `docs-sync` w tej samej sesji
- gdy temat przechodzi w implementacje, zatrzymaj sie i zasugeruj `/slice` lub `/source`

## Non-goals

- nie wprowadza zmian w kodzie ani konfiguracji repo "przy okazji"

## Gotchas

- jesli pytanie jest rozmyte, zadaj pytania zawezajace zamiast produkowac szeroka analize

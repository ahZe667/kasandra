---
name: docs-sync
description: Fires when code/contract/assumption changed and docs or examples must follow. Use proactively at the end of any task that touched behavior, after `/slice` or `/source`, or when user invokes `/docs-sync`.
---

# Docs sync

## Cel

Utrzymac spojnosc miedzy `docs/`, `docs/examples/` a aktualnym zachowaniem systemu. Po zmianie kontraktu zadna para dokumentow nie powinna zostac ze soba w sprzecznosci.

## Constraints

- nie dodawaj niepotwierdzonych faktow rynkowych, prawnych ani technicznych
- zmiana faz, zakresu zrodel albo kierunku technicznego wymaga sprawdzenia `docs/03-roadmap-and-gates.md`

## Non-goals

- nie rozszerza opisu poza to, co wynika z realnej zmiany w kodzie lub zalozeniach

## Gotchas

- `docs/examples/` sa zrodlem prawdy dla przykladow alertow i case studies
- overview (`01`), sources-and-alerts (`02`), roadmap (`03`), tech-stack (`04`) laduja sie razem; sprzecznosci miedzy nimi sa zwykle zrodlem bledow Claude'a
- gdy w watpliwosci czy cos sie zmienilo: porownaj `git diff` z ostatnimi tresciami docs

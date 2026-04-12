# Repo check

Użyj tej komendy do końcowego sprawdzenia jakości repo przed oddaniem pracy.

## Procedura

1. Przeczytaj `AGENTS.md`.
2. Przejrzyj zmienione pliki.
3. Jeśli zmienił się kontrakt albo ważne założenie, sprawdź spójność `docs/`, `examples/` i odpowiednich skills.
4. Uruchom `powershell -ExecutionPolicy Bypass -File scripts/repo-check.ps1`.
5. W odpowiedzi wypisz:
   - niespójności,
   - ryzyka,
   - brakujące kroki przed oddaniem.

# Task finish

Zakończ bieżący task. Uruchamia checki, commituje i podsumowuje pracę.

## Procedura

1. Uruchom `powershell -ExecutionPolicy Bypass -File scripts/repo-check.ps1`.
2. Jeśli checki nie przechodzą, napraw problemy i uruchom ponownie.
3. Commituj zmiany zgodnie z konwencją commitów z `AGENTS.md`.
4. Pokaż podsumowanie:
   - co zostało dowiezione
   - jak uruchomić/zweryfikować zmianę
   - znane ograniczenia lub follow-upy

## Input użytkownika

$ARGUMENTS

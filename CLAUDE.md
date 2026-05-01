@.claude/project-memory/MEMORY.md

# Kasandra

Monitoring polskich spolek oparty o dane publiczne. Repo laczy dokumentacje, przyklady i implementacje.

## Repo contract

- Gdy zmienia sie kontrakt, zachowanie albo zalozenie, zsynchronizuj `docs/` w tym samym change secie.

## Workflow agentowy

- Commands (`.claude/commands/`) sa publicznym UX i cienkim routingiem do skilla.
- Skills (`.claude/skills/<nazwa>/SKILL.md`) trzymaja cele, constraints i gotchas — bez railroadingu.
- `CLAUDE.md` + `.claude/project-memory/` trzymaja stabilne fakty projektu

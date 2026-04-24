"""Alert generation: converts change records to user-facing alerts in the alerts table."""

from __future__ import annotations

import json
import sqlite3

from kasandra.processing.priority import NEXT_STEP, PRIORITY, TITLE

# Rules that are internal signals only — not surfaced as user-facing alerts
_SKIP_RULES = {"A-WPIS-NR"}

_PRIORITY_ORDER = {"K": 0, "W": 1, "S": 2, "N": 3}
_PRIORITY_LABELS = {"K": "KRYTYCZNY", "W": "WYSOKI", "S": "ŚREDNI", "N": "NISKI"}


def _build_summary(change: sqlite3.Row) -> str:
    rule = change["alert_rule"]
    try:
        before = json.loads(change["value_before"]) if change["value_before"] else None
        after = json.loads(change["value_after"]) if change["value_after"] else None
    except (json.JSONDecodeError, TypeError):
        before, after = change["value_before"], change["value_after"]

    parts: list[str] = []
    if before and before not in ([], None, "null"):
        parts.append(f"Poprzednio: {before}")
    if after and after not in ([], None, "null"):
        parts.append(f"Teraz: {after}")
    if not parts:
        parts.append("Zmiana wykryta.")

    next_step = NEXT_STEP.get(rule)
    if next_step:
        parts.append(f"Dalszy krok: {next_step}")

    return " | ".join(parts)


def generate_alerts(conn: sqlite3.Connection) -> int:
    """Generate alert records from changes not yet reflected in alerts.

    Each change produces at most one alert (idempotent by change_id in evidence).
    Returns number of new alert records inserted.
    """
    skip_placeholders = ",".join("?" * len(_SKIP_RULES))
    unprocessed = conn.execute(
        f"""
        SELECT c.*, co.slug FROM changes c
        JOIN companies co ON co.id = c.company_id
        WHERE c.alert_rule NOT IN ({skip_placeholders})
          AND NOT EXISTS (
              SELECT 1 FROM alerts a
              WHERE a.company_id = c.company_id
                AND a.alert_rule = c.alert_rule
                AND json_extract(a.evidence, '$[0]') = c.id
          )
        ORDER BY c.id
        """,
        tuple(_SKIP_RULES),
    ).fetchall()

    saved = 0
    for ch in unprocessed:
        rule = ch["alert_rule"]
        priority = PRIORITY.get(rule, "N")
        title = TITLE.get(rule, rule)
        summary = _build_summary(ch)
        evidence = json.dumps([ch["id"]])

        conn.execute(
            """INSERT INTO alerts (company_id, alert_rule, title, summary, evidence, priority)
               VALUES (?,?,?,?,?,?)""",
            (ch["company_id"], rule, title, summary, evidence, priority),
        )
        saved += 1

    conn.commit()
    return saved


def render_digest(conn: sqlite3.Connection) -> str:
    """Render a text digest of new alerts, grouped by priority (K→W→S→N)."""
    alerts = conn.execute(
        """
        SELECT a.*, co.slug FROM alerts a
        JOIN companies co ON co.id = a.company_id
        WHERE a.status = 'new'
        ORDER BY
            CASE a.priority WHEN 'K' THEN 0 WHEN 'W' THEN 1 WHEN 'S' THEN 2 ELSE 3 END,
            co.slug
        """
    ).fetchall()

    if not alerts:
        return "Brak nowych alertów."

    lines = [f"=== Digest alertów ({len(alerts)}) ===", ""]
    current_priority = None

    for a in alerts:
        if a["priority"] != current_priority:
            current_priority = a["priority"]
            label = _PRIORITY_LABELS.get(current_priority, current_priority)
            lines.append(f"--- {label} ---")
        lines.append(f"[{a['priority']}] {a['slug']} — {a['title']} ({a['alert_rule']})")
        lines.append(f"    {a['summary']}")

    return "\n".join(lines)

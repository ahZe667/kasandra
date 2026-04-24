"""Diff engine: detects field-level changes between consecutive snapshots."""

from __future__ import annotations

import json
import sqlite3


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def _load(snap: sqlite3.Row) -> dict | None:
    if snap["normalized_payload"] is None:
        return None
    return json.loads(snap["normalized_payload"])


def _sklad_by_key(members: list) -> dict:
    return {m["osoba_key"]: m for m in members}


def _bens_by_key(bens: list) -> dict:
    return {b["osoba_key"]: b for b in bens}


# --------------------------------------------------------------------------
# KRS diff
# --------------------------------------------------------------------------

def diff_krs(snap_old: sqlite3.Row, snap_new: sqlite3.Row) -> list[dict]:
    old = _load(snap_old)
    new = _load(snap_new)
    if old is None or new is None:
        return []

    changes: list[dict] = []

    # A-WPIS-NR — jakikolwiek nowy wpis rejestrowy
    old_wpis = old["snapshot_meta"].get("nr_ostatniego_wpisu")
    new_wpis = new["snapshot_meta"].get("nr_ostatniego_wpisu")
    if old_wpis != new_wpis:
        changes.append({
            "alert_rule": "A-WPIS-NR",
            "field": "snapshot_meta.nr_ostatniego_wpisu",
            "value_before": json.dumps(old_wpis, ensure_ascii=False),
            "value_after": json.dumps(new_wpis, ensure_ascii=False),
        })

    # A-ZARZAD-SKLAD + A-ZARZAD-PREZES
    old_dict = _sklad_by_key(old["zarzad"].get("sklad", []))
    new_dict = _sklad_by_key(new["zarzad"].get("sklad", []))
    old_keys = set(old_dict)
    new_keys = set(new_dict)
    if old_keys != new_keys:
        dodani = new_keys - old_keys
        usunieci = old_keys - new_keys
        changes.append({
            "alert_rule": "A-ZARZAD-SKLAD",
            "field": "zarzad.sklad",
            "value_before": json.dumps(sorted(usunieci), ensure_ascii=False),
            "value_after": json.dumps(sorted(dodani), ensure_ascii=False),
        })
        # Dodatkowa reguła gdy prezes zarządu konkretnie się zmienił
        prezes_usunieci = {k for k in usunieci if old_dict[k].get("funkcja") == "PREZES ZARZĄDU"}
        prezes_dodani = {k for k in dodani if new_dict[k].get("funkcja") == "PREZES ZARZĄDU"}
        if prezes_usunieci or prezes_dodani:
            changes.append({
                "alert_rule": "A-ZARZAD-PREZES",
                "field": "zarzad.sklad",
                "value_before": json.dumps(sorted(prezes_usunieci), ensure_ascii=False),
                "value_after": json.dumps(sorted(prezes_dodani), ensure_ascii=False),
            })

    # A-ADRES
    old_adres = old.get("adres", {})
    new_adres = new.get("adres", {})
    if old_adres != new_adres:
        changes.append({
            "alert_rule": "A-ADRES",
            "field": "adres",
            "value_before": json.dumps(old_adres, ensure_ascii=False),
            "value_after": json.dumps(new_adres, ensure_ascii=False),
        })

    # A-KAPITAL
    old_kap = old.get("kapital", {})
    new_kap = new.get("kapital", {})
    if old_kap != new_kap:
        changes.append({
            "alert_rule": "A-KAPITAL",
            "field": "kapital",
            "value_before": json.dumps(old_kap, ensure_ascii=False),
            "value_after": json.dumps(new_kap, ensure_ascii=False),
        })

    return changes


# --------------------------------------------------------------------------
# CRBR diff
# --------------------------------------------------------------------------

def diff_crbr(snap_old: sqlite3.Row, snap_new: sqlite3.Row) -> list[dict]:
    old = _load(snap_old)
    new = _load(snap_new)

    if old is None and new is None:
        return []

    if old is None and new is not None:
        bens = set(_bens_by_key(new.get("beneficjenci", [])))
        return [{
            "alert_rule": "A-CRBR-BEN-NOWY-WPIS",
            "field": "beneficjenci",
            "value_before": json.dumps([], ensure_ascii=False),
            "value_after": json.dumps(sorted(bens), ensure_ascii=False),
        }]

    if old is not None and new is None:
        bens = set(_bens_by_key(old.get("beneficjenci", [])))
        return [{
            "alert_rule": "A-CRBR-BEN-ZNIKNAL-WPIS",
            "field": "beneficjenci",
            "value_before": json.dumps(sorted(bens), ensure_ascii=False),
            "value_after": json.dumps([], ensure_ascii=False),
        }]

    old_dict = _bens_by_key(old.get("beneficjenci", []))
    new_dict = _bens_by_key(new.get("beneficjenci", []))
    old_keys = set(old_dict)
    new_keys = set(new_dict)

    if old_keys == new_keys:
        return []

    changes: list[dict] = []
    dodani = new_keys - old_keys
    usunieci = old_keys - new_keys

    if dodani:
        changes.append({
            "alert_rule": "A-CRBR-BEN-NOWY",
            "field": "beneficjenci",
            "value_before": json.dumps([], ensure_ascii=False),
            "value_after": json.dumps(sorted(dodani), ensure_ascii=False),
        })
    if usunieci:
        changes.append({
            "alert_rule": "A-CRBR-BEN-USUN",
            "field": "beneficjenci",
            "value_before": json.dumps(sorted(usunieci), ensure_ascii=False),
            "value_after": json.dumps([], ensure_ascii=False),
        })
    return changes


# --------------------------------------------------------------------------
# A-CRBR-BRAK — statyczny check: spółka bez wpisu CRBR, nigdy go nie miała
# --------------------------------------------------------------------------

def check_crbr_brak(conn: sqlite3.Connection) -> int:
    """Flag non-exempt companies whose latest CRBR snapshot is brak_wpisow and never had ok.

    Returns number of new change records inserted.
    """
    companies = conn.execute(
        "SELECT id, slug FROM companies WHERE crbr_exempt = 0"
    ).fetchall()
    saved = 0
    for company in companies:
        cid = company["id"]
        latest = conn.execute(
            """SELECT * FROM snapshots
               WHERE company_id=? AND source='crbr'
               ORDER BY collected_at DESC LIMIT 1""",
            (cid,),
        ).fetchone()
        if latest is None or latest["status"] != "brak_wpisow":
            continue
        # Flaguj tylko gdy spółka nigdy nie miała ok (nie flaguj po utracie wpisu — to A-CRBR-BEN-ZNIKNAL-WPIS)
        ever_ok = conn.execute(
            "SELECT id FROM snapshots WHERE company_id=? AND source='crbr' AND status='ok' LIMIT 1",
            (cid,),
        ).fetchone()
        if ever_ok:
            continue
        # Idempotentność: pomiń jeśli już oflagowano dla tego snapshotu
        existing = conn.execute(
            "SELECT id FROM changes WHERE company_id=? AND alert_rule='A-CRBR-BRAK' AND snapshot_new_id=?",
            (cid, latest["id"]),
        ).fetchone()
        if existing:
            continue
        conn.execute(
            """INSERT INTO changes
               (company_id, source, alert_rule, field, value_before, value_after, snapshot_old_id, snapshot_new_id)
               VALUES (?,?,?,?,?,?,?,?)""",
            (cid, "crbr", "A-CRBR-BRAK", None,
             json.dumps(None), json.dumps("brak_wpisow"),
             None, latest["id"]),
        )
        saved += 1
        print(f"  {company['slug']:12s} crbr [A-CRBR-BRAK] zapisano")
    return saved


# --------------------------------------------------------------------------
# Persist changes
# --------------------------------------------------------------------------

def save_changes(
    conn: sqlite3.Connection,
    company_id: int,
    source: str,
    snap_old: sqlite3.Row,
    snap_new: sqlite3.Row,
    field_changes: list[dict],
) -> int:
    saved = 0
    for ch in field_changes:
        existing = conn.execute(
            """SELECT id FROM changes
               WHERE company_id=? AND snapshot_old_id=? AND snapshot_new_id=? AND alert_rule=? AND field IS ?""",
            (company_id, snap_old["id"], snap_new["id"], ch["alert_rule"], ch.get("field")),
        ).fetchone()
        if existing:
            continue
        conn.execute(
            """INSERT INTO changes
               (company_id, source, alert_rule, field, value_before, value_after, snapshot_old_id, snapshot_new_id)
               VALUES (?,?,?,?,?,?,?,?)""",
            (
                company_id, source, ch["alert_rule"], ch.get("field"),
                ch["value_before"], ch["value_after"],
                snap_old["id"], snap_new["id"],
            ),
        )
        saved += 1
    return saved


# --------------------------------------------------------------------------
# Main diff loop
# --------------------------------------------------------------------------

def run_diff(conn: sqlite3.Connection) -> int:
    """Diff latest two snapshots per company/source. Returns total new change records."""
    companies = conn.execute("SELECT id, slug FROM companies ORDER BY slug").fetchall()
    total = 0

    for company in companies:
        cid = company["id"]
        slug = company["slug"]

        for source in ("krs", "crbr"):
            snaps = conn.execute(
                "SELECT * FROM snapshots WHERE company_id=? AND source=? ORDER BY collected_at ASC",
                (cid, source),
            ).fetchall()

            if len(snaps) < 2:
                continue

            snap_old = snaps[-2]
            snap_new = snaps[-1]

            if (
                snap_old["payload_hash"] is not None
                and snap_new["payload_hash"] is not None
                and snap_old["payload_hash"] == snap_new["payload_hash"]
            ):
                print(f"  {slug:12s} {source:4s} — bez zmian (hash identyczny)")
                continue

            field_changes = diff_krs(snap_old, snap_new) if source == "krs" else diff_crbr(snap_old, snap_new)

            if not field_changes:
                print(f"  {slug:12s} {source:4s} — hash różny, diff pusty")
                continue

            saved = save_changes(conn, cid, source, snap_old, snap_new, field_changes)
            total += saved
            for ch in field_changes:
                print(f"  {slug:12s} {source:4s} [{ch['alert_rule']}] zapisano: {ch.get('field')}")

    total += check_crbr_brak(conn)
    conn.commit()
    print(f"\nDiff gotowy. Nowych rekordów w changes: {total}")
    return total

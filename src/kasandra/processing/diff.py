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


def _ch(alert_rule: str, field: str, before, after) -> dict:
    return {
        "alert_rule": alert_rule,
        "field": field,
        "value_before": json.dumps(before, ensure_ascii=False),
        "value_after": json.dumps(after, ensure_ascii=False),
    }


# --------------------------------------------------------------------------
# KRS diff
# --------------------------------------------------------------------------

def diff_krs(snap_old: sqlite3.Row, snap_new: sqlite3.Row) -> list[dict]:
    old = _load(snap_old)
    new = _load(snap_new)
    if old is None or new is None:
        return []

    changes: list[dict] = []

    old_wpis = old["snapshot_meta"].get("nr_ostatniego_wpisu")
    new_wpis = new["snapshot_meta"].get("nr_ostatniego_wpisu")
    if old_wpis != new_wpis:
        changes.append(_ch("A-WPIS-NR", "snapshot_meta.nr_ostatniego_wpisu", old_wpis, new_wpis))

    old_dict = _sklad_by_key(old["zarzad"].get("sklad", []))
    new_dict = _sklad_by_key(new["zarzad"].get("sklad", []))
    old_keys = set(old_dict)
    new_keys = set(new_dict)
    if old_keys != new_keys:
        dodani = new_keys - old_keys
        usunieci = old_keys - new_keys
        changes.append(_ch("A-ZARZAD-SKLAD", "zarzad.sklad", sorted(usunieci), sorted(dodani)))
        prezes_usunieci = {k for k in usunieci if old_dict[k].get("funkcja") == "PREZES ZARZĄDU"}
        prezes_dodani = {k for k in dodani if new_dict[k].get("funkcja") == "PREZES ZARZĄDU"}
        if prezes_usunieci or prezes_dodani:
            changes.append(_ch("A-ZARZAD-PREZES", "zarzad.sklad", sorted(prezes_usunieci), sorted(prezes_dodani)))

    old_adres = old.get("adres", {})
    new_adres = new.get("adres", {})
    if old_adres != new_adres:
        changes.append(_ch("A-ADRES", "adres", old_adres, new_adres))

    old_kap = old.get("kapital", {})
    new_kap = new.get("kapital", {})
    if old_kap != new_kap:
        changes.append(_ch("A-KAPITAL", "kapital", old_kap, new_kap))

    old_wlasc = {w["osoba_key"] for w in old.get("wlasciciele", {}).get("lista", [])}
    new_wlasc = {w["osoba_key"] for w in new.get("wlasciciele", {}).get("lista", [])}
    if old_wlasc != new_wlasc:
        dodani = new_wlasc - old_wlasc
        usunieci = old_wlasc - new_wlasc
        if dodani:
            changes.append(_ch("A-WLASC-NOWY", "wlasciciele.lista", [], sorted(dodani)))
        if usunieci:
            changes.append(_ch("A-WLASC-USUN", "wlasciciele.lista", sorted(usunieci), []))

    old_repr = old.get("zarzad", {}).get("sposob_reprezentacji")
    new_repr = new.get("zarzad", {}).get("sposob_reprezentacji")
    if old_repr != new_repr:
        changes.append(_ch("A-ZARZAD-REPR", "zarzad.sposob_reprezentacji", old_repr, new_repr))

    old_nazwa = old.get("company", {}).get("nazwa")
    new_nazwa = new.get("company", {}).get("nazwa")
    if old_nazwa != new_nazwa:
        changes.append(_ch("A-NAZWA", "company.nazwa", old_nazwa, new_nazwa))

    old_forma = old.get("company", {}).get("forma")
    new_forma = new.get("company", {}).get("forma")
    if old_forma != new_forma:
        changes.append(_ch("A-FORMA", "company.forma", old_forma, new_forma))

    old_pkd = old.get("pkd_glowny", {}).get("kod")
    new_pkd = new.get("pkd_glowny", {}).get("kod")
    if old_pkd != new_pkd:
        changes.append(_ch("A-PKD", "pkd_glowny.kod", old_pkd, new_pkd))

    old_d = old.get("distress", {})
    new_d = new.get("distress", {})
    if not old_d.get("dzial6") and new_d.get("dzial6"):
        changes.append(_ch("A-DZ6-NEW", "distress.dzial6", False, new_d.get("dzial6_typy", [])))
    if not old_d.get("dzial4") and new_d.get("dzial4"):
        changes.append(_ch("A-DZ4-NEW", "distress.dzial4", False, True))
    if not old_d.get("dzial5") and new_d.get("dzial5"):
        changes.append(_ch("A-DZ5-NEW", "distress.dzial5", False, True))

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
        return [_ch("A-CRBR-BEN-NOWY-WPIS", "beneficjenci", [], sorted(bens))]
    if old is not None and new is None:
        bens = set(_bens_by_key(old.get("beneficjenci", [])))
        return [_ch("A-CRBR-BEN-ZNIKNAL-WPIS", "beneficjenci", sorted(bens), [])]

    old_keys = set(_bens_by_key(old.get("beneficjenci", [])))
    new_keys = set(_bens_by_key(new.get("beneficjenci", [])))
    if old_keys == new_keys:
        return []

    dodani = new_keys - old_keys
    usunieci = old_keys - new_keys
    changes: list[dict] = []
    if dodani:
        changes.append(_ch("A-CRBR-BEN-NOWY", "beneficjenci", [], sorted(dodani)))
    if usunieci:
        changes.append(_ch("A-CRBR-BEN-USUN", "beneficjenci", sorted(usunieci), []))
    return changes


# --------------------------------------------------------------------------
# VAT diff
# --------------------------------------------------------------------------

def diff_vat(snap_old: sqlite3.Row, snap_new: sqlite3.Row) -> list[dict]:
    old = _load(snap_old)
    new = _load(snap_new)
    if old is None or new is None:
        return []

    changes: list[dict] = []

    old_status = old.get("vat", {}).get("status")
    new_status = new.get("vat", {}).get("status")
    if old_status != new_status:
        changes.append(_ch("A-VAT-STATUS", "vat.status", old_status, new_status))

    old_konta = set(old.get("vat", {}).get("konta", []))
    new_konta = set(new.get("vat", {}).get("konta", []))
    if old_konta != new_konta:
        nowe = new_konta - old_konta
        usuniete = old_konta - new_konta
        if nowe:
            changes.append(_ch("A-VAT-KONTO-NOWE", "vat.konta", [], sorted(nowe)))
        if usuniete:
            changes.append(_ch("A-VAT-KONTO-USUN", "vat.konta", sorted(usuniete), []))

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
            "SELECT * FROM snapshots WHERE company_id=? AND source='crbr' ORDER BY collected_at DESC LIMIT 1",
            (cid,),
        ).fetchone()
        if latest is None or latest["status"] != "brak_wpisow":
            continue
        # Skip if ever had ok (then it's A-CRBR-BEN-ZNIKNAL-WPIS, not A-CRBR-BRAK)
        if conn.execute(
            "SELECT 1 FROM snapshots WHERE company_id=? AND source='crbr' AND status='ok' LIMIT 1", (cid,)
        ).fetchone():
            continue
        if conn.execute(
            "SELECT 1 FROM changes WHERE company_id=? AND alert_rule='A-CRBR-BRAK'", (cid,)
        ).fetchone():
            continue
        conn.execute(
            """INSERT INTO changes
               (company_id, source, alert_rule, field, value_before, value_after, snapshot_old_id, snapshot_new_id)
               VALUES (?,?,?,?,?,?,?,?)""",
            (cid, "crbr", "A-CRBR-BRAK", None, json.dumps(None), json.dumps("brak_wpisow"), None, latest["id"]),
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
            (company_id, source, ch["alert_rule"], ch.get("field"),
             ch["value_before"], ch["value_after"], snap_old["id"], snap_new["id"]),
        )
        saved += 1
    return saved


# --------------------------------------------------------------------------
# Main diff loop
# --------------------------------------------------------------------------

_DIFF_FN = {"krs": diff_krs, "vat": diff_vat, "crbr": diff_crbr}


def run_diff(conn: sqlite3.Connection) -> int:
    """Diff latest two snapshots per company/source. Returns total new change records."""
    companies = conn.execute("SELECT id, slug FROM companies ORDER BY slug").fetchall()
    total = 0

    for company in companies:
        cid = company["id"]
        slug = company["slug"]

        for source in ("krs", "vat"):  # CRBR zawieszone 2026-04-28
            snaps = conn.execute(
                "SELECT * FROM snapshots WHERE company_id=? AND source=? AND is_synthetic=0 ORDER BY collected_at ASC",
                (cid, source),
            ).fetchall()

            if len(snaps) < 2:
                continue

            snap_old = snaps[-2]
            snap_new = snaps[-1]

            if snap_old["payload_hash"] == snap_new["payload_hash"]:
                print(f"  {slug:12s} {source:4s} - bez zmian (hash identyczny)")
                continue

            field_changes = _DIFF_FN[source](snap_old, snap_new)

            if not field_changes:
                print(f"  {slug:12s} {source:4s} - hash rozny, diff pusty")
                continue

            saved = save_changes(conn, cid, source, snap_old, snap_new, field_changes)
            total += saved
            if saved > 0:
                print(f"  {slug:12s} {source:4s} zapisano {saved} zmian")

    # total += check_crbr_brak(conn)  # CRBR zawieszone 2026-04-28
    conn.commit()
    print(f"\nDiff gotowy. Nowych rekordów w changes: {total}")
    return total

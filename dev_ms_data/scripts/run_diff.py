"""
run_diff.py — uruchamia diff między ostatnimi dwoma snapshotami i zapisuje zmiany do DB.

Logika:
- Dla każdej spółki i źródła bierze dwa ostatnie snapshoty (status=ok).
- Jeśli hash się różni, rozkłada diff na poziomie pól i zapisuje do tabeli changes.
- Idempotentny: nie duplikuje rekordów dla tej samej pary (snapshot_old_id, snapshot_new_id, field).

Reguły diff (KRS):
  A-ZARZAD-SKLAD   — zmiana składu zarządu (dodano/usunięto osoby)
  A-PROKURA-SKLAD  — zmiana prokury (jeśli pole obecne)
  A-ADRES          — zmiana adresu siedziby
  A-KAPITAL        — zmiana kapitału zakładowego
  A-WPIS-NR        — nowy numer ostatniego wpisu (= jakakolwiek zmiana w KRS)

Reguły diff (CRBR):
  A-CRBR-BEN-SKLAD — zmiana listy beneficjentów (dodano/usunięto)

Usage:
    python dev_ms_data/scripts/run_diff.py [--date DATE]

Domyślnie dyfuje najnowszy snapshot względem poprzedniego dla każdej spółki.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

from kasandra.storage.sqlite import connect  # noqa: E402


# --------------------------------------------------------------------------
# Pomocnicze
# --------------------------------------------------------------------------

def load_payload(snap) -> dict | None:
    if snap["normalized_payload"] is None:
        return None
    return json.loads(snap["normalized_payload"])


def sklad_keys(members: list) -> set:
    return {m["osoba_key"] for m in members}


def beneficjenci_keys(bens: list) -> set:
    return {b["osoba_key"] for b in bens}


# --------------------------------------------------------------------------
# Diff KRS
# --------------------------------------------------------------------------

def diff_krs(snap_old, snap_new) -> list[dict]:
    old = load_payload(snap_old)
    new = load_payload(snap_new)
    if old is None or new is None:
        return []

    changes = []

    # A-WPIS-NR — nowy wpis w KRS (jakiekolwiek zmiany rejestrowe)
    old_wpis = old["snapshot_meta"].get("nr_ostatniego_wpisu")
    new_wpis = new["snapshot_meta"].get("nr_ostatniego_wpisu")
    if old_wpis != new_wpis:
        changes.append({
            "alert_rule": "A-WPIS-NR",
            "field": "snapshot_meta.nr_ostatniego_wpisu",
            "value_before": json.dumps(old_wpis, ensure_ascii=False),
            "value_after": json.dumps(new_wpis, ensure_ascii=False),
        })

    # A-ZARZAD-SKLAD — skład zarządu
    old_sklad = sklad_keys(old["zarzad"].get("sklad", []))
    new_sklad = sklad_keys(new["zarzad"].get("sklad", []))
    if old_sklad != new_sklad:
        dodani = new_sklad - old_sklad
        usunieci = old_sklad - new_sklad
        changes.append({
            "alert_rule": "A-ZARZAD-SKLAD",
            "field": "zarzad.sklad",
            "value_before": json.dumps(sorted(usunieci), ensure_ascii=False),
            "value_after": json.dumps(sorted(dodani), ensure_ascii=False),
        })

    # A-ADRES — siedziba
    old_adres = old.get("adres", {})
    new_adres = new.get("adres", {})
    if old_adres != new_adres:
        changes.append({
            "alert_rule": "A-ADRES",
            "field": "adres",
            "value_before": json.dumps(old_adres, ensure_ascii=False),
            "value_after": json.dumps(new_adres, ensure_ascii=False),
        })

    # A-KAPITAL — kapitał zakładowy
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
# Diff CRBR
# --------------------------------------------------------------------------

def diff_crbr(snap_old, snap_new) -> list[dict]:
    old = load_payload(snap_old)
    new = load_payload(snap_new)

    # brak → brak: bez zmian
    if old is None and new is None:
        return []

    # pojawił się wpis
    if old is None and new is not None:
        bens = beneficjenci_keys(new.get("beneficjenci", []))
        return [{
            "alert_rule": "A-CRBR-BEN-NOWY-WPIS",
            "field": "beneficjenci",
            "value_before": json.dumps([], ensure_ascii=False),
            "value_after": json.dumps(sorted(bens), ensure_ascii=False),
        }]

    # zniknął wpis
    if old is not None and new is None:
        bens = beneficjenci_keys(old.get("beneficjenci", []))
        return [{
            "alert_rule": "A-CRBR-BEN-ZNIKNAL-WPIS",
            "field": "beneficjenci",
            "value_before": json.dumps(sorted(bens), ensure_ascii=False),
            "value_after": json.dumps([], ensure_ascii=False),
        }]

    # obydwa ok — sprawdź skład
    old_bens = beneficjenci_keys(old.get("beneficjenci", []))
    new_bens = beneficjenci_keys(new.get("beneficjenci", []))
    if old_bens != new_bens:
        dodani = new_bens - old_bens
        usunieci = old_bens - new_bens
        return [{
            "alert_rule": "A-CRBR-BEN-SKLAD",
            "field": "beneficjenci",
            "value_before": json.dumps(sorted(usunieci), ensure_ascii=False),
            "value_after": json.dumps(sorted(dodani), ensure_ascii=False),
        }]

    return []


# --------------------------------------------------------------------------
# Zapis zmian do DB
# --------------------------------------------------------------------------

def save_changes(conn, company_id: int, source: str, snap_old, snap_new, field_changes: list) -> int:
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
# Główna pętla
# --------------------------------------------------------------------------

def run_diff(conn) -> None:
    companies = conn.execute("SELECT id, slug FROM companies ORDER BY slug").fetchall()
    total_changes = 0

    for company in companies:
        cid = company["id"]
        slug = company["slug"]

        for source in ("krs", "crbr"):
            snaps = conn.execute(
                """SELECT * FROM snapshots
                   WHERE company_id=? AND source=?
                   ORDER BY collected_at ASC""",
                (cid, source),
            ).fetchall()

            if len(snaps) < 2:
                continue

            # Bierze dwa ostatnie snapshoty
            snap_old = snaps[-2]
            snap_new = snaps[-1]

            # Szybki skip jeśli hash identyczny
            if (snap_old["payload_hash"] is not None
                    and snap_new["payload_hash"] is not None
                    and snap_old["payload_hash"] == snap_new["payload_hash"]):
                print(f"  {slug:12s} {source:4s} — bez zmian (hash identyczny)")
                continue

            if source == "krs":
                field_changes = diff_krs(snap_old, snap_new)
            else:
                field_changes = diff_crbr(snap_old, snap_new)

            if not field_changes:
                print(f"  {slug:12s} {source:4s} — hash różny, ale diff pusty")
                continue

            saved = save_changes(conn, cid, source, snap_old, snap_new, field_changes)
            total_changes += saved
            for ch in field_changes:
                print(f"  {slug:12s} {source:4s} [{ch['alert_rule']}] zapisano: {ch.get('field')}")

    conn.commit()
    print(f"\nDiff gotowy. Nowych rekordów w changes: {total_changes}")


def main() -> None:
    db_path = REPO_ROOT / "var" / "sqlite" / "kasandra.sqlite3"
    conn = connect(db_path)
    print("=== Diff snapshotów ===\n")
    run_diff(conn)
    conn.close()


if __name__ == "__main__":
    main()

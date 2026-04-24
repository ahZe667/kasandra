"""
import_to_db.py — seed bazy danych Kasandra z istniejących znormalizowanych danych.

Wgrywa:
  1. Watchlistę 10 spółek (Faza 0)
  2. Snapshoty KRS:  normalized/2026-04-20/krs/ i normalized/2026-04-22/krs/
  3. Snapshoty CRBR: normalized/2026-04-22/crbr/

Usage:
    python dev_ms_data/scripts/import_to_db.py [--db PATH]

Domyślna ścieżka DB: var/sqlite/kasandra.sqlite3
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

from kasandra.storage.sqlite import (  # noqa: E402
    connect,
    init_db,
    insert_snapshot,
    upsert_company,
)

# --------------------------------------------------------------------------
# Watchlista Fazy 0 — source of truth: dev_ms.md
# crbr_exempt = True dla spółek notowanych na GPW (zwolnione z CRBR)
# --------------------------------------------------------------------------
WATCHLIST = [
    dict(krs="0000636642", nip="5223071241", regon="365388398",  slug="zabka",       crbr_exempt=False, notes="duży retail, dużo zmian operacyjnych"),
    dict(krs="0000140428", nip="8421622720", regon="771564493",  slug="drutex",      crbr_exempt=False, notes="producent okien/drzwi, stabilna"),
    dict(krs="0000898248", nip="5512617657", regon="122948517",  slug="maspex",      crbr_exempt=False, notes="FMCG, Tymbark — holding"),
    dict(krs="0000408273", nip="6211766191", regon="300820828",  slug="dino",        crbr_exempt=True,  notes="retail, notowana GPW"),
    dict(krs="0000033391", nip="5220003307", regon="010337520",  slug="asseco",      crbr_exempt=True,  notes="IT, notowana GPW; NIP w KRS API: 5220003782"),
    dict(krs="0000883491", nip="7773370464", regon="388181156",  slug="fame_mma",    crbr_exempt=False, notes="młoda SA, dynamiczne zmiany"),
    dict(krs="0001008036", nip="5273032556", regon="523923895",  slug="mentzen",     crbr_exempt=False, notes="nowa SA, Mentzen — ciekawy CRBR"),
    dict(krs="0000055656", nip="5862021333", regon="191892935",  slug="strong_man",  crbr_exempt=False, notes="stara spółka, logistyka Malbork"),
    dict(krs="0000864032", nip="9462683417", regon="381368271",  slug="tenczynek",   crbr_exempt=False, notes="Palikot, strata, ciekawy profil ryzyka"),
    dict(krs="0000779880", nip="5272889007", regon="382903625",  slug="januszex",    crbr_exempt=False, notes="mała spółka, 100% właściciel = prezes"),
]

# Mapowanie KRS -> slug (do łączenia snapshotów z companies)
KRS_TO_SLUG = {w["krs"]: w["slug"] for w in WATCHLIST}

# CRBR używa NIP — Asseco ma rozbieżność NIP (seed vs KRS API)
# W CRBR log: asseco ma nip=5220003782 (z KRS API), nie seed
NIP_TO_KRS = {w["nip"]: w["krs"] for w in WATCHLIST}
NIP_TO_KRS["5220003782"] = "0000033391"  # Asseco NIP z KRS API -> właściwy KRS


def import_krs_snapshots(conn, normalized_dir: Path, collected_at: str) -> int:
    krs_dir = normalized_dir / "krs"
    if not krs_dir.exists():
        print(f"  SKIP: brak katalogu {krs_dir}")
        return 0

    count = 0
    for json_path in sorted(krs_dir.glob("*.json")):
        with open(json_path, encoding="utf-8") as fp:
            payload = json.load(fp)

        krs = payload["company"]["krs"]
        row = conn.execute("SELECT id FROM companies WHERE krs = ?", (krs,)).fetchone()
        if row is None:
            print(f"  WARN: KRS {krs} nie istnieje w companies, pomijam {json_path.name}")
            continue

        # nazwa aktualizowana z pierwszego snapshotu
        if payload["company"].get("nazwa"):
            conn.execute(
                "UPDATE companies SET nazwa = ? WHERE id = ? AND nazwa IS NULL",
                (payload["company"]["nazwa"], row["id"]),
            )

        raw_path = str(
            Path("dev_ms_data/snapshots") / collected_at / "krs" / json_path.name.replace(".json", ".json")
        ).replace("\\", "/")
        # raw file ma to samo imię ale w snapshotach
        raw_path = f"dev_ms_data/snapshots/{collected_at}/krs/{json_path.stem}.json"

        snap_id = insert_snapshot(
            conn,
            company_id=row["id"],
            source="krs",
            collected_at=collected_at,
            status="ok",
            normalized_payload=payload,
            raw_path=raw_path,
        )
        count += 1
        print(f"  KRS {collected_at}: {json_path.name} -> snapshot #{snap_id}")

    return count


def import_crbr_snapshots(conn, normalized_dir: Path, collected_at: str) -> int:
    crbr_dir = normalized_dir / "crbr"
    if not crbr_dir.exists():
        print(f"  SKIP: brak katalogu {crbr_dir}")
        return 0

    count = 0
    for json_path in sorted(crbr_dir.glob("*.json")):
        with open(json_path, encoding="utf-8") as fp:
            payload = json.load(fp)

        nip = payload["company"].get("nip")
        krs = NIP_TO_KRS.get(nip)
        if krs is None:
            print(f"  WARN: NIP {nip} bez mapowania na KRS, pomijam {json_path.name}")
            continue

        row = conn.execute("SELECT id FROM companies WHERE krs = ?", (krs,)).fetchone()
        if row is None:
            print(f"  WARN: KRS {krs} (NIP {nip}) nie w companies, pomijam")
            continue

        status = payload.get("status", "ok")
        actual_payload = payload if status == "ok" else None

        raw_slug = payload.get("slug", "")
        raw_path = (
            f"dev_ms_data/snapshots/{collected_at}/crbr/{nip}_{raw_slug}.xml"
            if status == "ok" else None
        )

        snap_id = insert_snapshot(
            conn,
            company_id=row["id"],
            source="crbr",
            collected_at=collected_at,
            status=status,
            normalized_payload=actual_payload,
            raw_path=raw_path,
        )
        count += 1
        ben = len(payload.get("beneficjenci", []))
        print(f"  CRBR {collected_at}: {json_path.name} [{status}, {ben} ben.] -> snapshot #{snap_id}")

    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Importuj dane Fazy 0 do DB Kasandra.")
    parser.add_argument("--db", type=Path, default=None, help="Ścieżka do pliku .sqlite3")
    args = parser.parse_args()

    db_path = args.db or (REPO_ROOT / "var" / "sqlite" / "kasandra.sqlite3")
    normalized_root = REPO_ROOT / "dev_ms_data" / "normalized"

    print(f"DB: {db_path}")
    conn = connect(db_path)
    init_db(conn)

    # 1. Seed watchlisty
    print("\n[1] Seed companies (watchlista Fazy 0)")
    for w in WATCHLIST:
        cid = upsert_company(conn, **w)
        print(f"  {w['slug']:12s} KRS={w['krs']} -> company #{cid}")

    # 2. KRS 2026-04-20
    print("\n[2] Import KRS 2026-04-20")
    import_krs_snapshots(conn, normalized_root / "2026-04-20", "2026-04-20")

    # 3. KRS 2026-04-22
    print("\n[3] Import KRS 2026-04-22")
    import_krs_snapshots(conn, normalized_root / "2026-04-22", "2026-04-22")

    # 4. CRBR 2026-04-22
    print("\n[4] Import CRBR 2026-04-22")
    import_crbr_snapshots(conn, normalized_root / "2026-04-22", "2026-04-22")

    conn.commit()

    # Weryfikacja
    print("\n[OK] Podsumowanie DB:")
    companies = conn.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
    snapshots = conn.execute("SELECT COUNT(*) FROM snapshots").fetchone()[0]
    by_source = conn.execute(
        "SELECT source, status, COUNT(*) as n FROM snapshots GROUP BY source, status ORDER BY source, status"
    ).fetchall()
    print(f"  companies: {companies}")
    print(f"  snapshots: {snapshots}")
    for row in by_source:
        print(f"    {row[0]:6s} / {row[1]:12s}: {row[2]}")

    conn.close()


if __name__ == "__main__":
    main()

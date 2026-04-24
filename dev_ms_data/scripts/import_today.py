"""
import_today.py — importuje snapshoty z konkretnej daty do DB.

Usage:
    python dev_ms_data/scripts/import_today.py <date>

Przykład:
    python dev_ms_data/scripts/import_today.py 2026-04-23
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

from kasandra.storage.sqlite import connect, init_db, insert_snapshot  # noqa: E402

NIP_TO_KRS = {
    "5223071241": "0000636642",
    "8421622720": "0000140428",
    "5512617657": "0000898248",
    "6211766191": "0000408273",
    "5220003307": "0000033391",
    "5220003782": "0000033391",
    "7773370464": "0000883491",
    "5273032556": "0001008036",
    "5862021333": "0000055656",
    "9462683417": "0000864032",
    "5272889007": "0000779880",
}


def import_date(date: str) -> None:
    import json

    db_path = REPO_ROOT / "var" / "sqlite" / "kasandra.sqlite3"
    normalized_root = REPO_ROOT / "dev_ms_data" / "normalized" / date

    conn = connect(db_path)
    init_db(conn)

    # KRS
    krs_dir = normalized_root / "krs"
    krs_count = 0
    if krs_dir.exists():
        for json_path in sorted(f for f in krs_dir.glob("*.json") if not f.name.startswith("_")):
            with open(json_path, encoding="utf-8") as fp:
                payload = json.load(fp)
            krs = payload["company"]["krs"]
            row = conn.execute("SELECT id FROM companies WHERE krs = ?", (krs,)).fetchone()
            if row is None:
                print(f"  WARN: KRS {krs} nie w companies, pomijam")
                continue
            snap_id = insert_snapshot(
                conn,
                company_id=row["id"],
                source="krs",
                collected_at=date,
                status="ok",
                normalized_payload=payload,
                raw_path=f"dev_ms_data/snapshots/{date}/krs/{json_path.stem}.json",
            )
            krs_count += 1
            print(f"  KRS {date}: {json_path.name} -> snapshot #{snap_id}")
    else:
        print(f"  SKIP: brak {krs_dir}")

    # CRBR
    crbr_dir = normalized_root / "crbr"
    crbr_count = 0
    if crbr_dir.exists():
        for json_path in sorted(f for f in crbr_dir.glob("*.json") if not f.name.startswith("_")):
            with open(json_path, encoding="utf-8") as fp:
                payload = json.load(fp)
            nip = payload["company"].get("nip")
            krs = NIP_TO_KRS.get(nip)
            if krs is None:
                print(f"  WARN: NIP {nip} bez mapowania, pomijam {json_path.name}")
                continue
            row = conn.execute("SELECT id FROM companies WHERE krs = ?", (krs,)).fetchone()
            if row is None:
                print(f"  WARN: KRS {krs} nie w companies, pomijam")
                continue
            status = payload.get("status", "ok")
            actual_payload = payload if status == "ok" else None
            snap_id = insert_snapshot(
                conn,
                company_id=row["id"],
                source="crbr",
                collected_at=date,
                status=status,
                normalized_payload=actual_payload,
                raw_path=f"dev_ms_data/snapshots/{date}/crbr/{json_path.stem}.xml" if status == "ok" else None,
            )
            crbr_count += 1
            print(f"  CRBR {date}: {json_path.name} [{status}] -> snapshot #{snap_id}")
    else:
        print(f"  SKIP: brak {crbr_dir}")

    conn.commit()
    conn.close()
    print(f"\nGotowe: {krs_count} KRS + {crbr_count} CRBR snapshots dla {date}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python import_today.py <date>")
        sys.exit(1)
    import_date(sys.argv[1])

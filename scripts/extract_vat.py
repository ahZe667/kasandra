"""
extract_vat.py — normalizuje surowe odpowiedzi Białej Listy VAT do normalized_payload.

Usage:
    python dev_ms_data/scripts/extract_vat.py <snapshots_vat_dir> <normalized_dir> [date]

Przykład:
    python dev_ms_data/scripts/extract_vat.py \
        dev_ms_data/snapshots/2026-04-28/vat \
        dev_ms_data/normalized/2026-04-28
"""

import json
import sys
from datetime import date as _date
from pathlib import Path


def normalize(raw: dict, query_date: str) -> dict:
    """Zwraca normalized_payload dla snapshotu VAT."""
    subject = raw.get("result", {}).get("subject", {})
    konta = sorted(subject.get("accountNumbers") or [])
    return {
        "company": {
            "nip": subject.get("nip"),
            "nazwa": subject.get("name"),
            "krs": subject.get("krs"),
            "regon": subject.get("regon"),
        },
        "vat": {
            "status": subject.get("statusVat"),
            "konta": konta,
        },
        "snapshot_meta": {
            "query_date": query_date,
        },
    }


def main(snap_vat_dir: Path, norm_dir: Path, query_date: str) -> None:
    out_dir = norm_dir / "vat"
    out_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(f for f in snap_vat_dir.glob("*.json") if not f.name.startswith("_"))
    if not files:
        print(f"SKIP: brak plikow w {snap_vat_dir}")
        return

    ok_count = skip_count = 0
    for json_path in files:
        with open(json_path, encoding="utf-8") as fp:
            raw = json.load(fp)

        # brak_wpisu lub error — zapisz stub bez kont i statusu
        subject = raw.get("result", {}).get("subject")
        if not subject:
            code = raw.get("code", "unknown")
            nip_from_name = json_path.stem.split("_")[0]
            stub = {
                "company": {"nip": nip_from_name, "nazwa": None, "krs": None, "regon": None},
                "vat": {"status": None, "konta": []},
                "snapshot_meta": {"query_date": query_date, "api_code": code},
            }
            out_file = out_dir / json_path.name
            out_file.write_text(json.dumps(stub, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  SKIP ({code}): {json_path.name}")
            skip_count += 1
            continue

        payload = normalize(raw, query_date)
        out_file = out_dir / json_path.name
        out_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        status = payload["vat"]["status"]
        konta_n = len(payload["vat"]["konta"])
        print(f"  OK: {json_path.name} | status={status} | konta={konta_n}")
        ok_count += 1

    print(f"\nOK: {ok_count} spolek -> {out_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_vat.py <snap_vat_dir> <norm_dir> [date]")
        sys.exit(1)
    snap_vat_dir = Path(sys.argv[1])
    norm_dir = Path(sys.argv[2])
    query_date = sys.argv[3] if len(sys.argv) > 3 else str(_date.today())
    main(snap_vat_dir, norm_dir, query_date)

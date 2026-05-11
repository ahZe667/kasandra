"""
extract_vat.py — normalizuje surowe odpowiedzi Białej Listy VAT do normalized_payload.

Usage:
    python dev_ms_data/scripts/extract_vat.py <snapshots_vat_dir> <normalized_dir>

Przykład:
    python dev_ms_data/scripts/extract_vat.py \
        dev_ms_data/snapshots/2026-04-28/vat \
        dev_ms_data/normalized/2026-04-28
"""
import json
import sys
from pathlib import Path


def normalize(raw: dict) -> dict:
    subject = raw.get("result", {}).get("subject", {})
    return {
        "company": {
            "nip": subject.get("nip"),
            "nazwa": subject.get("name"),
            "krs": subject.get("krs"),
            "regon": subject.get("regon"),
        },
        "vat": {
            "status": subject.get("statusVat"),
            "konta": sorted(subject.get("accountNumbers") or []),
        },
    }


def main(snap_vat_dir: Path, norm_dir: Path) -> None:
    out_dir = norm_dir / "vat"
    out_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(f for f in snap_vat_dir.glob("*.json") if not f.name.startswith("_"))
    if not files:
        print(f"SKIP: brak plikow w {snap_vat_dir}")
        return

    ok_count = skip_count = 0
    for json_path in files:
        raw = json.loads(json_path.read_text(encoding="utf-8"))
        subject = raw.get("result", {}).get("subject")

        if not subject:
            code = raw.get("code", "unknown")
            payload = {
                "company": {"nip": json_path.stem.split("_")[0], "nazwa": None, "krs": None, "regon": None},
                "vat": {"status": None, "konta": []},
            }
            print(f"  SKIP ({code}): {json_path.name}")
            skip_count += 1
        else:
            payload = normalize(raw)
            status = payload["vat"]["status"]
            konta_n = len(payload["vat"]["konta"])
            print(f"  OK: {json_path.name} | status={status} | konta={konta_n}")
            ok_count += 1

        (out_dir / json_path.name).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nOK: {ok_count} spolek -> {out_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_vat.py <snap_vat_dir> <norm_dir>")
        sys.exit(1)
    main(Path(sys.argv[1]), Path(sys.argv[2]))

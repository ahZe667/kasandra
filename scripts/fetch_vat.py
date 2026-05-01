"""
fetch_vat.py — pobiera dane z Białej Listy VAT (MF API) dla watchlisty.

API: GET https://wl-api.mf.gov.pl/api/search/nip/{NIP}?date=YYYY-MM-DD
Bez autoryzacji, odpowiedź JSON.

Usage:
    python dev_ms_data/scripts/fetch_vat.py <snapshots_dir> [date]

Przykład:
    python dev_ms_data/scripts/fetch_vat.py dev_ms_data/snapshots/2026-04-28
"""

import json
import sys
import time
import urllib.error
import urllib.request
from datetime import date as _date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from kasandra.storage.sqlite import connect, init_db, list_companies  # noqa: E402

API_BASE = "https://wl-api.mf.gov.pl/api/search/nip"
RATE_LIMIT = 1.0


def fetch_one(nip: str, query_date: str) -> tuple[str, dict]:
    """Pobiera dane VAT dla jednego NIP. Zwraca (status, raw_dict).

    Status: 'ok' | 'brak_wpisu' | 'error'
    """
    url = f"{API_BASE}/{nip}?date={query_date}"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        subject = data.get("result", {}).get("subject")
        if subject:
            return "ok", data
        return "brak_wpisu", data
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "brak_wpisu", {}
        return "error", {"error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return "error", {"error": str(e)}


def main(snap_dir: Path, query_date: str) -> None:
    out_dir = snap_dir / "vat"
    out_dir.mkdir(parents=True, exist_ok=True)

    db_path = REPO_ROOT / "var" / "sqlite" / "kasandra.sqlite3"
    conn = connect(db_path)
    init_db(conn)
    companies = list_companies(conn)
    conn.close()

    log: list[dict] = []
    ok_count = err_count = skip_count = 0

    for company in companies:
        nip = company["nip"]
        slug = company["slug"]

        if not nip:
            print(f"-> {slug} (brak NIP, pomijam)")
            skip_count += 1
            log.append({"slug": slug, "nip": None, "status": "skip_no_nip"})
            continue

        status, raw = fetch_one(nip, query_date)
        size = len(json.dumps(raw))
        marker = "OK" if status == "ok" else ("BRAK" if status == "brak_wpisu" else "ERR")
        print(f"-> {slug} ({nip})... {marker} {size} B")

        out_file = out_dir / f"{nip}_{slug}.json"
        out_file.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")

        log.append({"slug": slug, "nip": nip, "status": status, "size_b": size})
        if status == "ok":
            ok_count += 1
        else:
            err_count += 1

        time.sleep(RATE_LIMIT)

    log_file = out_dir / "_log.json"
    log_file.write_text(
        json.dumps({"date": query_date, "entries": log}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    total = ok_count + err_count + skip_count
    print(
        f"\nDone: {ok_count}/{total} OK, {err_count} blad/brak, {skip_count} pominieto -> {out_dir}"
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_vat.py <snapshots_dir> [date]")
        sys.exit(1)
    snap_dir = Path(sys.argv[1])
    query_date = sys.argv[2] if len(sys.argv) > 2 else str(_date.today())
    main(snap_dir, query_date)

"""
fetch_krs.py — pobieranie OdpisAktualny z KRS REST API dla watchlisty.

Endpoint: https://api-krs.ms.gov.pl/api/krs/OdpisAktualny/{krs}?rejestr=P&format=json
Nie wymaga autoryzacji. Limit: ~1 req/s żeby nie nadużywać.

Usage:
    python dev_ms_data/scripts/fetch_krs.py <output_dir>

Przykład:
    python dev_ms_data/scripts/fetch_krs.py dev_ms_data/snapshots/2026-04-23

Produkuje:
    <output_dir>/krs/{KRS}_{slug}.json   surowy odpis per spółka
    <output_dir>/krs/_log.json           log wszystkich prób
"""
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

WATCHLIST = [
    ("zabka",      "0000636642"),
    ("drutex",     "0000140428"),
    ("maspex",     "0000898248"),
    ("dino",       "0000408273"),
    ("asseco",     "0000033391"),
    ("fame_mma",   "0000883491"),
    ("mentzen",    "0001008036"),
    ("strong_man", "0000055656"),
    ("tenczynek",  "0000864032"),
    ("januszex",   "0000779880"),
]

BASE = "https://api-krs.ms.gov.pl/api/krs/OdpisAktualny"


def fetch_one(krs: str, timeout: int = 30) -> tuple[int, bytes]:
    url = f"{BASE}/{krs}?rejestr=P&format=json"
    req = urllib.request.Request(url, headers={"User-Agent": "kasandra-dev/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        try:
            return e.code, e.read()
        except Exception:
            return e.code, b""


def main():
    if len(sys.argv) != 2:
        print("Usage: python fetch_krs.py <output_dir>")
        sys.exit(1)

    out_dir = Path(sys.argv[1]) / "krs"
    out_dir.mkdir(parents=True, exist_ok=True)
    log = []

    for slug, krs in WATCHLIST:
        print(f"-> {slug} ({krs})...", end=" ", flush=True)
        status, raw = fetch_one(krs)
        ok = status == 200
        fname = f"{krs}_{slug}.json"

        if ok:
            (out_dir / fname).write_bytes(raw)
            bytes_written = len(raw)
            print(f"OK {bytes_written} B")
        else:
            bytes_written = 0
            print(f"ERR HTTP {status}: {raw[:200]}")

        log.append({
            "slug": slug,
            "krs": krs,
            "http_status": status,
            "ok": ok,
            "bytes": bytes_written,
            "file": fname if ok else None,
        })
        time.sleep(1)

    (out_dir / "_log.json").write_text(
        json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    ok_count = sum(1 for e in log if e["ok"])
    print(f"\nDone: {ok_count}/{len(log)} OK -> {out_dir}")


if __name__ == "__main__":
    main()

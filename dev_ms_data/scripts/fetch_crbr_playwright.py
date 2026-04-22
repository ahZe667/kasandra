"""
fetch_crbr_playwright.py — pobieranie XML z CRBR przez Playwright (headless Chrome).

Dlaczego Playwright a nie HTTP:
    SOAP bramka-crbr.mf.gov.pl zwraca HTTP 500 (backend niedostepny publicznie).
    REST /adcrbr/api/ blokowane przez Imperva WAF (silent block bez JS).
    Playwright uruchamia prawdziwy Chrome, przechodzi Imperva challenge, dziala.

Wyniki dla watchlisty Faza 0 (10 spolek):
    6 spolek ma wpisy w CRBR -> pobierany XML
    4 spolek nie ma wpisow:
      - Dino SA, Asseco SA  -> zwolnienie ustawowe (spolki notowane na GPW)
      - Strong Man, Januszex -> brak zgloszenia (naruszenie obowiazku lub inna przyczyna)

    Uwaga NIP Asseco: KRS API zwraca 5220003782, publicznie znany to 5220003307.
    Obie nieistotne dla CRBR — Asseco zwolnione jako spolka giełdowa.

Usage:
    python dev_ms_data/scripts/fetch_crbr_playwright.py <output_dir>

Produkuje:
    <output_dir>/crbr/{NIP}_{slug}.xml    (tylko dla spolek z wpisami)
    <output_dir>/crbr/_log.json           log wszystkich prób
"""
import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

WATCHLIST = [
    ("zabka",      "5223071241"),
    ("drutex",     "8421622720"),
    ("maspex",     "5512617657"),
    ("dino",       "6211766191"),
    ("asseco",     "5220003782"),
    ("fame_mma",   "7773370464"),
    ("mentzen",    "5273032556"),
    ("strong_man", "5862021333"),
    ("tenczynek",  "9462683417"),
    ("januszex",   "5272889007"),
]

BASE = "https://crbr.podatki.gov.pl"


def fetch_one(page, slug: str, nip: str, out_dir: Path) -> dict:
    entry = {"slug": slug, "nip": nip, "status": "error", "file": None, "bytes": 0, "error": None}
    try:
        page.goto(f"{BASE}/adcrbr/#/", wait_until="networkidle", timeout=30000)
        time.sleep(1)

        page.click('button:has-text("Wyszukaj")')
        page.wait_for_load_state("networkidle")
        time.sleep(1)

        nip_input = page.query_selector_all("input[type=text]")[0]
        nip_input.click()
        nip_input.fill(nip)
        time.sleep(0.3)

        page.query_selector_all('button:has-text("Wyszukaj")')[-1].click()
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        body = page.inner_text("body")

        if "Brak wpis" in body:
            entry["status"] = "brak_wpisow"
            return entry

        if "Pobierz plik XML" not in body:
            entry["error"] = f"nieznany stan strony: {body[:300]}"
            return entry

        dest = out_dir / f"{nip}_{slug}.xml"
        with page.expect_download(timeout=30000) as dl_info:
            page.click('button:has-text("Pobierz plik XML")')
        dl_info.value.save_as(str(dest))

        entry.update({"status": "ok", "file": dest.name, "bytes": dest.stat().st_size})

    except Exception as e:
        entry["error"] = str(e)

    return entry


def main():
    if len(sys.argv) != 2:
        print("Usage: python fetch_crbr_playwright.py <output_dir>")
        sys.exit(1)

    out_dir = Path(sys.argv[1]) / "crbr"
    out_dir.mkdir(parents=True, exist_ok=True)
    log = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for slug, nip in WATCHLIST:
            print(f"-> {slug} ({nip})...", end=" ", flush=True)
            entry = fetch_one(page, slug, nip, out_dir)
            log.append(entry)
            if entry["status"] == "ok":
                print(f"OK {entry['bytes']} B")
            elif entry["status"] == "brak_wpisow":
                print("brak wpisow w CRBR")
            else:
                print(f"ERR: {entry['error']}")
            time.sleep(2)

        browser.close()

    (out_dir / "_log.json").write_text(
        json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    ok = sum(1 for e in log if e["status"] == "ok")
    brak = sum(1 for e in log if e["status"] == "brak_wpisow")
    err = len(log) - ok - brak
    print(f"\nDone: {ok} XML, {brak} brak wpisow, {err} bledy -> {out_dir}")


if __name__ == "__main__":
    main()

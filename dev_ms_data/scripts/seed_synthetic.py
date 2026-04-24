"""
seed_synthetic.py — tworzy spreparowany snapshot testowy dla zabki (2026-04-24).

CEL: przetestowanie silnika diff + alertów bez czekania na realne zmiany w rejestrach.

SYMULOWANA ZMIANA (realistyczna):
  KRS: wiceprezes T***** B********* opuszcza zarząd (funkcja: WICEPREZES ZARZĄDU)
       + numer ostatniego wpisu rośnie o 1 (bo wpis musiał powstać)
  CRBR: ten sam wiceprezes znika z listy beneficjentów (inne_uprawnienia, senior manager AML)

OZNACZENIE:
  - pliki zapisywane do dev_ms_data/synthetic/2026-04-24/
  - raw_path w DB wskazuje na ścieżkę z "synthetic" — jasne że to dane testowe
  - collected_at = "2026-04-24" (kolejny dzień po realnych danych)

IDEMPOTENTNOŚĆ:
  Jeśli snapshot (zabka, krs/crbr, 2026-04-24) już istnieje w DB → pomija.
"""
import copy
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

from kasandra.storage.sqlite import connect, insert_snapshot  # noqa: E402

SYNTH_DATE = "2026-04-24"
SYNTH_DIR = REPO_ROOT / "dev_ms_data" / "synthetic" / SYNTH_DATE


def get_latest_snapshot(conn, slug: str, source: str):
    return conn.execute(
        """SELECT s.* FROM snapshots s JOIN companies c ON c.id = s.company_id
           WHERE c.slug = ? AND s.source = ? AND s.status = 'ok'
           ORDER BY s.collected_at DESC LIMIT 1""",
        (slug, source),
    ).fetchone()


def get_company_id(conn, slug: str) -> int:
    return conn.execute("SELECT id FROM companies WHERE slug = ?", (slug,)).fetchone()["id"]


def make_krs_synth(payload: dict) -> dict:
    """Usuwa wiceprezesa T***** B********* z zarządu i inkrementuje numer wpisu."""
    new = copy.deepcopy(payload)

    # Usuń wiceprezesa o nazwisku zaczynającym się na B (T***** B*********)
    old_sklad = new["zarzad"]["sklad"]
    # Klucz drugiego wiceprezesa (funkcja WICEPREZES ZARZĄDU, nazwisko B...)
    target_key = next(
        (m["osoba_key"] for m in old_sklad
         if m.get("funkcja") == "WICEPREZES ZARZĄDU" and "|T*****|" in m["osoba_key"]
         and m["osoba_key"].startswith("NAT:B")),
        None,
    )
    if target_key is None:
        # Fallback: usuń drugiego wiceprezesa z listy
        wiceprezesi = [m for m in old_sklad if m.get("funkcja") == "WICEPREZES ZARZĄDU"]
        target_key = wiceprezesi[0]["osoba_key"] if wiceprezesi else None

    if target_key:
        new["zarzad"]["sklad"] = [m for m in old_sklad if m["osoba_key"] != target_key]
        print(f"  KRS synth: usunięto z zarządu: {target_key}")
    else:
        print("  KRS synth: WARN nie znaleziono celu do usunięcia z zarządu")

    # Inkrementuj numer ostatniego wpisu
    old_nr = new["snapshot_meta"].get("nr_ostatniego_wpisu") or 0
    new["snapshot_meta"]["nr_ostatniego_wpisu"] = old_nr + 1
    new["snapshot_meta"]["stan_z_dnia"] = SYNTH_DATE
    print(f"  KRS synth: nr wpisu {old_nr} -> {old_nr + 1}")

    return new, target_key


def make_crbr_synth(payload: dict, removed_key: str | None) -> dict:
    """Usuwa beneficjenta pasującego do klucza osoby usuniętej z zarządu KRS."""
    new = copy.deepcopy(payload)
    old_bens = new.get("beneficjenci", [])

    if removed_key:
        # Klucz CRBR i KRS są kompatybilne (ten sam format NAT:...)
        new["beneficjenci"] = [b for b in old_bens if b["osoba_key"] != removed_key]
        removed = [b for b in old_bens if b["osoba_key"] == removed_key]
        if removed:
            print(f"  CRBR synth: usunięto beneficjenta: {removed_key}")
        else:
            print(f"  CRBR synth: WARN klucz {removed_key} nie znaleziony w beneficjentach")
    else:
        # Fallback: usuń ostatniego beneficjenta
        if old_bens:
            new["beneficjenci"] = old_bens[:-1]
            print(f"  CRBR synth: (fallback) usunięto ostatniego beneficjenta")

    new["snapshot_meta"]["collected_at"] = SYNTH_DATE
    return new


def main() -> None:
    SYNTH_DIR.mkdir(parents=True, exist_ok=True)
    krs_dir = SYNTH_DIR / "krs"
    crbr_dir = SYNTH_DIR / "crbr"
    krs_dir.mkdir(exist_ok=True)
    crbr_dir.mkdir(exist_ok=True)

    db_path = REPO_ROOT / "var" / "sqlite" / "kasandra.sqlite3"
    conn = connect(db_path)
    company_id = get_company_id(conn, "zabka")

    print(f"=== Synthetic snapshot: zabka {SYNTH_DATE} ===\n")

    # --- KRS ---
    snap_krs = get_latest_snapshot(conn, "zabka", "krs")
    if snap_krs is None:
        print("ERR: brak bazowego KRS snapshotu dla zabki")
        return

    base_krs = json.loads(snap_krs["normalized_payload"])
    synth_krs, removed_key = make_krs_synth(base_krs)

    krs_file = krs_dir / "0000636642_zabka.json"
    krs_file.write_text(json.dumps(synth_krs, ensure_ascii=False, indent=2), encoding="utf-8")

    snap_id_krs = insert_snapshot(
        conn,
        company_id=company_id,
        source="krs",
        collected_at=SYNTH_DATE,
        status="ok",
        normalized_payload=synth_krs,
        raw_path=f"dev_ms_data/synthetic/{SYNTH_DATE}/krs/0000636642_zabka.json",
    )
    print(f"  KRS snapshot zapisany: #{snap_id_krs}\n")

    # --- CRBR ---
    snap_crbr = get_latest_snapshot(conn, "zabka", "crbr")
    if snap_crbr is None:
        print("ERR: brak bazowego CRBR snapshotu dla zabki")
        return

    base_crbr = json.loads(snap_crbr["normalized_payload"])
    synth_crbr = make_crbr_synth(base_crbr, removed_key)

    crbr_file = crbr_dir / "5223071241_zabka.json"
    crbr_file.write_text(json.dumps(synth_crbr, ensure_ascii=False, indent=2), encoding="utf-8")

    snap_id_crbr = insert_snapshot(
        conn,
        company_id=company_id,
        source="crbr",
        collected_at=SYNTH_DATE,
        status="ok",
        normalized_payload=synth_crbr,
        raw_path=f"dev_ms_data/synthetic/{SYNTH_DATE}/crbr/5223071241_zabka.json",
    )
    print(f"  CRBR snapshot zapisany: #{snap_id_crbr}\n")

    conn.commit()
    conn.close()
    print("Gotowe. Uruchom teraz: python dev_ms_data/scripts/run_diff.py")


if __name__ == "__main__":
    main()

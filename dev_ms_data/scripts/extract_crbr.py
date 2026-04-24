"""
extract_crbr.py — wyciaga normalized_payload ze snapshotow CRBR.

UWAGA: CRBR zawiera pelne numery PESEL. Skrypt maskuje je przed zapisem
w taki sam sposob jak KRS API (pierwszy znak + gwiazdki do dlugosci oryginalu).

Typy charakterUdzialu:
  1 — bezposrednia wlasnosc (ilosc + jednostka + rodzajWlasnosci)
  2 — posrednia wlasnosc / inne uprawnienia posrednie (uprWlasPosrednie)
  3 — inne uprawnienia (senior manager AML, inneUprBO)

Usage:
    python extract_crbr.py <snapshots_dir> <output_dir>

Przyklad:
    python dev_ms_data/scripts/extract_crbr.py \\
        dev_ms_data/snapshots/2026-04-22/crbr \\
        dev_ms_data/normalized/2026-04-22

Produkuje:
    <output_dir>/crbr/{nip}_{slug}.json   per spolka — normalized JSON
    <output_dir>/crbr_dataset.json        zbiorczy (lista) — kanoniczny dla diffu
    <output_dir>/crbr_dataset.md          czytelny markdown dla recznego przegladu
"""
import json
import sys
from pathlib import Path
from xml.etree import ElementTree as ET


CHARAKTER_OPIS = {
    "1": "bezposrednia_wlasnosc",
    "2": "posrednia_wlasnosc",
    "3": "inne_uprawnienia",
}


def mask(s):
    """Maskuje string jak KRS API: pierwszy znak + gwiazdki. None -> '?'."""
    if not s:
        return "?"
    return s[0] + "*" * (len(s) - 1)


def txt(el, tag):
    """Zwraca text dziecka el o podanym tagu lub None."""
    child = el.find(tag)
    return child.text.strip() if child is not None and child.text else None


def osoba_key_crbr(nazwisko, imie, pesel):
    return f"NAT:{mask(nazwisko)}|{mask(imie)}|{mask(pesel)}"


def osoba_display_crbr(nazwisko, imie):
    return f"{mask(imie)} {mask(nazwisko)}"


def parse_beneficjent(b_el):
    imie = txt(b_el, "imiePierwsze")
    nazwisko = txt(b_el, "nazwisko")
    pesel = txt(b_el, "pesel")

    obyw_el = b_el.find("obywatelstwo")
    obywatelstwo = txt(obyw_el, "kodKraju") if obyw_el is not None else None

    panstwo_el = b_el.find("panstwoZamieszkania")
    panstwo_zamieszkania = txt(panstwo_el, "kodKraju") if panstwo_el is not None else None

    info_el = b_el.find("informacjeOUdzialeLubUprawnieniach")
    charakter_kod = txt(info_el, "charakterUdzialu") if info_el is not None else None
    charakter_opis = CHARAKTER_OPIS.get(charakter_kod or "", "nieznany")

    udzial_ilosc = None
    udzial_jednostka_opis = None
    rodzaj_wlasnosci_opis = None
    posrednie_opis = None
    inne_uprbo_opis = None

    if info_el is not None:
        if charakter_kod == "1":
            udzial_ilosc = txt(info_el, "ilosc")
            udzial_jednostka_opis = txt(info_el, "jednostkaMiaryUdzialuOpis")
            rodzaj_wlasnosci_opis = txt(info_el, "rodzajWlasnosciOpis")
        elif charakter_kod == "2":
            posrednie_opis = txt(info_el, "uprWlasPosrednie")
        elif charakter_kod == "3":
            inne_el = info_el.find("inneUprBO/rodzajInnychUprawnien")
            if inne_el is not None:
                inne_uprbo_opis = txt(inne_el, "opis")

    return {
        "osoba_key": osoba_key_crbr(nazwisko, imie, pesel),
        "display": osoba_display_crbr(nazwisko, imie),
        "obywatelstwo": obywatelstwo,
        "panstwo_zamieszkania": panstwo_zamieszkania,
        "charakter_udzialu_kod": charakter_kod,
        "charakter_udzialu_opis": charakter_opis,
        "udzial_ilosc": udzial_ilosc,
        "udzial_jednostka_opis": udzial_jednostka_opis,
        "rodzaj_wlasnosci_opis": rodzaj_wlasnosci_opis,
        "posrednie_opis": posrednie_opis,
        "inne_uprbo_opis": inne_uprbo_opis,
    }


def normalize_xml(xml_path, slug):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    params_el = root.find("parametryWyszukiwania")
    collected_at = txt(params_el, "dataDo") if params_el is not None else None
    nip = txt(params_el, "nipLubIdentyfikatortrustu") if params_el is not None else None

    zgl_el = root.find("zgloszeniePodmiotu")
    if zgl_el is None:
        return None

    zgloszenie_id = txt(zgl_el, "id")
    korekta_raw = txt(zgl_el, "korekta")
    korekta = korekta_raw == "true" if korekta_raw else False
    data_poczatku = txt(zgl_el, "dataPoczatkuPrezentacji")
    data_konca = txt(zgl_el, "dataKoncaPrezentacji")

    dane_el = zgl_el.find("danePodmiotu")
    company = {}
    if dane_el is not None:
        adres_el = dane_el.find("adresSiedziby")
        adres = {}
        if adres_el is not None:
            adres = {
                "ulica": txt(adres_el, "ulica"),
                "nr_domu": txt(adres_el, "nrDomu"),
                "nr_lokalu": txt(adres_el, "nrLokalu"),
                "kod_pocztowy": txt(adres_el, "kodPocztowy"),
                "miejscowosc": txt(adres_el, "miejscowosc"),
                "wojewodztwo": txt(adres_el, "wojewodztwo"),
            }
        company = {
            "krs": txt(dane_el, "krs"),
            "nip": txt(dane_el, "nipLubIdentyfikatortrustu"),
            "nazwa": txt(dane_el, "pelnaNazwa"),
            "forma": txt(dane_el, "formaOrganizacyjnaOpis"),
            "adres": adres,
        }

    beneficjenci = [parse_beneficjent(b) for b in zgl_el.findall("beneficjent")]

    return {
        "source": "crbr",
        "slug": slug,
        "status": "ok",
        "snapshot_meta": {
            "collected_at": collected_at,
            "zgloszenie_id": zgloszenie_id,
            "korekta": korekta,
            "data_poczatku_prezentacji": data_poczatku,
            "data_konca_prezentacji": data_konca,
        },
        "company": company,
        "beneficjenci": beneficjenci,
    }


def normalize_brak(log_entry):
    return {
        "source": "crbr",
        "slug": log_entry["slug"],
        "status": "brak_wpisow",
        "snapshot_meta": {
            "collected_at": None,
            "zgloszenie_id": None,
            "korekta": False,
            "data_poczatku_prezentacji": None,
            "data_konca_prezentacji": None,
        },
        "company": {
            "krs": None,
            "nip": log_entry["nip"],
            "nazwa": None,
            "forma": None,
            "adres": {},
        },
        "beneficjenci": [],
    }


def render_md(dataset):
    lines = ["# CRBR — dataset znormalizowany (v0.1)", ""]
    lines.append("Wygenerowane przez `dev_ms_data/scripts/extract_crbr.py`.")
    lines.append("PESELe zamaskowane: pierwszy znak + gwiazdki.")
    lines.append("")
    lines.append("---")
    lines.append("")

    for entry in dataset:
        c = entry["company"]
        m = entry["snapshot_meta"]
        status = entry["status"]
        beneficjenci = entry["beneficjenci"]

        lines.append(f"## {c.get('nazwa') or entry['slug'].upper()}")
        lines.append("")
        lines.append(f"- **Status CRBR:** `{status}`")
        lines.append(f"- **NIP:** `{c.get('nip')}`  **KRS:** `{c.get('krs')}`")
        lines.append(f"- **Forma:** {c.get('forma')}")

        if status == "ok":
            a = c.get("adres", {})
            lokal = f"/{a['nr_lokalu']}" if a.get("nr_lokalu") else ""
            adres_str = f"{a.get('ulica') or ''} {a.get('nr_domu') or ''}{lokal}, {a.get('kod_pocztowy') or ''} {a.get('miejscowosc') or ''}"
            lines.append(f"- **Adres:** {adres_str.strip()}")
            korekta_flag = " ⚠ KOREKTA" if m.get("korekta") else ""
            lines.append(f"- **Zgłoszenie:** `{m['zgloszenie_id']}`{korekta_flag}, ważne {m['data_poczatku_prezentacji']} – {m['data_konca_prezentacji']}")
            lines.append(f"- **Pobrano:** {m['collected_at']}")
            lines.append("")
            lines.append(f"**Beneficjenci ({len(beneficjenci)}):**")
            lines.append("")
            for b in beneficjenci:
                charakter = f"`{b['charakter_udzialu_opis']}`"
                if b["charakter_udzialu_kod"] == "1":
                    szczegol = f"{b['udzial_ilosc']} {b['udzial_jednostka_opis']} — {b['rodzaj_wlasnosci_opis']}"
                elif b["charakter_udzialu_kod"] == "2":
                    szczegol = b.get("posrednie_opis") or "—"
                else:
                    szczegol = b.get("inne_uprbo_opis") or "—"
                lines.append(f"- `{b['osoba_key']}` ({b['obywatelstwo']}/{b['panstwo_zamieszkania']})")
                lines.append(f"  - {charakter}: {szczegol}")
        else:
            lines.append("")
            lines.append("_Brak wpisów w CRBR._")

        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) != 3:
        print("Usage: python extract_crbr.py <snapshots_dir> <output_dir>")
        sys.exit(1)

    snap_dir = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    crbr_out = out_dir / "crbr"
    crbr_out.mkdir(parents=True, exist_ok=True)

    log_path = snap_dir / "_log.json"
    log_entries = {}
    if log_path.exists():
        with open(log_path, encoding="utf-8") as fp:
            for entry in json.load(fp):
                log_entries[entry["slug"]] = entry

    dataset = []

    for xml_path in sorted(snap_dir.glob("*.xml")):
        slug = xml_path.stem.split("_", 1)[1] if "_" in xml_path.stem else xml_path.stem
        normalized = normalize_xml(xml_path, slug)
        if normalized is None:
            print(f"WARN: brak zgloszeniaPodmiotu w {xml_path.name}")
            continue
        dataset.append(normalized)
        out_name = xml_path.stem + ".json"
        with open(crbr_out / out_name, "w", encoding="utf-8") as fp:
            json.dump(normalized, fp, ensure_ascii=False, indent=2)
        print(f"OK: {xml_path.name} -> {out_name} ({len(normalized['beneficjenci'])} beneficjentow)")

    for slug, entry in log_entries.items():
        if entry["status"] == "brak_wpisow":
            normalized = normalize_brak(entry)
            dataset.append(normalized)
            out_name = f"{entry['nip']}_{slug}.json"
            with open(crbr_out / out_name, "w", encoding="utf-8") as fp:
                json.dump(normalized, fp, ensure_ascii=False, indent=2)
            print(f"BRAK: {slug} ({entry['nip']}) -> {out_name}")

    dataset.sort(key=lambda e: e["company"].get("nip") or "")

    with open(out_dir / "crbr_dataset.json", "w", encoding="utf-8") as fp:
        json.dump(dataset, fp, ensure_ascii=False, indent=2)

    md = render_md(dataset)
    with open(out_dir / "crbr_dataset.md", "w", encoding="utf-8") as fp:
        fp.write(md)

    ok = sum(1 for e in dataset if e["status"] == "ok")
    brak = sum(1 for e in dataset if e["status"] == "brak_wpisow")
    print(f"\nRazem: {len(dataset)} spolek — {ok} OK, {brak} brak wpisow -> {out_dir}")


if __name__ == "__main__":
    main()

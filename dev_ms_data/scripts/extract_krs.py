"""
extract_krs.py — wyciaga normalized_payload ze snapshotow KRS.

Wzor pol: dev_ms.md sekcja "Wzor wyciaganych danych — KRS normalized_payload (v0.1)".

Usage:
    python extract_krs.py <snapshots_dir> <output_dir>

Przyklad:
    python dev_ms_data/scripts/extract_krs.py \
        dev_ms_data/snapshots/2026-04-20/krs \
        dev_ms_data/normalized/2026-04-20

Produkuje:
    <output_dir>/krs/{filename}.json   per spolka — normalized JSON
    <output_dir>/dataset.json          zbiorczy plik (lista) — kanoniczny dla diffu
    <output_dir>/dataset.md            czytelny markdown dla recznego przegladu
"""
import json
import sys
from pathlib import Path


def safe(d, *keys):
    cur = d
    for k in keys:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
        if cur is None:
            return None
    return cur


def osoba_key(o):
    """Stabilny klucz osoby. Maski sa deterministyczne, wiec tasama osoba = ten sam klucz."""
    if 'nazwa' in o:
        ident = safe(o, 'krs', 'krs') or safe(o, 'identyfikator', 'regon') or '?'
        return f"LE:{o['nazwa']}|{ident}"
    nazw = safe(o, 'nazwisko', 'nazwiskoICzlon') or '?'
    imie = safe(o, 'imiona', 'imie') or '?'
    pesel = safe(o, 'identyfikator', 'pesel') or '?'
    return f"NAT:{nazw}|{imie}|{pesel}"


def osoba_display(o):
    if 'nazwa' in o:
        return o['nazwa']
    nazw = safe(o, 'nazwisko', 'nazwiskoICzlon') or '?'
    imie = safe(o, 'imiona', 'imie') or '?'
    imie2 = safe(o, 'imiona', 'imieDrugie') or ''
    parts = [imie, imie2, nazw]
    return ' '.join(p for p in parts if p)


def osoba_typ(o):
    return 'prawna' if 'nazwa' in o else 'fizyczna'


def normalize_zarzad_member(o):
    return {
        "osoba_key": osoba_key(o),
        "typ": osoba_typ(o),
        "display": osoba_display(o),
        "funkcja": o.get('funkcjaWOrganie'),
    }


def normalize_wlasciciel(o, calosc_field):
    return {
        "osoba_key": osoba_key(o),
        "typ": osoba_typ(o),
        "display": osoba_display(o),
        "posiadane_udzialy": o.get('posiadaneUdzialy'),
        "calosc": o.get(calosc_field),
    }


def normalize(raw):
    odpis = raw['odpis']
    naglowek = odpis['naglowekA']
    dane = odpis['dane']
    dz1 = dane.get('dzial1') or {}
    dz2 = dane.get('dzial2') or {}
    dz3 = dane.get('dzial3') or {}
    dz4 = dane.get('dzial4') or {}
    dz5 = dane.get('dzial5') or {}
    dz6 = dane.get('dzial6') or {}

    dane_pod = dz1.get('danePodmiotu') or {}
    iden = dane_pod.get('identyfikatory') or {}
    adres = safe(dz1, 'siedzibaIAdres', 'adres') or {}
    kapital = safe(dz1, 'kapital', 'wysokoscKapitaluZakladowego') or {}

    repr_ = dz2.get('reprezentacja') or {}
    sklad = repr_.get('sklad') or []

    if dz1.get('wspolnicySpzoo'):
        wlasc_typ = 'wspolnicy_spzoo'
        wlasc_lista = [normalize_wlasciciel(w, 'czyPosiadaCaloscUdzialow') for w in dz1['wspolnicySpzoo']]
    elif dz1.get('jedynyAkcjonariusz'):
        wlasc_typ = 'jedyny_akcjonariusz'
        wlasc_lista = [normalize_wlasciciel(w, 'czyPosiadaCaloscAkcji') for w in dz1['jedynyAkcjonariusz']]
    else:
        wlasc_typ = 'brak_w_krs'
        wlasc_lista = []

    pkd_lista = safe(dz3, 'przedmiotDzialalnosci', 'przedmiotPrzewazajacejDzialalnosci') or []
    pkd_main = pkd_lista[0] if pkd_lista else {}
    pkd_kod_parts = [pkd_main.get('kodDzial'), pkd_main.get('kodKlasa'), pkd_main.get('kodPodklasa')]
    pkd_kod = '.'.join(p for p in pkd_kod_parts if p)

    return {
        "company": {
            "krs": naglowek.get('numerKRS'),
            "nazwa": dane_pod.get('nazwa'),
            "forma": dane_pod.get('formaPrawna'),
            "nip": iden.get('nip'),
            "regon": iden.get('regon'),
        },
        "snapshot_meta": {
            "stan_z_dnia": naglowek.get('stanZDnia'),
            "nr_ostatniego_wpisu": naglowek.get('numerOstatniegoWpisu'),
            "data_ostatniego_wpisu": naglowek.get('dataOstatniegoWpisu'),
        },
        "adres": {
            "ulica": adres.get('ulica'),
            "nr_domu": adres.get('nrDomu'),
            "nr_lokalu": adres.get('nrLokalu'),
            "kod_pocztowy": adres.get('kodPocztowy'),
            "miejscowosc": adres.get('miejscowosc'),
            "kraj": adres.get('kraj'),
        },
        "kapital": {
            "wartosc": kapital.get('wartosc'),
            "waluta": kapital.get('waluta'),
        },
        "zarzad": {
            "nazwa_organu": repr_.get('nazwaOrganu'),
            "sposob_reprezentacji": repr_.get('sposobReprezentacji'),
            "sklad": [normalize_zarzad_member(o) for o in sklad],
        },
        "wlasciciele": {
            "typ": wlasc_typ,
            "lista": wlasc_lista,
        },
        "pkd_glowny": {
            "kod": pkd_kod,
            "opis": pkd_main.get('opis'),
        },
        "distress": {
            "dzial4": bool(dz4),
            "dzial5": bool(dz5),
            "dzial6": bool(dz6),
            "dzial6_typy": list(dz6.keys()) if dz6 else [],
        },
    }


def render_md(dataset):
    lines = ["# KRS — dataset znormalizowany (v0.1)", ""]
    lines.append("Wygenerowane przez `dev_ms_data/scripts/extract_krs.py`.")
    lines.append("Schemat pol: `dev_ms.md` sekcja \"Wzor wyciaganych danych\".")
    lines.append("")
    lines.append("---")
    lines.append("")

    for entry in dataset:
        c = entry['company']
        m = entry['snapshot_meta']
        a = entry['adres']
        k = entry['kapital']
        z = entry['zarzad']
        w = entry['wlasciciele']
        p = entry['pkd_glowny']
        d = entry['distress']

        lokal = f"/{a['nr_lokalu']}" if a.get('nr_lokalu') else ""
        adres_str = f"{a.get('ulica') or ''} {a.get('nr_domu') or ''}{lokal}, {a.get('kod_pocztowy') or ''} {a.get('miejscowosc') or ''}, {a.get('kraj') or ''}".strip()

        lines.append(f"## {c['nazwa']}")
        lines.append("")
        lines.append(f"- **KRS / NIP / REGON:** `{c['krs']}` / `{c['nip']}` / `{c['regon']}`")
        lines.append(f"- **Forma:** {c['forma']}")
        lines.append(f"- **Adres:** {adres_str}")
        lines.append(f"- **Kapital:** {k.get('wartosc')} {k.get('waluta')}")
        lines.append(f"- **PKD glowny:** `{p['kod']}` — {p['opis']}")
        lines.append(f"- **Stan na dzien:** {m['stan_z_dnia']} (wpis #{m['nr_ostatniego_wpisu']} z {m['data_ostatniego_wpisu']})")
        lines.append("")
        lines.append(f"**Zarzad** — organ: `{z['nazwa_organu']}`, osob: {len(z['sklad'])}, reprezentacja: _{z['sposob_reprezentacji']}_")
        lines.append("")
        for member in z['sklad']:
            lines.append(f"- `{member['osoba_key']}`")
            lines.append(f"  - {member['display']} — {member['funkcja']} ({member['typ']})")
        lines.append("")

        lines.append(f"**Wlasciciele** — typ: `{w['typ']}`, pozycji: {len(w['lista'])}")
        lines.append("")
        if not w['lista']:
            lines.append("- _brak danych w KRS (typowe dla SA bez jedynego akcjonariusza — dane w ksiedze akcyjnej)_")
        for wl in w['lista']:
            calosc = " — **100%**" if wl.get('calosc') else ""
            udz = wl.get('posiadane_udzialy') or '—'
            lines.append(f"- `{wl['osoba_key']}`")
            lines.append(f"  - {wl['display']}{calosc} ({wl['typ']})")
            lines.append(f"  - udzialy: {udz}")
        lines.append("")

        flags = f"dz4={d['dzial4']} | dz5={d['dzial5']} | dz6={d['dzial6']}"
        lines.append(f"**Distress flags:** {flags}")
        if d['dzial6_typy']:
            lines.append(f"- dz6 typy: `{', '.join(d['dzial6_typy'])}`")
        lines.append("")
        lines.append("---")
        lines.append("")

    return '\n'.join(lines)


def main():
    if len(sys.argv) != 3:
        print("Usage: python extract_krs.py <snapshots_dir> <output_dir>")
        sys.exit(1)

    snap_dir = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    krs_out = out_dir / 'krs'
    krs_out.mkdir(parents=True, exist_ok=True)

    dataset = []
    files = sorted(f for f in snap_dir.glob('*.json') if not f.name.startswith('_'))
    for f in files:
        with open(f, encoding='utf-8') as fp:
            raw = json.load(fp)
        normalized = normalize(raw)
        dataset.append(normalized)
        with open(krs_out / f.name, 'w', encoding='utf-8') as fp:
            json.dump(normalized, fp, ensure_ascii=False, indent=2)

    with open(out_dir / 'dataset.json', 'w', encoding='utf-8') as fp:
        json.dump(dataset, fp, ensure_ascii=False, indent=2)

    md = render_md(dataset)
    with open(out_dir / 'dataset.md', 'w', encoding='utf-8') as fp:
        fp.write(md)

    print(f"OK: {len(dataset)} spolek -> {out_dir}")


if __name__ == '__main__':
    main()

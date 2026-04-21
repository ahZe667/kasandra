"""
fetch_crbr.py - probka pobrania danych z CRBR przez publiczne SOAP API MF.

Endpoint (SOAP 1.2, bez autoryzacji):
    https://bramka-crbr.mf.gov.pl:5058/uslugiBiznesowe/uslugiESB/AP/ApiPrzegladoweCRBR/2022/02/01

Spec: ApiPrzegladoweCRBR_Specyfikacja_We-Wy 2.0.0 (MF, 2020-11-10)
Operacja: PobierzInformacjeOSpolkachIBeneficjentach (po NIP)

Status (2026-04-21):
    Bramka przyjmuje envelope zgodny ze spec, ale konsekwentnie zwraca
    HTTP 500 + SOAP Fault env:Receiver "Internal Error (from server)"
    - nawet dla przykladowego NIP ze specyfikacji (1120149662).
    Probowano: SOAP 1.2 z action w Content-Type, SOAP 1.1 z SOAPAction,
    WS-Addressing, oba endpointy (2020/05/01 i 2022/02/01), rozne NIPy.
    Wszystkie wariacje -> env:Receiver 500.
    Wniosek: backend bramki nie dziala publicznie badz wymaga czegos
    nieudokumentowanego (IP whitelist / rejestracja). Patrz dev_ms.md.

Usage:
    python dev_ms_data/scripts/fetch_crbr.py <output_dir>

Produkuje (nawet jesli blad):
    <output_dir>/crbr/{NIP}.xml           surowy response (fault lub dane)
    <output_dir>/crbr/_log.json           podsumowanie kazdej proby
"""
import json
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ENDPOINT = "https://bramka-crbr.mf.gov.pl:5058/uslugiBiznesowe/uslugiESB/AP/ApiPrzegladoweCRBR/2022/02/01"
NS_OP = "http://www.mf.gov.pl/uslugiBiznesowe/uslugiESB/AP/ApiPrzegladoweCRBR/2022/02/01"
NS_SCHEMA = "http://www.mf.gov.pl/schematy/AP/ApiPrzegladoweCRBR/2022/02/01"

# Watchlista Faza 0 — NIP wyciagniete z KRS snapshots (2026-04-20).
WATCHLIST = [
    ("zabka", "5223071241"),
    ("drutex", "8421622720"),
    ("maspex", "5512617657"),
    ("dino", "6211766191"),
    ("asseco", "5220003782"),
    ("fame_mma", "7773370464"),
    ("mentzen", "5273032556"),
    ("strong_man", "5862021333"),
    ("tenczynek", "9462683417"),
    ("januszex", "5272889007"),
]


def build_envelope(nip: str) -> str:
    return (
        f'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" '
        f'xmlns:ns="{NS_OP}" xmlns:ns1="{NS_SCHEMA}">'
        f"<soap:Header/>"
        f"<soap:Body>"
        f"<ns:PobierzInformacjeOSpolkachIBeneficjentach>"
        f"<PobierzInformacjeOSpolkachIBeneficjentachDane>"
        f"<ns1:SzczegolyWniosku><ns1:NIP>{nip}</ns1:NIP></ns1:SzczegolyWniosku>"
        f"</PobierzInformacjeOSpolkachIBeneficjentachDane>"
        f"</ns:PobierzInformacjeOSpolkachIBeneficjentach>"
        f"</soap:Body></soap:Envelope>"
    )


def call_crbr(nip: str, timeout: int = 30) -> tuple[int, bytes]:
    body = build_envelope(nip).encode("utf-8")
    headers = {
        "Content-Type": (
            'application/soap+xml; charset=utf-8; '
            'action="PobierzInformacjeOSpolkachIBeneficjentach"'
        ),
        "User-Agent": "kasandra-dev/0.1",
    }
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(ENDPOINT, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        try:
            return e.code, e.read()
        except Exception:
            return e.code, b""


def main():
    if len(sys.argv) != 2:
        print("Usage: python fetch_crbr.py <output_dir>")
        sys.exit(1)

    out_dir = Path(sys.argv[1]) / "crbr"
    out_dir.mkdir(parents=True, exist_ok=True)
    log = []

    for slug, nip in WATCHLIST:
        print(f"-> {slug} ({nip})...", end=" ", flush=True)
        status, raw = call_crbr(nip)
        fname = f"{nip}_{slug}.xml"
        (out_dir / fname).write_bytes(raw)
        is_fault = b"<env:Fault" in raw or b"<soap:Fault" in raw or b"<Fault" in raw
        entry = {
            "slug": slug,
            "nip": nip,
            "http_status": status,
            "bytes": len(raw),
            "fault": is_fault,
            "file": fname,
        }
        log.append(entry)
        print(f"HTTP {status}, {len(raw)} B, fault={is_fault}")
        time.sleep(1)  # rate limit — bramka jest publiczna ale nie przesadzajmy

    (out_dir / "_log.json").write_text(
        json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nDone: {len(log)} requests -> {out_dir}")


if __name__ == "__main__":
    main()

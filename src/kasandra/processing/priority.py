"""Priority and title mappings for alert rules."""

from __future__ import annotations

PRIORITY: dict[str, str] = {
    "A-WPIS-NR": "N",
    "A-ZARZAD-PREZES": "W",
    "A-ZARZAD-SKLAD": "S",
    "A-ADRES": "N",
    "A-KAPITAL": "S",
    "A-CRBR-BRAK": "W",
    "A-CRBR-BEN-NOWY": "W",
    "A-CRBR-BEN-USUN": "W",
    "A-CRBR-BEN-NOWY-WPIS": "W",
    "A-CRBR-BEN-ZNIKNAL-WPIS": "W",
    "A-CRBR-BEN-SKLAD": "W",  # legacy
}

TITLE: dict[str, str] = {
    "A-WPIS-NR": "Nowy wpis w KRS",
    "A-ZARZAD-PREZES": "Zmiana prezesa zarządu",
    "A-ZARZAD-SKLAD": "Zmiana składu zarządu",
    "A-ADRES": "Zmiana adresu siedziby",
    "A-KAPITAL": "Zmiana kapitału zakładowego",
    "A-CRBR-BRAK": "Brak zgłoszenia w CRBR",
    "A-CRBR-BEN-NOWY": "Nowy beneficjent rzeczywisty",
    "A-CRBR-BEN-USUN": "Usunięty beneficjent rzeczywisty",
    "A-CRBR-BEN-NOWY-WPIS": "Pojawił się wpis w CRBR",
    "A-CRBR-BEN-ZNIKNAL-WPIS": "Zniknął wpis z CRBR",
    "A-CRBR-BEN-SKLAD": "Zmiana składu beneficjentów CRBR",  # legacy
}

NEXT_STEP: dict[str, str] = {
    "A-ZARZAD-PREZES": "Sprawdzić wpływ na reprezentację spółki i uprawnienia do podpisu.",
    "A-ZARZAD-SKLAD": "Sprawdzić, czy zmiana wpływa na reprezentację spółki.",
    "A-ADRES": "Zapisać zmianę w historii, brak eskalacji.",
    "A-KAPITAL": "Sprawdzić przyczyny zmiany kapitału.",
    "A-CRBR-BRAK": "Zweryfikować, czy spółka powinna być w CRBR (sp. z o.o. lub SA niebędąca na GPW).",
    "A-CRBR-BEN-NOWY": "Zapisać zmianę i porównać z kolejnym snapshotem KRS.",
    "A-CRBR-BEN-USUN": "Zapisać zmianę i porównać z kolejnym snapshotem KRS.",
    "A-CRBR-BEN-NOWY-WPIS": "Nowy wpis w CRBR — zidentyfikować beneficjentów.",
    "A-CRBR-BEN-ZNIKNAL-WPIS": "Wpis zniknął z CRBR — sprawdzić przyczynę.",
    "A-CRBR-BEN-SKLAD": "Zweryfikować zmianę beneficjentów i porównać z KRS.",
}

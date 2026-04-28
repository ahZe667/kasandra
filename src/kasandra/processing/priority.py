"""Priority and title mappings for alert rules."""

from __future__ import annotations

PRIORITY: dict[str, str] = {
    # distress — najwyzszy priorytet
    "A-DZ6-NEW": "K",
    "A-DZ4-NEW": "K",
    "A-DZ5-NEW": "W",
    # zmiany wlascicielskie
    "A-WLASC-NOWY": "W",
    "A-WLASC-USUN": "W",
    # zmiany zarzadu
    "A-ZARZAD-PREZES": "W",
    "A-ZARZAD-SKLAD": "S",
    "A-ZARZAD-REPR": "S",
    # zmiany strukturalne
    "A-FORMA": "W",
    "A-KAPITAL": "S",
    "A-NAZWA": "S",
    "A-PKD": "S",
    # VAT
    "A-VAT-STATUS": "W",
    "A-VAT-KONTO-USUN": "W",
    "A-VAT-KONTO-NOWE": "S",
    # dane kontekstowe
    "A-ADRES": "N",
    "A-WPIS-NR": "N",
    # CRBR (zawieszone — pozostawione dla historycznych danych)
    "A-CRBR-BRAK": "W",
    "A-CRBR-BEN-NOWY": "W",
    "A-CRBR-BEN-USUN": "W",
    "A-CRBR-BEN-NOWY-WPIS": "W",
    "A-CRBR-BEN-ZNIKNAL-WPIS": "W",
    "A-CRBR-BEN-SKLAD": "W",  # legacy
}

TITLE: dict[str, str] = {
    "A-DZ6-NEW": "Postepowanie upadlosciowe / restrukturyzacyjne",
    "A-DZ4-NEW": "Nowe wpisy w dziale 4 KRS",
    "A-DZ5-NEW": "Nowe wpisy w dziale 5 KRS",
    "A-WLASC-NOWY": "Nowy wspolnik / akcjonariusz",
    "A-WLASC-USUN": "Usuniecie wspolnika / akcjonariusza",
    "A-ZARZAD-PREZES": "Zmiana prezesa zarzadu",
    "A-ZARZAD-SKLAD": "Zmiana skladu zarzadu",
    "A-ZARZAD-REPR": "Zmiana sposobu reprezentacji",
    "A-FORMA": "Zmiana formy prawnej",
    "A-KAPITAL": "Zmiana kapitalu zakladowego",
    "A-NAZWA": "Zmiana nazwy spolki",
    "A-PKD": "Zmiana glownego PKD",
    "A-VAT-STATUS": "Zmiana statusu VAT",
    "A-VAT-KONTO-NOWE": "Nowy rachunek bankowy w Bialej Liscie VAT",
    "A-VAT-KONTO-USUN": "Usuniecie rachunku bankowego z Bialej Listy VAT",
    "A-ADRES": "Zmiana adresu siedziby",
    "A-WPIS-NR": "Nowy wpis w KRS",
    "A-CRBR-BRAK": "Brak zgloszenia w CRBR",
    "A-CRBR-BEN-NOWY": "Nowy beneficjent rzeczywisty",
    "A-CRBR-BEN-USUN": "Usuniecie beneficjenta rzeczywistego",
    "A-CRBR-BEN-NOWY-WPIS": "Pojawil sie wpis w CRBR",
    "A-CRBR-BEN-ZNIKNAL-WPIS": "Zniknal wpis z CRBR",
    "A-CRBR-BEN-SKLAD": "Zmiana skladu beneficjentow CRBR",  # legacy
}

NEXT_STEP: dict[str, str] = {
    "A-DZ6-NEW": "Sprawdzic rodzaj postepowania i jego status w KRS online.",
    "A-DZ4-NEW": "Zidentyfikowac wierzyciela i przedmiot zaleglosci.",
    "A-DZ5-NEW": "Sprawdzic podstawe powolania kuratora lub zarzadu komisarycznego.",
    "A-WLASC-NOWY": "Zidentyfikowac nowego wspolnika i jego udzial — porowac z CRBR.",
    "A-WLASC-USUN": "Sprawdzic czy zmiana wlascicielska odbywa sie rowniez w CRBR.",
    "A-ZARZAD-PREZES": "Sprawdzic wplyw na reprezentacje spolki i uprawnienia do podpisu.",
    "A-ZARZAD-SKLAD": "Sprawdzic, czy zmiana wplywa na reprezentacje spolki.",
    "A-ZARZAD-REPR": "Sprawdzic nowy sposob reprezentacji — implikacje dla umow.",
    "A-FORMA": "Zmiana formy prawnej — weryfikacja dokumentow i kontraktow.",
    "A-KAPITAL": "Sprawdzic przyczyny zmiany kapitalu — podwyzszenie lub obnizenie.",
    "A-NAZWA": "Zaktualizowac dane spolki we wszystkich systemach.",
    "A-PKD": "Sprawdzic, czy zmiana PKD odzwierciedla faktyczna zmiane dzialalnosci.",
    "A-VAT-STATUS": "Sprawdzic przyczyne zmiany — utrata VAT to sygnal ostrzegawczy dla compliance.",
    "A-VAT-KONTO-NOWE": "Zidentyfikowac nowy rachunek i potwierdzic wlasciciela w Bialej Liscie.",
    "A-VAT-KONTO-USUN": "Sprawdzic czy rachunek zostal zablokowany lub spolka zmienila bank.",
    "A-ADRES": "Zapisac zmiane w historii, brak eskalacji.",
    "A-CRBR-BRAK": "Zweryfikowac, czy spolka powinna byc w CRBR.",
    "A-CRBR-BEN-NOWY": "Zapisac zmiane i porowac z kolejnym snapshotem KRS.",
    "A-CRBR-BEN-USUN": "Zapisac zmiane i porowac z kolejnym snapshotem KRS.",
    "A-CRBR-BEN-NOWY-WPIS": "Nowy wpis w CRBR — zidentyfikowac beneficjentow.",
    "A-CRBR-BEN-ZNIKNAL-WPIS": "Wpis zniknal z CRBR — sprawdzic przyczyne.",
    "A-CRBR-BEN-SKLAD": "Zweryfikowac zmiane beneficjentow i porowac z KRS.",
}

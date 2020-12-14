


def valikko():
    """
    Esittää valikon ja käsittelee valinnat.
    """
    print("")
    print("    Valitse seuraavista:")
    print("     [1] Uusi peli")
    print("     [2] Näytä historia")
    print("     [3] Lopeta")
    while True:
        syote = input("     Valinta: ")
        print("")
        if syote == "1":
            print("setuppi")
            break
        elif syote == "2":
            print("dataa dataa dataa")
        elif syote == "3":
            print("lopetetaan..")
            break
        else:
            print("     Virheellinen syöte!")

valikko()


def valikko2():
    print()
    print(" Tämä ohjelma muuntaa yhdysvaltalaisia yksiköitä SI-yksiköiksi")
    print()
    print("  Mahdolliset toiminnot:")
    print("    (P)ituus (in/\", ft/', yd, mi)")
    print("    (M)assa (oz, lb)")
    print("    (T)ilavuus (cp, pt, qt, gal)")
    print("    (L)ämpötila (fahrenheit)")
    print("    (Q)Lopeta")
    while True:
        print()
        valinta = input("  Tee valintasi: ").strip().lower()
        if valinta == "lämpotila" or valinta == "l":
            print("testi")
        elif valinta in ("p", "pituus", "m", "massa", "t", "tilavuus"):
            karvo = kysy_arvo()
            print(muunna(karvo))
        elif valinta == "q":
            print("  Suljetaan..")
            break
        else:
            print("  Toimintoa ei ole")
    print()

#valikko2()
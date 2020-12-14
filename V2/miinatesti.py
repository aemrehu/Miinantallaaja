import haravasto
import json
import random
import time

tila = {
    "kentta": [],
    "nakyva": [],
    "avatut": 0
}

asetukset = {
    "miinat": 0,
    "koko": [0, 0],
    "ruudut": 0,
    "voitto": 0,
    "havio": 0
}

aika = {
    "a": 0,
    "b": 0
}

DATA = []

def paiva():
    pvm = time.asctime()
    return pvm

def lataa_data():
    try:
        with open("tulokset.json") as lahde:
            n = json.load(lahde)
            try:
                for i in range(len(n)):
                    DATA.append(n[i])
            except TypeError:
                pass
    except (IOError, json.JSONDecodeError):
        print("Tiedoston avaaminen ei onnistunut.")

def tallenna(info):
    try:
        with open("tulokset.json", "w") as kohde:
            json.dump(info, kohde)
    except (IOError, json.JSONDecodeError):
        print("Tiedoston avaaminen ei onnistunut.")

def tulosta_data():
    for i in range(len(DATA)):
        print(DATA[i])

def alusta():
    """
    Asettaa pelin tilan alkupisteeseen.
    """

    tila["avatut"] = 0

    asetukset["voitto"] = 0

    asetukset["havio"] = 0

    kentta = []
    for rivi in range(asetukset["koko"][0]):
        kentta.append([])
        for sarake in range(asetukset["koko"][1]):
            kentta[-1].append(" ")
    tila["kentta"] = kentta

    nakyva = []
    for riv in range(asetukset["koko"][0]):
        nakyva.append([])
        for sarak in range(asetukset["koko"][1]):
            nakyva[-1].append(" ")
    tila["nakyva"] = nakyva

    jaljella = []
    for x in range(asetukset["koko"][1]):
        for y in range(asetukset["koko"][0]):
            jaljella.append((x, y))
    miinoita(tila["kentta"], jaljella, asetukset["miinat"])

def kirjaa_data():
    secs = aika["b"] - aika["a"]
    if secs < 0:
        kesto = "0 sek"
    elif secs < 60:
        kesto = "{:.2f} sek".format(secs)
    else: 
        kesto = "{:.1f} min".format(secs/60)
    pvm = paiva()
    if asetukset["voitto"] == 1:
        string = "{} - VOITTO ajassa: {} - Kenttä: {}*{}, miinoja {} \n".format(pvm, kesto, asetukset["koko"][0], asetukset["koko"][1], asetukset["miinat"])
    else:
        string = "{} - HÄVIÖ ajassa: {} - Kenttä: {}*{}, miinoja {} \n".format(pvm, kesto, asetukset["koko"][0], asetukset["koko"][1], asetukset["miinat"])
    DATA.append(string)

def aloita():
    """
    Toivottaa tervetulleeksi ja avaa valikon.
    """
    lataa_data()
    print("")
    print("   TERVETULOA HARAVOIMAAN MIINOJA!")
    valikko()

def lopeta():
    """
    Sulkee peli-ikkunan ja siirtyy valikkoon.
    """
    kirjaa_data()
    haravasto.lopeta()
    time.sleep(1/2)
    valikko()

def valikko():
    """
    Esittää valikon ja käsittelee valinnat.
    """
    valinnat = ["1", "2", "3"]
    print("")
    print("    Valitse seuraavista:")
    print("     [1] Uusi peli")
    print("     [2] Näytä historia")
    print("     [3] Lopeta")
    while True:
        syote = input("     Valinta: ")
        print("")
        if syote == "1":
            setup()
            break
        elif syote == "2":
            tulosta_data()
        elif syote == "3":
            print("    Lopetetaan..")
            tallenna(DATA)
            break
        else:
            print("     Virheellinen syöte!")

def kysy_luku(kysymys, alaraja, ylaraja, virhe, virheala):
    while True:
        try:
            luku = int(input(kysymys))
            if luku >= ylaraja:
                print(virhe)
                False
            elif luku < alaraja:
                print(virheala)
                False
            else:
                return luku
        except ValueError:
            print("    Arvon tulee olla kokonaisluku")

def setup():
    """
    Kysyy käyttäjältä halutun kentän koon sekä miinojen määrän.
    Asettaa asetukset.
    """
    korkeus = kysy_luku(
        "    Anna kentän korkeus: ",
        4,
        26,
        "    Liian korkea kenttä!",
        "    Liian matala kenttä!"
    )
    
    leveys = kysy_luku(
        "    Anna kentän leveys: ",
        4,
        46,
        "    Liian leveä kenttä!",
        "    Liian kapea kenttä!"
    )
    
    miinat = kysy_luku(
        "    Anna miinojen määrä: ",
        2,
        int(korkeus * leveys * 4 / 5),
        "    Liian paljon miinoja!",
        "    Liian vähän miinoja!"
    )

    print("")
    asetukset["ruudut"] = korkeus * leveys
    asetukset["koko"][0] = korkeus
    asetukset["koko"][1] = leveys
    asetukset["miinat"] = miinat
    main()

def main():
    """
    Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän.
    """
    alusta()
    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(asetukset["koko"][1] * 40, asetukset["koko"][0] * 40)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aseta_toistuva_kasittelija(paivita_peli, 1)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    aika["a"] = time.time()
    haravasto.aloita()

def miinoita(alue, ruudut, miinat):
    """
    Asettaa kentälle N kpl miinoja satunnaisiin paikkoihin.
    """
    for i in range(miinat):
        n = random.randrange(0, len(ruudut))
        x, y = ruudut[n]
        alue[y][x] = "x"
        ruudut.remove(ruudut[n])

def laske_miinat(lista, x, y):
    """
    Laskee annetussa yhden ruudun ympärillä olevat miinat ja palauttaa
    niiden lukumäärän. Funktio toimii sillä oletuksella, että valitussa ruudussa ei
    ole miinaa - jos on, sekin lasketaan mukaan.
    """
    v = []
    for j in [y-1, y, y+1]:
        for i in [x-1, x, x+1]:
            if j < 0 or i < 0:
                break
            else:
                try:
                    e = lista[j][i]
                    if e == "x":
                        v.append(e)
                except IndexError:
                    break
    if len(v) > 0:
        tila["nakyva"][y][x] = "{}".format(len(v))
        tila["kentta"][y][x] = "{}".format(len(v))

def tulvataytto(lista, x, y):
    """
    Merkitsee kentällä olevat tuntemattomat ruudut turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    """
    alku = [(y, x)]
    if lista[y][x] == "x":
        tila["nakyva"] = tila["kentta"]
        aika["b"] = time.time()
        asetukset["havio"] = 1
        print("    HÄVISIT - eteenpäin klikkaamalla -")
    else:
        while True:
            b, a = alku.pop()
            tila["nakyva"][b][a] = "0"
            lista[b][a] = "0"
            laske_miinat(tila["kentta"], a, b)
            for j in [b-1, b, b+1]:
                for i in [a-1, a, a+1]:
                    if j < 0 or i < 0:
                        pass
                    elif j == b-1 and i == a-1:
                        pass
                    elif j == b+1 and i == a-1:
                        pass
                    elif j == b-1 and i == a+1:
                        pass
                    elif j == b+1 and i == a+1:
                        pass
                    elif lista[b][a] in ("1", "2", "3", "4", "5", "6", "7", "8"):
                        break
                    else:
                        try:
                            if lista[j][i] == " ":
                                alku.append((j, i))
                        except IndexError:
                            pass
            if alku == []:
                break

def vertailu():
    """
    Vertaa avaamattomien ruutujen määrää miinojen määrään. Jos sama --> voitto
    """
    s = 0
    d = 0
    for j in range(len(tila["kentta"])):
        for i in range(len(tila["kentta"][j])):
            if tila["kentta"][j][i] == " ":
                d += 1
            elif tila["kentta"][j][i] == "x":
                s += 1
    if asetukset["voitto"] == 0:
        if s == asetukset["miinat"] and d == 0:
            voitto = True
        else:
            voitto = False
    else:
        voitto = False
    return voitto

def paivita_peli(kulunut_aika):
    """
    Päivittää peli-ikkunan.
    """
    voitto = vertailu()
    if voitto == True:
        tila["nakyva"] = tila["kentta"]
        asetukset["voitto"] = 1
        aika["b"] = time.time()
        print("    VOITIT! - eteenpäin klikkaamalla -")
    else:
        pass

def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for i in range(len(tila["nakyva"])):
        for j in range(len(tila["nakyva"][i])):
            haravasto.lisaa_piirrettava_ruutu(tila["nakyva"][i][j], j*40, i*40)
    haravasto.piirra_ruudut()

def kasittele_hiiri(x, y, nappi, muokkaus):
    """
    Käsittelee hiiren painalluksen, ja palauttaa sen koordinaatit.
    """
    if asetukset["voitto"] == 1 or asetukset["havio"] == 1:
        if nappi == haravasto.HIIRI_VASEN or nappi == haravasto.HIIRI_OIKEA:
            lopeta()
    else:
        if nappi == haravasto.HIIRI_VASEN:
            c, v = int(x/40), int(y/40)
            tulvataytto(tila["kentta"], c, v)
        elif nappi == haravasto.HIIRI_OIKEA:
            c, v = int(x/40), int(y/40)
            if tila["nakyva"][v][c] == " ":
                tila["nakyva"][v][c] = "f"
            elif tila["nakyva"][v][c] == "f":
                tila["nakyva"][v][c] = " "

if __name__ == "__main__":
    aloita()
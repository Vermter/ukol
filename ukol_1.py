class Zvire:
    def __init__(self, jmeno:str, druh:str, vaha:int):
        self.jmeno=jmeno
        self.druh=druh
        self.vaha=vaha
    def __str__(self):
        return f"{self.jmeno} je {self.druh} a váží {self.vaha} kg."
    def export_to_dict(self):
        jmeno=self.jmeno
        druh=self.druh
        vaha=self.vaha
        zvirata_dict={"jmeno":jmeno,"druh":druh,"vaha":vaha}
        return zvirata_dict
    
# pavouk = Zvire('Adolf', 'Tarantule Velká', 0.1)
# print(pavouk.export_to_dict())

panda = Zvire('Růženka', 'Panda Velká', 150)
vydra= Zvire('Vilda', 'Vydra Mořská', 20)
tygr=Zvire("Matýsek","Tygr Sumaterský", 300)
medved=Zvire("Karlík", "Lední medvěd", 700)
zvirata=[panda,vydra, tygr, medved]


def pridat_zvire(dictionary, zvirata):
    for zvire in zvirata:
        vysledek=zvire.export_to_dict()
        dictionary.append(vysledek)
zvirata_dict=[]
pridat_zvire(zvirata_dict,zvirata)

print(zvirata_dict)

# --------------------------------------------------------------------------------------

class Zamestnanec:
    def __init__(self, cele_jmeno:str, rocni_plat:int, pozice:str):
        self.cele_jmeno=cele_jmeno
        self.rocni_plat=rocni_plat
        self.pozice=pozice
    def __str__(self):
        return f"{self.cele_jmeno} pracuje na pozici {self.pozice} a jeho roční plat je {self.rocni_plat} Kč."
    def ziskej_inicialy(self):
        jmeno=self.cele_jmeno.split()
        return f"{jmeno[0][0]}. {jmeno[1][0]}."
    def export_to_dict(self):
        jmeno=self.cele_jmeno
        plat=self.rocni_plat
        pozice=self.pozice
        zamestnanci_dict={"jmeno":jmeno,"plat":plat,"pozice":pozice}
        return zamestnanci_dict
    def naklady_mesicni(self):
        return self.rocni_plat/12

tereza=Zamestnanec("Tereza Vysoká", 700_000, "cvičitelka tygrů")
anet=Zamestnanec("Anet Krasna", 600_000, "cvičitelka vyder")
martin=Zamestnanec("Martin Veliký", 650_000, "cvičitel ledních medvědů")
zamestnanci=[tereza,anet,martin]

# print(tereza.ziskej_inicialy())

def pridat_zamestnance(dictionary, lide):
    for clovek in lide:
        vysledek=clovek.export_to_dict()
        dictionary.append(vysledek)
zamestnanci_dict=[]
pridat_zamestnance(zamestnanci_dict,zamestnanci)

print(zamestnanci_dict)

# ----------------------------------------------------------------------------------------
class Reditel (Zamestnanec):
    def __init__(self, cele_jmeno, rocni_plat, oblibene_zvire:Zvire, pozice="Reditel"):
        super().__init__(cele_jmeno, rocni_plat, pozice)
        self.oblibene_zvire=oblibene_zvire
    def export_to_dict(self):
        return super().export_to_dict()
    def naklady_mesicni(self):
        return super().naklady_mesicni()

reditel = Reditel(cele_jmeno='Karel', rocni_plat=800_000, oblibene_zvire=tygr)
assert reditel.pozice == 'Reditel'
assert isinstance(reditel.oblibene_zvire, Zvire)

# ----------------------------------------------------------------------------------------


class Zoo:
    def __init__(self, jmeno:str, adresa:str, reditel:Reditel, zamestnanci:list[Zamestnanec],zvirata:list[Zvire]):
        self.jmeno=jmeno
        self.adresa=adresa
        self.reditel=reditel
        self.zamestnanci=zamestnanci
        self.zvirata=zvirata
    def vaha_vsech_zvirat_v_zoo(self):
        vaha=0
        for zvire in self.zvirata:
            vaha+=zvire.export_to_dict()["vaha"]
        return vaha
    def mesicni_naklady_na_zamestnance(self):
        naklady_z=0
        for zamestnanec in self.zamestnanci:
            naklady_z+=zamestnanec.naklady_mesicni()
        naklady_r=0
        naklady_r+=reditel.naklady_mesicni()
        return naklady_z+naklady_r
    


zoo=Zoo("ZOO Praha", "U Trojského zámku 3/120", reditel, zamestnanci, zvirata)
print(f"Váha všech zvířat v ZOO je {zoo.vaha_vsech_zvirat_v_zoo()} kg.")

print(f"Měsíční náklady na zaměstnance jsou {round(zoo.mesicni_naklady_na_zamestnance(),2)} Kč.")










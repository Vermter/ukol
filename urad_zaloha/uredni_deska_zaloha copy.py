from bs4 import BeautifulSoup
import requests
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import spacy
import stanza

# url = "https://www.mesto-kadan.cz/cs/mestsky-urad/uredni-deska-6.html"
# response = requests.get(url)
# response.encoding = "utf-8"
# soup = BeautifulSoup(response.text, "html.parser")
# text = soup.get_text()
# # -------------------------------------------------------------------





# # stanza.download("cs")
# model = stanza.Pipeline("cs", processors="tokenize, mwt, pos, lemma")
# with open("html_export.txt","r",encoding="utf-8") as file:
#     full_text = file.read()
# polozky = [p for p in full_text.split("\n\n\n") if p]

# temata = { "fotovoltaika", "baterie", "větrnný", "fotovoltaický", "solární", "obnovitelný", "smr", "jaderný", "energie","elektrárna", "bess", "fve", "vte", "tr", "transformovna"}
# zakazana_slova = {"odstávka"}

# relevantni_polozky = []

# for polozka in polozky:
#     doc = model(polozka)
#     lemmas = {word.lemma.lower() for sentence in doc.sentences for word in sentence.words}
#     # print(polozka)
#     # print(lemmas)
#     if temata & lemmas and not any(zakazane_slovo in lemmas for zakazane_slovo in zakazana_slova):
#         relevantni_polozky.append(polozka)




# if relevantni_polozky:
#     df = pd.DataFrame(relevantni_polozky, columns=["Relevantní oznámení"])
#     df.to_csv("relevantni_polozky.csv", index=False, encoding="utf-8")
#     print("seznam uložen")
# else:
#     print("nic nenalezeno")
from bs4 import BeautifulSoup
import requests
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import spacy
import stanza
import re

url = "https://ude.ginis.cloud/deska.php?deska=MUALAWO0A01S"
# response = requests.get(url)
# response.encoding = "utf-8"
# soup = BeautifulSoup(response.text, "html.parser")
# text = soup.get_text()
# with open("uredni_deska_html.txt","w", encoding="utf-8") as f:
#     f.write(text)

# -------------------------------------------------------------------

# stahování a příprava modelu pro analýzu textu
# stanza.download("cs")
model = stanza.Pipeline("cs", processors="tokenize, mwt, pos, lemma")
with open("uredni_deska_html.txt", "r", encoding="utf-8") as file:
    full_text = file.read()

# Rozdělení textu na jednotlivé položky
polozky = [p for p in full_text.split("\n") if p]

# Definice relevantních témat
temata = { 
    "fotovoltaika", "fve", "baterie", "bess", "smr", "větrný", "fotovoltaický", 
    "solární", "obnovitelný", "jaderný", "energie", "elektrárna", 
    "vte", "tr", "transformovna", "dotace"
}

# Definice zakázaných slov
zakazana_slova = {"odstávka"}

# Seznam pro relevantní položky
relevantni_polozky = []

# Funkce pro nahrazení zkratek za plné názvy
def replace_abbreviations(text):
    replacements = {
        "bess": "bateriové úložiště",
        "smr": "malý modulární reaktor",
        "fve": "fotovoltaická elektrárna",
        "vte": "větrná elektrárna",
    }
    # Pro každou zkratku v dictionary, nahradíme text
    for abbr, full_form in replacements.items():
        text = re.sub(r'\b' + re.escape(abbr) + r'\b', full_form, text, flags=re.IGNORECASE)
    return text

# Procházíme každou položku
for polozka in polozky:
    # Nahrazení zkratek za plné názvy
    polozka = replace_abbreviations(polozka)
    
    doc = model(polozka)
    lemmas = {word.lemma.lower() for sentence in doc.sentences for word in sentence.words}
    
    # Zkontrolujeme, zda se témata vyskytují a zda není položka spojená se zakázanými slovy
    if temata & lemmas and not any(zakazane_slovo in lemmas for zakazane_slovo in zakazana_slova):
        relevantni_polozky.append(polozka)

# Uložení výsledků do CSV souboru
if relevantni_polozky:
    # df = pd.DataFrame(relevantni_polozky, columns=["Relevantní oznámení"])
    df = pd.DataFrame({
        "Relevantní oznámení": relevantni_polozky,
        "URL": [url] * len(relevantni_polozky)
    })
    df.to_csv("uredni_deska_vystup.csv", index=False, encoding="utf-8")
    print("seznam uložen")
else:
    print("nic nenalezeno")

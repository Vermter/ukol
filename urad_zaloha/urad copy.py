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
# text = soup.find("table").prettify()

# with open("html_export.txt","w", encoding="utf-8") as f:
#     f.write(text)
# -------------------------------------------------------------------

# model = spacy.load("cs_core_news_sm")




# stanza.download("cs")
model = stanza.Pipeline("cs", processors="tokenize, mwt, pos, lemma")
with open("html_export.txt","r",encoding="utf-8") as file:
    full_text = file.read()
polozky = [p for p in full_text.split("\n\n\n") if p]
# polozky = [p.strip() for p in full_text.split("\n\n\n") if p.strip()]

temata = { "jaderný", "energie","elektrárna", "FVE", "VTE", "TR", "Transformovna"}
# temata = { "sbírka", "energetika", "obnovitelné zdroje", "větrnná elektrárna", "fotovoltaická elektrárna", "solární elektrárna", "fotovoltaika", "bateriové úložiště", "BESS", "FVE", "VTE", "transformovna", "elektrárna", "trafostanice", "ČEZ"}
relevantni_polozky = []


# for polozka in polozky:
#     doc = model(polozka)
#     seznam_temat = {token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha}
#     if temata & seznam_temat:
#         relevantni_polozky.append(polozka.strip())
for polozka in polozky:
    doc = model(polozka)
    lemmas = {word.lemma.lower() for sentence in doc.sentences for word in sentence.words}
    # print(polozka)
    # print(lemmas)
    if temata & lemmas:
        relevantni_polozky.append(polozka)
        print(relevantni_polozky)




if relevantni_polozky:
    df = pd.DataFrame(relevantni_polozky, columns=["Relevantní oznámení"])
    df.to_csv("relevantni_polozky.csv", index=False, encoding="utf-8")
    print("seznam uložen")
else:
    print("nic nenalezeno")

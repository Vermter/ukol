from bs4 import BeautifulSoup
import requests
from sentence_transformers import SentenceTransformer, util
import pandas as pd

url = "https://www.mesto-kadan.cz/cs/mestsky-urad/uredni-deska-6.html"
response = requests.get(url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")
text = soup.get_text()

# print(soup)
with open("html_export.txt","w", encoding="utf-8") as f:
    f.write(text)

model = SentenceTransformer("all-MiniLM-L6-v2")
with open("html_export.txt","r",encoding="utf-8") as file:
    full_text = file.read()


polozky = [p.strip() for p in full_text.split("\n\n") if p.strip()]
# \n\n

temata = [ "energetika", "obnovitelné zdroje", "větrnná elektrárna", "fotovoltaická elektrárna", "solární elektrárna", "fotovoltaika", "bateriové úložiště", "BESS", "FVE", "VTE", "transformovna", "elektrárna", "trafostanice", "ČEZ"]
temata_embendding = model.encode(temata, convert_to_tensor=True)
relevantni_polozky = []
prahova_hodnota = 0.5

for polozka in polozky:
    polozka_embedding = model.encode(polozka, convert_to_tensor=True)
    scores = util.cos_sim(polozka_embedding, temata_embendding)
    # print(polozka)
    if scores.max().item()> prahova_hodnota:
        relevantni_polozky.append(polozka)

if relevantni_polozky:
    df = pd.DataFrame(relevantni_polozky, columns=["Relevantní oznámení"])
    df.to_csv("relevantni_polozky.csv", index=False, encoding="utf-8")
    print("seznam uložen")
else:
    print("nic nenalezeno")
from bs4 import BeautifulSoup
import requests
import pandas as pd
import stanza
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Stahování a příprava modelu pro analýzu textu
stanza.download("cs")
model = stanza.Pipeline("cs", processors="tokenize, mwt, pos, lemma")

# Načítání URL z Excelového souboru
urls_df = pd.read_excel("odkazy_zdroj.xlsx")
urls = urls_df["url"].tolist()

# Definice relevantních témat
temata = { 
    "fotovoltaika", "fve", "baterie", "bess", "smr", "větrný", "fotovoltaický", 
    "solární", "obnovitelný", "jaderný", "energie", "elektrárna", 
    "vte", "tr", "transformovna", "rozpočet", "kabel"
}

# Definice zakázaných slov
zakazana_slova = {"odstávka"}

# Funkce pro nahrazení zkratek za plné názvy
def replace_abbreviations(text):
    replacements = {
        "bess": "bateriové úložiště",
        "smr": "malý modulární reaktor",
        "fve": "fotovoltaická elektrárna",
        "vte": "větrná elektrárna",
    }
    for abbr, full_form in replacements.items():
        text = re.sub(r'\b' + re.escape(abbr) + r'\b', full_form, text, flags=re.IGNORECASE)
    return text

# Funkce pro kontrolu, zda stránka používá JavaScript (na základě délky HTML)
def is_dynamic_page(url):
    response = requests.get(url)
    # Pokud je délka textu menší než nějaký prahový limit (např. 1000 znaků), předpokládáme, že jde o dynamickou stránku
    return len(response.text) < 1000

# Funkce pro získání textu stránky pomocí Selenium
def get_page_content_selenium(url):
    options = Options()
    options.add_argument("--headless")  # Spustí prohlížeč v režimu bez GUI
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)  # Počkáme na načtení obsahu
    page_content = driver.page_source
    driver.quit()
    return page_content

# Seznam pro všechny relevantní položky
vsechny_relevantni_polozky = []
url_seznam = []

# Cyklus pro procházení všech URL
for url in urls:
    # Nejprve zjistíme, zda stránka používá JavaScript nebo je statická
    if is_dynamic_page(url):
        print(f"Používám Selenium pro {url}")
        page_content = get_page_content_selenium(url)
    else:
        print(f"Stahuji {url} pomocí requests")
        response = requests.get(url)
        response.encoding = "utf-8"
        page_content = response.text


    # Zpracování obsahu
    soup = BeautifulSoup(page_content, "html.parser")
    
    # Rozdělení textu podle HTML tagů (H1, H2, H3), nových řádků (\n), čárek a středníků
    text = soup.get_text()
    polozky = [p.strip() for p in re.split(r'</?H[1-3]>|\n|,|;|\.|:|\s{3,}', text) if p.strip()]

    # Seznam pro relevantní položky pro aktuální URL
    relevantni_polozky = []

    # Procházíme každou položku
    for polozka in polozky:
        # Nahrazení zkratek za plné názvy
        polozka = replace_abbreviations(polozka)
        
        # Zpracování textu modelem
        doc = model(polozka)
        lemmas = {word.lemma.lower() for sentence in doc.sentences for word in sentence.words}

        # Zkontrolujeme, zda se témata vyskytují a zda není položka spojená se zakázanými slovy
        if temata & lemmas and not any(zakazane_slovo in lemmas for zakazane_slovo in zakazana_slova):
            relevantni_polozky.append(polozka)

    # Přidání relevantních položek pro tuto URL do celkového seznamu
    if relevantni_polozky:
        vsechny_relevantni_polozky.extend(relevantni_polozky)
        # Vytvoření seznamu URL pro tuto konkrétní stránku (stejné URL pro všechny položky z této stránky)
        url_seznam.extend([url] * len(relevantni_polozky))

# Vytvoření DataFrame a uložení výsledků do CSV
if vsechny_relevantni_polozky:
    df = pd.DataFrame({
        "Relevantní oznámení": vsechny_relevantni_polozky,
        "URL": url_seznam
    })
    df.to_csv("uredni_deska_vystup.csv", index=False, encoding="utf-8")
    print("seznam uložen")
else:
    print("nic nenalezeno")

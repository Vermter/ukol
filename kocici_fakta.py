import requests
import json

pocet = 15
# to = 0.001
to = 10

try:
    response = requests.get(f"https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount={pocet}", timeout=to)
    data = response.json()
    with open("kocky.json", mode="w", encoding="utf-8") as output_file:
        json.dump(data,output_file, indent=4, ensure_ascii=False)

    seznam_faktu = []

    for fact in range(0,pocet):
        text = data[fact]["text"]
        seznam_faktu.append(f"{fact + 1}. {text}")

    with open("kocici_fakta.json", mode="w", encoding="utf-8") as output_file:
        json.dump(seznam_faktu,output_file, indent=4, ensure_ascii=False)
except requests.exceptions.Timeout:
    print("Nebuď nedočkavý")
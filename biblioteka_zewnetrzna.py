import requests
import json
from datetime import datetime, timedelta
import os

plik = "pogoda.json"
latitude = 50.0344
longitude = 19.2103

# Pobranie daty
data = input("Podaj datę (YYYY-mm-dd), Enter = jutro: ").strip()
if not data:
    data = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

if os.path.exists(plik):
    with open(plik, "r") as f:
        zapisane = json.load(f)
else:
    zapisane = {}

if data in zapisane:
    print("Wynik z pliku:", zapisane[data])
else:
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={data}&end_date={data}"
    try:
        dane = requests.get(url).json()
        suma_opadow = dane.get("daily", {}).get("rain_sum", [None])[0]
    except:
        suma_opadow = None

    if suma_opadow is None or suma_opadow < 0:
        wynik = "Nie wiem"
    elif suma_opadow == 0.0:
        wynik = "Nie będzie padać"
    else:
        wynik = "Będzie padać"

    zapisane[data] = wynik
    with open(plik, "w") as f:
        json.dump(zapisane, f, indent=2)

    print("Wynik z API:")
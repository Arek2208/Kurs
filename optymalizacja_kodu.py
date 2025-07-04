import requests
import json
from datetime import datetime, timedelta
import os

class WeatherForecast:
    def __init__(self):
        self.filename = "pogoda.json"
        self.latitude = 50.0344
        self.longitude = 19.2103
        self.data = self.load_file()

    def load_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {}

    def save_file(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get_weather_from_api(self, date):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={date}&end_date={date}"
        try:
            response = requests.get(url)
            json_data = response.json()
            rain = json_data.get("daily", {}).get("rain_sum", [None])[0]
        except:
            rain = None

        if rain is None or rain < 0:
            return "Nie wiem"
        elif rain == 0.0:
            return "Nie będzie padać"
        else:
            return "Będzie padać"

    # Obsługa zapytań jak w słowniku
    def __getitem__(self, date):
        if date in self.data:
            return self.data[date]
        else:
            result = self.get_weather_from_api(date)
            self.data[date] = result
            self.save_file()
            return result

    def __setitem__(self, date, result):
        self.data[date] = result
        self.save_file()

    def __iter__(self):
        return iter(self.data)

    def items(self):
        return self.data.items()



def get_date_from_user():
    date = input("Podaj datę (YYYY-mm-dd), lub Enter na jutro: ").strip()
    if date == "":
        date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date ,"%Y-%m-%d")
        except :
            print("Zły format daty. Spróbuj jeszcze raz.")
            exit(1)
    return date

if __name__ == ("__main__"):
    forecast = WeatherForecast()
    date = get_date_from_user()
    result = forecast[date]
    print(f"Pogoda dla {date}: {result}")
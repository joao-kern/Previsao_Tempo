import requests
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

class Weather:
    def __init__(self):
        pass

    @staticmethod
    def request_weather(city, date, user):

        today = datetime.today()

        api_key = API_KEY
        city = f"{city}"
    
        date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")

        if datetime.strptime(date, "%Y-%m-%d") > today:
            endpoint = "https://api.weatherapi.com/v1/forecast.json"
        else:
            endpoint = "https://api.weatherapi.com/v1/history.json"
        
        url = f"{endpoint}?key={api_key}&q={city}&dt={date}&lang=pt"

        response = requests.get(url)
        data = response.json()

        if "error" in data:
            return data
        else:
            Weather.update_forecasts_file(city, date, data, user)
            return data
        
    

    @staticmethod
    def update_forecasts_file(city, date, data, user):

        directory = "weather_data_user"
        filename = "forecasts.json"
        filepath = os.path.join(directory, filename)

        if not os.path.exists(directory):
            os.makedirs(directory)

        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as json_file:
                forecasts = json.load(json_file)
        else:
            forecasts = {}

        username = user["username"]
        if username not in forecasts:
            forecasts[username] = []

        forecast_entry = {
            "city": city,
            "date": date,
            "min_temp_°C": data['forecast']['forecastday'][0]['day']['mintemp_c'],
            "max_temp_°C": data['forecast']['forecastday'][0]['day']['maxtemp_c'],
            "chance_rain_%": data["forecast"]["forecastday"][0]["day"].get("daily_chance_of_rain", 0)
        }
        forecasts[f"{user["username"]}"].append(forecast_entry)

        with open(filepath, "w", encoding="utf-8") as json_file:
            json.dump(forecasts, json_file, ensure_ascii=False, indent=4)
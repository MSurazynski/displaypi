import requests
import json
from datetime import datetime

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": "51.439270092728904",
    "longitude": "5.50632763399379",
    "hourly": ["temperature_2m", "weather_code"],
    "forecast_days": 1
}

response = requests.get(url, params=params)
data = response.json()

result = []

for time, temp, weather_code in zip(data["hourly"]["time"], data["hourly"]["temperature_2m"], data["hourly"]["weather_code"]):
    hour = datetime.fromisoformat(time).hour
    if hour in [8, 12, 14, 18]:
        print(f"{time}: {temp}°C")
        result.append({
            "hour": hour,
            "temp": round(temp),
            "weather_code": weather_code
        })

with open("data/weather.json", "w") as f:
    json.dump(result, f, indent=2)
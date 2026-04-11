from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta
import json
from utils.parse_tasks import load_and_parse_tasks


load_dotenv()
TODOIST_TOKEN = os.getenv("TODOIST_TOKEN")


def load_tasks():
    '''
    Loads tasks from the Todoist API, filters them for today's tasks, and saves the result in a JSON file. 
    If there are more than three tasks, it limits the output to three and indicates that there are more.
    '''

    all_tasks = load_and_parse_tasks()
    result = {}

    result['tasks'] = []
    result['more-than-three'] = False

    today = str(datetime.now().date())

    for task in all_tasks:
        if task.get("due") and str(task["due"]["date"]) == today:
            result['tasks'].append({"title": task["content"]})

    if len(result['tasks']) > 3:
        result['tasks'] = result['tasks'][:3]
        result['more-than-three'] = True;

    os.makedirs("assets/json", exist_ok=True)
    with open("assets/json/tasks.json", "w") as f:
        json.dump(result, f, indent=2)
    print('Tasks data loaded successfully.')


def load_date(today=True):
    '''
    Loads the date in a specific format (e.g., "Monday, 1 January") and saves it in a JSON file.
    @param today: If True, loads today's date; if False, loads tomorrow's date.
    '''
    
    if today:  
        result = [datetime.now().strftime("%A, %-d %B")]
    else:
        result = [(datetime.today() + timedelta(days=1)).strftime("%A, %-d %B")]

    os.makedirs("assets/json", exist_ok=True)
    with open("assets/json/date.json", "w") as f:
        json.dump(result, f, indent=2)
    print('Date data loaded successfully.')


def load_weather(today=True, morning=True):
    '''
    Loads the weather forecast for specific hours from the Open-Meteo API and saves the result in a JSON file.
    @param today: If True, loads today's weather; if False, loads tomorrow's weather.
    @param morning: If True, loads morning weather; if False, loads afternoon weather.
    '''
    
    url = "https://api.open-meteo.com/v1/forecast"

    target_date = datetime.now().date() if today else datetime.now().date() + timedelta(days=1)
    target_hours = [8, 10, 12, 14] if morning else [16, 18, 20, 22]

    params = {
        "latitude": "51.439270092728904",
        "longitude": "5.50632763399379",
        "hourly": ["temperature_2m", "weather_code"],
        "forecast_days": 1 if today else 2
    }

    response = requests.get(url, params=params)
    data = response.json()

    result = []

    for time, temp, weather_code in zip(data["hourly"]["time"], data["hourly"]["temperature_2m"], data["hourly"]["weather_code"]):
        timestamp = datetime.fromisoformat(time)
        if timestamp.date() == target_date and timestamp.hour in target_hours:
            result.append({
                "hour": timestamp.hour,
                "temp": round(temp),
                "weather_code": weather_code
            })

    os.makedirs("assets/json", exist_ok=True)
    with open("assets/json/weather.json", "w") as f:
        json.dump(result, f, indent=2)
    print('Weather data loaded successfully.')


if __name__ == "__main__":
    load_tasks()
    load_date()
    load_weather()


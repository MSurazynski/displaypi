from dotenv import load_dotenv

load_dotenv()

import os
import requests
from datetime import datetime, timedelta
import json
import time
import config
from utils.parse_tasks import load_and_parse_tasks


TODOIST_TOKEN = os.getenv("TODOIST_TOKEN")


def load_tasks():
    """
    Loads tasks from the Todoist API, filters them for today's tasks, and saves the result in a JSON file.
    """

    all_tasks = load_and_parse_tasks()
    result = {}

    result["tasks"] = []
    result["more-than-three"] = False

    today = str(datetime.now().date())

    for task in all_tasks:
        if task.get("due") and str(task["due"]["date"]) == today:
            result["tasks"].append({"title": task["content"]})

    # If 20th of any month add reccuring tasks
    if datetime.now().day == 25:
        result["tasks"].append({"title": "Wyprać pościele"})
        result["tasks"].append({"title": "Naoliwić deskę"})

    os.makedirs("assets/json", exist_ok=True)
    with open("assets/json/tasks.json", "w") as f:
        json.dump(result, f, indent=2)
    print("Tasks data loaded successfully.")


def load_date(today=True):
    """
    Loads the date in a specific format (e.g., "Monday, 1 January") and saves it in a JSON file.
    @param today: If True, loads today's date; if False, loads tomorrow's date.
    """

    if today:
        result = [datetime.now().strftime("%A, %-d %B")]
    else:
        result = [(datetime.today() + timedelta(days=1)).strftime("%A, %-d %B")]

    os.makedirs("assets/json", exist_ok=True)
    with open("assets/json/date.json", "w") as f:
        json.dump(result, f, indent=2)
    print("Date data loaded successfully.")


def load_weather(today=True, morning=True):
    """
    Loads the weather forecast for specific hours from the Open-Meteo API and saves the result in a JSON file.
    @param today: If True, loads today's weather; if False, loads tomorrow's weather.
    @param morning: If True, loads morning weather; if False, loads afternoon weather.
    """

    url = "https://api.open-meteo.com/v1/forecast"

    target_date = (
        datetime.now().date() if today else datetime.now().date() + timedelta(days=1)
    )
    target_hours = (
        [8, 9, 10, 11, 12, 13, 14] if morning else [16, 17, 18, 19, 20, 21, 22]
    )

    params = {
        "latitude": "51.439270092728904",
        "longitude": "5.50632763399379",
        "hourly": [
            "temperature_2m",
            "weather_code",
            "precipitation",
            "precipitation_probability",
        ],
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
        "forecast_days": 1 if today else 2,
    }

    response = requests.get(url, params=params)
    data = response.json()

    hourly_result = []

    for time, temp, weather_code, precipitation, precipitation_probability in zip(
        data["hourly"]["time"],
        data["hourly"]["temperature_2m"],
        data["hourly"]["weather_code"],
        data["hourly"]["precipitation"],
        data["hourly"]["precipitation_probability"],
    ):
        timestamp = datetime.fromisoformat(time)
        if timestamp.date() == target_date and timestamp.hour in target_hours:
            hourly_result.append(
                {
                    "hour": timestamp.hour,
                    "temp": round(temp),
                    "weather_code": weather_code,
                    "rain_mm": precipitation,
                    "rain_probability": precipitation_probability,
                }
            )

    daily_result = None

    daily_result = None
    for date_str, weather_code, temp_max, temp_min in zip(
        data["daily"]["time"],
        data["daily"]["weather_code"],
        data["daily"]["temperature_2m_max"],
        data["daily"]["temperature_2m_min"],
    ):
        date_obj = datetime.fromisoformat(date_str).date()
        if date_obj == target_date:
            daily_result = {
                "date": date_str,
                "weather_code": weather_code,
                "temp_max": round(temp_max),
                "temp_min": round(temp_min),
            }
            break

    result = {
        "hours": hourly_result,
        "day": daily_result,
    }

    os.makedirs("assets/json", exist_ok=True)
    with open("assets/json/weather.json", "w") as f:
        json.dump(result, f, indent=2)
    print("Weather data loaded successfully.")


def load_nasa_image():
    """
    Fetches NASA APOD and keeps retrying until an image is downloaded successfully.
    If the current day APOD is not an image, it automatically tries previous days.
    """

    url = "https://api.nasa.gov/planetary/apod"
    retry_delay_seconds = 5
    request_timeout_seconds = 10
    date_to_try = datetime.now().date()

    dated_image_path = (
        config.TEMP_IMAGE_DIRECTORY_PATH / config.NASA_NOT_CONVERTED_IMAGE_NAME
    )

    config.TEMP_IMAGE_DIRECTORY_PATH.mkdir(parents=True, exist_ok=True)

    if dated_image_path.exists():
        print(
            f"NASA image already exists for today: {dated_image_path}. Skipping fetch."
        )
        return dated_image_path

    while True:
        params = {
            "api_key": "DEMO_KEY",  # Replace with your NASA API key if you have one
            "date": date_to_try.isoformat(),
        }

        try:
            response = requests.get(url, params=params, timeout=request_timeout_seconds)
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as error:
            print(
                f"NASA APOD request failed: {error}. Retrying in {retry_delay_seconds}s..."
            )
            time.sleep(retry_delay_seconds)
            continue

        image_url = data.get("url", "")
        if data.get("media_type") != "image" or not image_url:
            print(
                f"NASA APOD for {date_to_try} is not an image. Trying previous day..."
            )
            date_to_try = date_to_try - timedelta(days=1)
            continue

        try:
            img_response = requests.get(image_url, timeout=request_timeout_seconds)
            img_response.raise_for_status()
        except requests.RequestException as error:
            print(
                f"Failed to download NASA image: {error}. Retrying in {retry_delay_seconds}s..."
            )
            time.sleep(retry_delay_seconds)
            continue

        with open(dated_image_path, "wb") as img_file:
            img_file.write(img_response.content)

        print(
            f"NASA image data loaded successfully from {date_to_try} to {dated_image_path}."
        )
        return dated_image_path


if __name__ == "__main__":
    load_tasks()
    load_date()
    load_weather()
    load_nasa_image()

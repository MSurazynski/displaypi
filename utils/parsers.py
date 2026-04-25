from dotenv import load_dotenv

load_dotenv()

import os
import requests
from datetime import datetime, timedelta
import json
import time
import config.config as config
from errors import *
import logging

logger = logging.getLogger(__name__)


TODOIST_TOKEN = os.getenv("TODOIST_TOKEN")


def save_tasks_to_json(tasks: list[dict]):
    """
    Parses list of tasks and saves them to json file.
    Also saves reccuring tasks for some special dates.

    Args:
        tasks: List of tasks
    """
    logger.info("Started parsing Todoist task data.")

    result = {}
    result["tasks"] = []

    today = str(datetime.now().date())

    for task in tasks:
        if task.get("due") and str(task["due"]["date"]) == today:
            result["tasks"].append({"title": task["content"]})

    # If 20th of any month add reccuring tasks
    if datetime.now().day == 25:
        result["tasks"].append({"title": "Wyprać pościele"})
        result["tasks"].append({"title": "Naoliwić deskę"})
        result["tasks"].append({"title": "Kupić Mai kwiaty na 27ego?"})

    os.makedirs("assets/json", exist_ok=True)
    with open("assets/json/tasks.json", "w") as f:
        json.dump(result, f, indent=2)

    logger.info("Tasks data saved to json successfully")


def save_weather_to_json(data: dict[dict], today=True, morning=True):
    """
    Parses weather data and saves it to json file.

    Args:
        data: weather data
        today: If True, loads today's weather; if False, loads tomorrow's weather.
        morning: If True, loads morning weather; if False, loads afternoon weather.
    """
    logger.info("Started parsing weather data.")

    TARGET_DATE = (
        datetime.now().date() if today else datetime.now().date() + timedelta(days=1)
    )
    TARGET_HOURS = (
        [8, 9, 10, 11, 12, 13, 14] if morning else [16, 17, 18, 19, 20, 21, 22]
    )

    # Compute hourly data
    hourly_result = []
    for time, temp, weather_code, precipitation, precipitation_probability in zip(
        data["hourly"]["time"],
        data["hourly"]["temperature_2m"],
        data["hourly"]["weather_code"],
        data["hourly"]["precipitation"],
        data["hourly"]["precipitation_probability"],
    ):
        timestamp = datetime.fromisoformat(time)
        if timestamp.date() == TARGET_DATE and timestamp.hour in TARGET_HOURS:
            hourly_result.append(
                {
                    "hour": timestamp.hour,
                    "temp": round(temp),
                    "weather_code": weather_code,
                    "rain_mm": precipitation,
                    "rain_probability": precipitation_probability,
                }
            )

    # Compute daily data
    daily_result = {}
    for date_str, weather_code, temp_max, temp_min in zip(
        data["daily"]["time"],
        data["daily"]["weather_code"],
        data["daily"]["temperature_2m_max"],
        data["daily"]["temperature_2m_min"],
    ):
        date_obj = datetime.fromisoformat(date_str).date()
        if date_obj == TARGET_DATE:
            daily_result = {
                "date": date_str,
                "weather_code": weather_code,
                "temp_max": round(temp_max),
                "temp_min": round(temp_min),
            }
            break

    result = {"hours": hourly_result, "day": daily_result}

    os.makedirs("assets/json", exist_ok=True)
    with open("assets/json/weather.json", "w") as f:
        json.dump(result, f, indent=2)
    logger.info("Weather data saved to json successfully.")


if __name__ == "__main__":
    load_tasks()
    load_date()
    load_weather()
    load_nasa_image()

from dotenv import load_dotenv
from pathlib import Path
import os
import requests
import logging
from errors.errors import *
from datetime import datetime
import config.config as config

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def fetch_tasks() -> list[dict]:
    """
    Fetch all tasks from the Todoist API, handling pagination if necessary.

    Raises:
        ConfigError: Missing API token.
        APIError: Any error in getting a reponse from Todoist API.
        JsonError: Response from Todoist API has unexpected shape.
    """
    logger.info("Starting to fetch data from Todoist API")

    token = os.getenv("TODOIST_TOKEN")
    if not token:
        raise ConfigError("Todoist token could not be found.")

    all_tasks: list[dict] = []
    # Points to the next page in multi page response
    cursor = None

    page_number = 0
    while True:
        page_number += 1
        logger.info(f"Handling {page_number} page of Todost tasks.")

        params = {}

        # If this is at least 2nd iteration pass cursor to the next page to the request
        if cursor:
            params["cursor"] = cursor

        try:
            response = requests.get(
                "https://api.todoist.com/api/v1/tasks",
                params=params,
                headers={"Authorization": f"Bearer {token}"},
                timeout=20,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise APIError("Todoist request failed.") from e

        # Check if reponse is a json
        try:
            data = response.json()
        except ValueError as e:
            raise JsonError("Todoist response is not a Json.") from e

        # Check if reponse data is a dict
        if not isinstance(data, dict):
            raise JsonError("Todoist reponse JSON has an unexpected shape")

        tasks_from_reponse_page = data.get("results", [])

        # Check if list of tasks from the response is a list
        if not isinstance(tasks_from_reponse_page, list):
            raise JsonError("Todoist response JSON's dict should contain a list.")

        # Add this reponse page to the list of all tasks
        all_tasks.extend(data.get("results", []))

        # Get cursor pointing to the next page
        cursor = data.get("next_cursor")
        if not cursor:
            break

    logger.info("Todoist API call is successfull.")
    return all_tasks


def fetch_weather():
    """
    Fetches the weather forecast for specific hours from the Open-Meteo API and saves the result in a JSON file.

    Raises:
        APIError: Any error in getting a response from weather API
        JsonError: Response from weather API has unexpected shape
    """

    logger.info("Starting to fetch weather data from weather API")

    URL = "https://api.open-meteo.com/v1/forecast"
    PARAMS = {
        "latitude": "51.439270092728904",
        "longitude": "5.50632763399379",
        "hourly": [
            "temperature_2m",
            "weather_code",
            "precipitation",
            "precipitation_probability",
        ],
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
        "forecast_days": 2,
    }

    try:
        response = requests.get(URL, params=PARAMS, timeout=20)
        response.raise_for_status()
    except requests.RequestException as e:
        raise APIError("Weather request failed.") from e

    # Check if response is a json
    try:
        data = response.json()
    except ValueError as e:
        raise JsonError("Weather response data is not a json.") from e

    # Check format of the response data
    if (
        not isinstance(data, dict)
        or not isinstance(data["hourly"], dict)
        or not isinstance(data["daily"], dict)
    ):
        raise JsonError("Weather data has an unexpected shape")

    logger.info("Weather API call is successfull.")
    return data


def fetch_nasa_image_and_save() -> Path:
    """
    Fetches image from NASA APOD API.

    Returns:
        Path to NASA image.

    Raises:
        APIError: Any error in getting a response from NASA API.
        JsonError: Unexpected response format.
        ResponseDataTypeError: NASA APOD for today is video and not an image.
    """
    logger.info("Starting to fetch NASA API.")

    URL = "https://api.nasa.gov/planetary/apod"
    TODAY = datetime.now().date()
    IMAGE_PATH = config.TEMP_IMAGE_DIRECTORY_PATH / config.NASA_NOT_CONVERTED_IMAGE_NAME

    # Make sure directory exists
    config.TEMP_IMAGE_DIRECTORY_PATH.mkdir(parents=True, exist_ok=True)

    # If image for this day already exists return it (in case it was already fetched today)
    if IMAGE_PATH.exists():
        logger.info(
            f"NASA image already exists for today: {IMAGE_PATH}. Skipping API fetch."
        )
        return IMAGE_PATH

    params = {
        "api_key": "DEMO_KEY",
        "date": TODAY.isoformat(),
    }

    try:
        response = requests.get(URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise APIError("NASA request failed.") from e

    try:
        data = response.json()
    except ValueError as e:
        raise JsonError("NASA response data is not a json.") from e

    if not isinstance(data, dict):
        raise JsonError("Nasa reponse data has unexpected shape.")

    if not data.get("media_type") == "image":
        raise ResponseDataTypeError("NASA APOD for today is not an image.")

    image_url = data.get("url")
    if not image_url:
        raise JsonError("Nasa response data does not have URL to image.")

    try:
        image = requests.get(image_url, timeout=10)
        image.raise_for_status()
    except requests.RequestException as e:
        raise APIError("NASA image download failed.") from e

    with open(IMAGE_PATH, "wb") as img_file:
        img_file.write(image.content)

    logger.info("NASA API called successfully.")
    return IMAGE_PATH

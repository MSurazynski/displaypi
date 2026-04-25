from dotenv import load_dotenv
import os
import sys
import utils.dashboard_export as dashboard_export
from utils.require_assets import require_assets_structure
from utils.convert_image import convert_image
import config.config as config
from utils.parsers import save_tasks_to_json, save_weather_to_json
from utils.api import fetch_tasks, fetch_weather, fetch_nasa_image_and_save
import argparse
from random import choice
import datetime
from errors.errors import *
from utils.retry import retry
import logging

logger = logging.getLogger(__name__)


parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str, required=False)
parser.add_argument("--daytime", type=str, required=False)
parser.add_argument("--day", type=str, required=False)
args = parser.parse_args()

load_dotenv()
MACHINE = os.getenv("MACHINE")


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


def display_random_private_image():
    """
    Displays random private photo from the images saved in assets/converted/private-images.
    """

    image_files = list(config.PRIVATE_IMAGES_DIRECTORY.glob("*.bmp"))
    if image_files and MACHINE == "RPI":
        random_image = choice(image_files)
        from utils.display_image import display_image

        logger.info(f"Displaying {random_image}")
        display_image(image_path=random_image)


def display_dashboard(morning=True, today=True):
    """
    Main function to generate and display the morning dashboard on the e-paper display.
    It performs the following steps:
    1. Loads the necessary data (tasks, date, weather) and saves it in JSON files.
    2. Starts the Vite development server and takes a screenshot of the dashboard page.
    3. Converts the screenshot to the required format for the e-paper display.
    4. Displays the converted image on the e-paper display (only if running on a Raspberry Pi).
    """

    # Fetch all needed data and save to json files
    try:
        tasks = retry(fetch_tasks)
        save_tasks_to_json(tasks=tasks)
    except ConfigError as e:
        logger.error(f"Config problem: {e}")
    except APIError as e:
        logger.error(f"API problem: {e}")
    except JsonError as e:
        logger.error(f"Json problem: {e}")

    try:
        data = retry(fetch_weather)
        save_weather_to_json(data=data, today=today, morning=morning)
    except APIError as e:
        logger.error(f"Api problem: {e}")
    except JsonError as e:
        logger.error(f"Json problem: {e}")

    # 2. Start Vite server and take screenshot of the dashboard page
    dashboard_export.main()

    # 3. Convert the screenshot to the required format for the e-paper display
    convert_image(
        image_to_convert_path=config.TEMP_IMAGE_DIRECTORY_PATH
        / config.DASHBOARD_NOT_CONVERTED_IMAGE_NAME,
        output_directory_path=config.DASHBOARD_CONVERTED_DIRECTORY_PATH,
    )

    # 4. Display the converted image (only if running on the Raspberry Pi)
    if MACHINE == "RPI":
        from utils.display_image import display_image

        display_image(
            image_path=config.DASHBOARD_CONVERTED_DIRECTORY_PATH
            / config.DASHBOARD_CONVERTED_IMAGE_NAME
        )


def display_nasa_photo():
    """
    Function to generate and display the NASA photo of the day on the e-paper display.
    It performs the following steps:
    1. Loads the NASA photo of the day and saves it in the assets/images/converted/nasa directory.
    2. Displays the NASA photo on the e-paper display (only if running on a Raspberry Pi).
    """

    # 1. Load NASA photo of the day
    try:
        retry(fetch_nasa_image_and_save, attempts=5)
    except APIError as e:
        logger.error(f"Api problem: {e}")
        raise
    except JsonError as e:
        logger.error(f"Json problem: {e}")
        raise
    except ResponseDataTypeError as e:
        logger.error(f"NASA provided a video instead of an image: {e}")
        raise
    except AppError:
        logger.error("Aborting.")
        raise SystemExit(1)

    # 2. Convert the NASA photo to the required format for the e-paper display
    convert_image(
        image_to_convert_path=config.TEMP_IMAGE_DIRECTORY_PATH
        / config.NASA_NOT_CONVERTED_IMAGE_NAME,
        output_directory_path=config.NASA_CONVERTED_IMAGE_DIRECTORY_PATH,
        use_smart_rotation=True,
    )

    # 2. Display the NASA photo (only if running on the Raspberry Pi)
    if MACHINE == "RPI":
        from utils.display_image import display_image

        display_image(
            image_path=config.NASA_CONVERTED_IMAGE_DIRECTORY_PATH
            / config.NASA_CONVERTED_IMAGE_NAME
        )


# Generate morning dashboard page screenshot
if __name__ == "__main__":

    setup_logging()
    require_assets_structure()

    logger.info("------------------------------------------")
    logger.info(f"Started at {datetime.datetime.now()}")

    if args.type == "dashboard":
        if args.daytime == "morning" and args.day == "today":
            display_dashboard(morning=True, today=True)
            logger.info("Morning dashboard displayed successfully.")
        elif args.daytime == "evening" and args.day == "today":
            display_dashboard(morning=False, today=True)
            logger.info("Evening dashboard displayed successfully.")
        elif args.daytime == "morning" and args.day == "tomorrow":
            display_dashboard(morning=True, today=False)
            logger.info("Morning dashboard displayed successfully.")
        elif args.daytime == "evening" and args.day == "tomorrow":
            display_dashboard(morning=False, today=False)
            logger.info("Evening dashboard displayed successfully.")
    elif args.type == "nasa":
        display_nasa_photo()
        logger.info("NASA photo displayed successfully.")

    elif args.type == "random-image":
        display_random_private_image()
        logger.info("Displaying random private image.")

    else:
        logger.info("Invalid arguments provided.")

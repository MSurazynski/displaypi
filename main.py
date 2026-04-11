from dotenv import load_dotenv
import os
import utils.dashboard_export as dashboard_export
from utils.convert_image import convert_image
from config import DASHBOARD_NOT_CONVERTED_DIRECTORY_PATH, DASHBOARD_IMAGE_NAME, DASHBOARD_CONVERTED_DIRECTORY_PATH
from utils.data import load_tasks, load_date, load_weather
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--daytime", type=str, required=False)
parser.add_argument("--day", type=str, required=False)
args = parser.parse_args()

load_dotenv()
MACHINE = os.getenv("MACHINE")


def display_today_morning_dashboard():
    '''
    Main function to generate and display the morning dashboard on the e-paper display. 
    It performs the following steps:
    1. Loads the necessary data (tasks, date, weather) and saves it in JSON files.
    2. Starts the Vite development server and takes a screenshot of the dashboard page.
    3. Converts the screenshot to the required format for the e-paper display.
    4. Displays the converted image on the e-paper display (only if running on a Raspberry Pi).
    '''
    
    #1. Load data for the dashboard (tasks, date, weather)
    load_tasks()
    load_date(today=True)
    load_weather(today=True, morning=True) 

    # 2. Start Vite server and take screenshot of the dashboard page
    dashboard_export.main()

    # 3. Convert the screenshot to the required format for the e-paper display
    convert_image(image_to_convert_path=DASHBOARD_NOT_CONVERTED_DIRECTORY_PATH / DASHBOARD_IMAGE_NAME, output_directory_path=DASHBOARD_CONVERTED_DIRECTORY_PATH)

    # 4. Display the converted image (only if running on the Raspberry Pi)
    if MACHINE == "RPI":
        from utils.display_image import display_image
        display_image(image_path=DASHBOARD_CONVERTED_DIRECTORY_PATH / DASHBOARD_IMAGE_NAME)


# Generate morning dashboard page screenshot
if __name__ == "__main__":
    if args.daytime=="morning" and args.day=="today":
        display_today_morning_dashboard()

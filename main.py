from dotenv import load_dotenv
import os
import utils.dashboard_export as dashboard_export
from utils.convert_image import convert_image
import config
from utils.data import load_tasks, load_date, load_weather, load_nasa_image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str, required=False)
parser.add_argument("--daytime", type=str, required=False)
parser.add_argument("--day", type=str, required=False)
args = parser.parse_args()

load_dotenv()
MACHINE = os.getenv("MACHINE")


def display_dashboard(morning=True, today=True):
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
    load_date(today=today)
    load_weather(today=today, morning=morning) 

    # 2. Start Vite server and take screenshot of the dashboard page
    dashboard_export.main()

    # 3. Convert the screenshot to the required format for the e-paper display
    convert_image(
        image_to_convert_path=config.TEMP_IMAGE_DIRECTORY_PATH / config.DASHBOARD_NOT_CONVERTED_IMAGE_NAME, 
        output_directory_path=config.DASHBOARD_CONVERTED_DIRECTORY_PATH
    )

    # 4. Display the converted image (only if running on the Raspberry Pi)
    if MACHINE == "RPI":
        from utils.display_image import display_image
        display_image(image_path=config.DASHBOARD_CONVERTED_DIRECTORY_PATH / config.DASHBOARD_CONVERTED_IMAGE_NAME)

def display_nasa_photo():
    '''
    Function to generate and display the NASA photo of the day on the e-paper display. 
    It performs the following steps:
    1. Loads the NASA photo of the day and saves it in the assets/images/converted/nasa directory.
    2. Displays the NASA photo on the e-paper display (only if running on a Raspberry Pi).
    '''
    
    # 1. Load NASA photo of the day
    load_nasa_image()

    # 2. Convert the NASA photo to the required format for the e-paper display
    convert_image(
        image_to_convert_path=config.TEMP_IMAGE_DIRECTORY_PATH / config.NASA_NOT_CONVERTED_IMAGE_NAME, 
        output_directory_path=config.NASA_CONVERTED_IMAGE_DIRECTORY_PATH,
        use_smart_rotation=True
    )  

    # 2. Display the NASA photo (only if running on the Raspberry Pi)
    if MACHINE == "RPI":
        from utils.display_image import display_image
        display_image(image_path=config.NASA_CONVERTED_IMAGE_DIRECTORY_PATH / config.NASA_CONVERTED_IMAGE_NAME)

# Generate morning dashboard page screenshot
if __name__ == "__main__":
    
    if args.type == "dashboard":
        if args.daytime == "morning" and args.day == "today":
            display_dashboard(morning=True, today=True)
            print("Morning dashboard displayed successfully.")
        elif args.daytime == "evening" and args.day == "today":
            display_dashboard(morning=False, today=True)
            print("Evening dashboard displayed successfully.")

    elif args.type == "nasa":
        display_nasa_photo()
        print("NASA photo displayed successfully.")

    else:
        print("Invalid arguments provided.")

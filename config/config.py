from pathlib import Path
from datetime import datetime

DASHBOARD_PAGE_PROJECT_DIR = Path("dashboard-page")
FALLBACK_IMAGE_DIRECTORY_PATH = Path("assets/images/fallback")

TEMP_IMAGE_DIRECTORY_PATH = Path("assets/images/temp")

DASHBOARD_CONVERTED_DIRECTORY_PATH = Path("assets/images/converted/dashboard")
DASHBOARD_NOT_CONVERTED_IMAGE_NAME = Path("dashboard-screenshot.png")
DASHBOARD_CONVERTED_IMAGE_NAME = Path("dashboard-screenshot.bmp")

NASA_CONVERTED_IMAGE_DIRECTORY_PATH = Path("assets/images/converted/nasa")
NASA_NOT_CONVERTED_IMAGE_NAME = Path(f"nasa-image-{datetime.now().date().isoformat()}.png")
NASA_CONVERTED_IMAGE_NAME = Path(f"nasa-image-{datetime.now().date().isoformat()}.bmp")

PRIVATE_IMAGES_DIRECTORY = Path("assets/images/converted/private-images")

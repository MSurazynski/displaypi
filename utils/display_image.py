import sys
sys.path.append('/home/michal/e-Paper/RaspberryPi_JetsonNano/python/lib')
from waveshare_epd import epd7in3e
from PIL import Image
import logging
from pathlib import Path


logging.basicConfig(level=logging.DEBUG)
epd = epd7in3e.EPD()

def display_image(image_path: Path):
    '''
    Displays the converted image on the e-paper display.
    @param image_path: Path to the converted image (expected 480x800 or 800x480 in BMP format).
    '''
    if not image_path.exists():
        logging.error(f"Image not found: {image_path}")
        return

    try:
        logging.info("Initializing display...")
        epd.init()
        epd.Clear()

        logging.info("Loading image...")
        img = Image.open(image_path)

        # Standardize to panel orientation explicitly to avoid implicit driver rotation surprises.
        if img.size == (epd.height, epd.width):
            img = img.rotate(270, expand=True)
        elif img.size != (epd.width, epd.height):
            logging.warning("Unexpected image dimensions %s, resizing to panel size %sx%s", img.size, epd.width, epd.height)
            img = img.resize((epd.width, epd.height))

        logging.info("Displaying image...")
        epd.display(epd.getbuffer(img))

        logging.info("Done. Putting display to sleep.")
        epd.sleep()

    except KeyboardInterrupt:
        logging.info("Interrupted")
        epd.sleep()
        exit()
    except Exception as e:
        logging.error(f"Error: {e}")
        epd.sleep()

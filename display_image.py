import sys
sys.path.append('/home/michal/e-Paper/RaspberryPi_JetsonNano/python/lib')


from waveshare_epd import epd7in3e
from PIL import Image
import logging

logging.basicConfig(level=logging.DEBUG)

epd = epd7in3e.EPD()

try:
    logging.info("Initializing display...")
    epd.init()
    epd.Clear()

    logging.info("Loading image...")
    img = Image.open("images-converted/image.bmp")  # Must be 800x480
    img = img.resize((epd.width, epd.height))  # Safety resize

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
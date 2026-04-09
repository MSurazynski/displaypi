import sys
sys.path.append('/home/michal/e-Paper/RaspberryPi_JetsonNano/python/lib')
from waveshare_epd import epd7in3e


epd = epd7in3e.EPD()
epd.init()
epd.Clear()
epd.sleep()
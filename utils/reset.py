import sys
import epaper


epd = epaper.epaper("epd7in3e").EPD()
epd.init()
epd.Clear()
epd.sleep()


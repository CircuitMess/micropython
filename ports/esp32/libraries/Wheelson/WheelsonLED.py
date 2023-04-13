from machine import I2C
from .Nuvoton import WSNV_ADDR

BACKLIGHT_SET_BYTE = 0x20
BACKLIGHT_GET_BYTE = 0x21
HEADLIGHT_SET_BYTE = 0x22
HEADLIGHT_GET_BYTE = 0x23
RGB_SET_BYTE = 0x24
RGB_GET_BYTE = 0x25


class WLEDColor:
    OFF = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7


class LEDControl:
    def __init__(self, i2c):
        self.i2c = i2c

    def setBacklight(self, backlight):
        msg = bytearray([BACKLIGHT_SET_BYTE, backlight])
        self.i2c.writeto(WSNV_ADDR, msg)

    def getBacklight(self):
        msg = bytearray([BACKLIGHT_GET_BYTE])
        self.i2c.writeto(WSNV_ADDR, msg)
        value = bytearray(1)
        self.i2c.readfrom_into(WSNV_ADDR, value)
        return value[0]

    def setHeadlight(self, headlight):
        msg = bytearray([HEADLIGHT_SET_BYTE, headlight])
        self.i2c.writeto(WSNV_ADDR, msg)

    def getHeadlight(self):
        msg = bytearray([HEADLIGHT_GET_BYTE])
        self.i2c.writeto(WSNV_ADDR, msg)
        value = bytearray(1)
        self.i2c.readfrom_into(WSNV_ADDR, value)
        return value[0] & 0xFF

    def setRGB(self, colour):
        msg = bytearray([RGB_SET_BYTE, colour])
        self.i2c.writeto(WSNV_ADDR, msg)

    def getRGB(self):
        msg = bytearray([RGB_GET_BYTE])
        self.i2c.writeto(WSNV_ADDR, msg)
        value = bytearray(1)
        self.i2c.readfrom_into(WSNV_ADDR, value)
        bitColour = value[0] & 0xFF
        return WLEDColor(bitColour)

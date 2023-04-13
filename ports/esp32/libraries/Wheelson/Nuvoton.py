from machine import Pin, I2C
from .Pins import *
from time import sleep_us, sleep_ms

IDENTIFY_BYTE = 0x00
BATTERY_BYTE = 0x50
WSNV_ADDR = 0x38
WSNV_PIN_RESET = 33
SHUTDOWN_BYTE = 0x51


class NuvotonInterface:
    def __init__(self, Wire):
        self.Wire = Wire

    def begin(self):
        pin_reset = Pin(WSNV_PIN_RESET, Pin.OUT)
        pin_reset.off()
        sleep_ms(50)
        pin_reset.on()
        sleep_ms(500)

        if not WSNV_ADDR in self.Wire.scan():
            return False
        return self.identify()

    def identify(self):
        self.Wire.writeto(WSNV_ADDR, bytes([IDENTIFY_BYTE]))
        value = self.Wire.readfrom(WSNV_ADDR, 1)

        return value[0] == WSNV_ADDR

    def reset(self):
        pin_reset = Pin(WSNV_PIN_RESET, Pin.OUT)
        pin_reset.off()
        sleep_ms(50)
        pin_reset.on()

    def getBatteryVoltage(self):
        self.Wire.writeto(WSNV_ADDR, bytes([BATTERY_BYTE]))
        level = self.Wire.readfrom(WSNV_ADDR, 2)

        return level[0] << 8 | level[1]

    def getWire(self):
        return self.Wire

    def shutdown(self):
        for i in range(4):
            Motors.setMotor(i, 0)
        LED.setBacklight(False)
        LED.setHeadlight(0)
        LED.setRGB(OFF)

        self.Wire.writeto(WSNV_ADDR, bytes([SHUTDOWN_BYTE]))

    def getI2C(self):
        return self.Wire

from ST7735 import TFT
from machine import SPI, Pin, Signal, I2C
from CircuitOS import InputGPIO, Display, Piezo, RGB_LED, PanelST7735_128x128
from .Pins import *
from CircuitOS import LSM6DS3TR
from CircuitOS import BM8563

import efuse

revision = efuse.read_rev()

pins = Pins(revision)
btn_pins = Buttons(pins)

spiTFT: SPI = SPI(1, baudrate=27000000, polarity=0, phase=0, sck=Pin(pins.get(Pins.TFT_SCK)),
				  mosi=Pin(pins.get(Pins.TFT_MOSI)))

backlight = Signal(Pin(pins.get(Pins.BL), mode=Pin.OUT, value=True), invert=True)

buttons = InputGPIO(btn_pins.get_pins_array(), inverted=False)

piezo = Piezo(pins.get(Pins.BUZZ))
rgb = RGB_LED((pins.get(Pins.LED_R), pins.get(Pins.LED_G), pins.get(Pins.LED_B)), False)
if (revision == 1):
	panel = PanelST7735_128x128(spiTFT, dc=Pin(pins.get(Pins.TFT_DC), Pin.OUT),
								reset=Pin(pins.get(Pins.TFT_RST), Pin.OUT), rotation=2)
else:
	print("Unknown revision", revision)

display = Display(panel)

i2c = I2C(0, sda=Pin(pins.get(Pins.I2C_SDA)), scl=Pin(pins.get(Pins.I2C_SCL)))

imu = LSM6DS3TR(i2c)
rtc = BM8563(i2c)


def begin():
	imu.begin()
	rtc.begin()
	panel.init()

	display.fill(Display.Color.Black)
	display.commit()

	backlight.on()

	buttons.scan()

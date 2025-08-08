from machine import SPI, Pin, Signal, I2C
from CircuitOS import InputGPIO, Display, Piezo, PanelST7735_128x128, BM8563
from .Pins import *
import efuse

revision = efuse.read_rev()

pins = Pins(revision)
btn_pins = Buttons(pins)

spiTFT: SPI = SPI(1, baudrate=27000000, polarity=0, phase=0, sck=Pin(pins.get(Pins.TFT_SCK)),
				  mosi=Pin(pins.get(Pins.TFT_MOSI)))

blPin = Pin(pins.get(Pins.BL), mode=Pin.OUT, value=True)
backlight = Signal(blPin, invert=True)

buttons = InputGPIO(btn_pins.get_pins_array(), inverted=True)

piezo = Piezo(pins.get(Pins.BUZZ))
dc = Pin(pins.get(Pins.TFT_DC), Pin.OUT)
reset = Pin(pins.get(Pins.TFT_RST), Pin.OUT)

if (revision == 1):
	panel = PanelST7735_128x128(spiTFT, dc=dc, reset=reset, rotation=1)
else:
	panel = PanelST7735_128x128(spiTFT, dc=dc, reset=reset, rotation=3)
display = Display(panel)

i2c = I2C(0, sda=Pin(pins.get(Pins.I2C_SDA)), scl=Pin(pins.get(Pins.I2C_SCL)))
rtc = BM8563(i2c)
led = Signal(Pin(pins.get(Pins.LED), mode=Pin.OUT, value=False), invert=False)


def begin():
	panel.init()

	display.fill(Display.Color.Black)
	display.commit()

	backlight.on()

	buttons.scan()

	rtc.begin()

from machine import SPI, Pin, Signal, I2C
from CircuitOS import InputGPIO, Display, Piezo, PanelST7735_128x128, BM8563
from .Pins import *

spiTFT: SPI = SPI(1, baudrate=27000000, polarity=0, phase=0, sck=Pin(Pins.TFT_SCK), mosi=Pin(Pins.TFT_MOSI))

blPin = Pin(Pins.BL, mode=Pin.OUT, value=True)
backlight = Signal(blPin, invert=True)

buttons = InputGPIO(Buttons.Pins, inverted=True)

piezo = Piezo(Pins.BUZZ)
dc = Pin(Pins.TFT_DC, Pin.OUT)
reset = Pin(Pins.TFT_RST, Pin.OUT)
panel = PanelST7735_128x128(spiTFT, dc=dc, reset=reset, rotation=3)
display = Display(panel)

i2c = I2C(0, sda=Pin(Pins.I2C_SDA), scl=Pin(Pins.I2C_SCL))
rtc = BM8563(i2c)
led = Signal(Pin(Pins.LED, mode=Pin.OUT, value=False), invert=False)


def begin():
	panel.init()

	display.fill(Display.Color.Black)
	display.commit()

	backlight.on()

	buttons.scan()

	rtc.begin()

from ST7735 import TFT
from machine import SPI, Pin, Signal, I2C
from CircuitOS import InputGPIO, InputTouch, Display, PanelST7735_128x128, AW9523
from .Pins import *
from ._LED import LED

pins = Pins(0)
btn_pins = Buttons(pins)
touch_pins = Touchpads(pins)
led_pins = LEDs(pins)

spiTFT: SPI = SPI(1, baudrate=27000000, polarity=0, phase=0, sck=Pin(pins.get(Pins.TFT_SCK)),
				  mosi=Pin(pins.get(Pins.TFT_SDA)))

blPin = Pin(pins.get(Pins.LED_BACKLIGHT), mode=Pin.OUT, value=True)
backlight = Signal(blPin, invert=True)

buttons = InputGPIO(btn_pins.get_pins_array(), inverted=True)
touchpads = InputTouch(touch_pins.get_pins_array(), touch_pins.Thresholds)

i2c = I2C(0, sda=Pin(pins.get(Pins.I2C_SDA)), scl=Pin(pins.get(Pins.I2C_SCL)))
aw9523 = AW9523(i2c, 0x5b)
aw9523.begin()
aw9523.set_current_limit(3)  # Imax / 4
leds = LED(aw9523, led_pins.pins)

dc = Pin(pins.get(Pins.TFT_DC), Pin.OUT)
reset = Pin(pins.get(Pins.TFT_RST), Pin.OUT)
panel = PanelST7735_128x128(spiTFT, dc=dc, reset=reset, rotation=2)
display = Display(panel)


def begin():
	panel.init()

	display.fill(Display.Color.Black)
	display.commit()

	backlight.on()

	buttons.scan()
	touchpads.scan()

from machine import SPI, I2C, Pin
from CircuitOS import Display, PanelST7735
from .Pins import *
from .Nuvoton import *
from .LED import *
from .Motors import *
from .WheelInput import *
import efuse

revision = efuse.read_rev()
pins = Pins(revision)
btn_pins = Buttons(pins)
motor_pins = Motor(pins)

i2c = I2C(0, sda=Pin(pins.get(Pins.I2C_SDA)), scl=Pin(pins.get(Pins.I2C_SCL)))
nuvo = Nuvoton(i2c, Pin(pins.get(Pins.NUVO_RESET), Pin.OUT))

motors = Motors(nuvo)
led = LED(nuvo)
buttons = WheelInput(nuvo)

spiTFT: SPI = SPI(1, baudrate=27000000, polarity=0, phase=0, sck=Pin(pins.get(Pins.TFT_SCK)),
				  mosi=Pin(pins.get(Pins.TFT_MOSI)))

if (revision == 2):  # rev3
	panel = PanelST7735(spiTFT, dc=Pin(pins.get(Pins.TFT_DC), Pin.OUT), reset=Pin(pins.get(Pins.TFT_RST), Pin.OUT),
						cs=Pin(pins.get(Pins.TFT_CS), Pin.OUT), rotation=1, color_order_rgb=True)
elif (revision == 1):  # rev2
	panel = PanelST7735(spiTFT, dc=Pin(pins.get(Pins.TFT_DC), Pin.OUT), reset=Pin(pins.get(Pins.TFT_RST), Pin.OUT),
						cs=Pin(pins.get(Pins.TFT_CS), Pin.OUT), rotation=1, color_order_rgb=True)
else:  # rev1
	panel = PanelST7735(spiTFT, dc=Pin(pins.get(Pins.TFT_DC), Pin.OUT), reset=Pin(pins.get(Pins.TFT_RST), Pin.OUT),
						cs=Pin(pins.get(Pins.TFT_CS), Pin.OUT), rotation=1)

display = Display(panel)


class WheelBacklight:
	def on(self):
		led.set_backlight(True)

	def off(self):
		led.set_backlight(False)


backlight = WheelBacklight()


def begin():
	panel.init()

	# Can't set TFT offset before this, since panel.init() resets it to default
	if (revision == 2 or revision == 1):
		panel.tft.offset(1, 2)

	display.fill(display.Color.Black)
	display.commit()

	nuvo.begin()
	backlight.on()

	buttons.scan()

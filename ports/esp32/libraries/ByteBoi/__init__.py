from machine import SPI, Pin, Signal, I2C
from CircuitOS import Display, PCA95XX, RGBSolidGPIO, RGBSolidExpander
from .Pins import *
import efuse

revision = efuse.read_rev()

i2c = None
expander = None

if revision == 2:
	variant = 3  # v2.6
elif revision == 1:
	variant = 2  # v2.0
else:
	# HW v1.x: probe for the PCA95XX expander on the v1.0 I2C pins
	probe = Pins(0)
	i2c = I2C(0, sda=Pin(probe.get(Pins.I2C_SDA)), scl=Pin(probe.get(Pins.I2C_SCL)))
	expander = PCA95XX(i2c)
	variant = 0 if expander.begin() else 1  # v1.0 with expander, otherwise v1.1

pins = Pins(variant)
Buttons.init(pins)

# Shared SD (and v1.0 display) SPI bus. On v2.6 these lines belong to the SDMMC peripheral.
spi = None
if variant != 3:
	spi: SPI = SPI(1, baudrate=16000000, polarity=0, phase=0, sck=Pin(pins.get(Pins.SPI_SCK)),
				   mosi=Pin(pins.get(Pins.SPI_MOSI)), miso=Pin(pins.get(Pins.SPI_MISO)))

if variant == 0:
	from CircuitOS import PanelILI9341, InputPCA95XX

	panel = PanelILI9341(spi, dc=Pin(pins.get(Pins.TFT_DC), Pin.OUT), reset=Pin(pins.get(Pins.TFT_RST), Pin.OUT),
						 cs=Pin(pins.get(Pins.TFT_CS), Pin.OUT), rotation=1)
	panel.init()
	buttons = InputPCA95XX(expander)
	for btn in dir(Buttons):
		attr = getattr(Buttons, btn)
		if type(attr) != int:
			continue

		buttons.register_button(attr)


	class BBBacklight:
		def __init__(self):
			expander.pin_mode(pins.get(Pins.BL), Pin.OUT)

		def on(self):
			expander.pin_write(pins.get(Pins.BL), False)

		def off(self):
			expander.pin_write(pins.get(Pins.BL), True)


	backlight = BBBacklight()
	rgb = RGBSolidExpander(pins.get(Pins.LED_R), pins.get(Pins.LED_G), pins.get(Pins.LED_B), expander)


else:
	from CircuitOS import PanelST7789, InputShift

	# variant 2 (v2.0) and 3 (v2.6) share the same panel setup
	if variant == 2 or variant == 3:
		rotation = 3
	else:
		rotation = 1

	spiTFT: SPI = SPI(2, baudrate=16000000, polarity=1, phase=1, sck=Pin(pins.get(Pins.TFT_SCK)),
					  mosi=Pin(pins.get(Pins.TFT_MOSI)))
	panel = PanelST7789(spiTFT, dc=Pin(pins.get(Pins.TFT_DC), Pin.OUT), reset=Pin(pins.get(Pins.TFT_RST), Pin.OUT),
						rotation=rotation)
	panel.init()

	blPin = Pin(pins.get(Pins.BL), mode=Pin.OUT, value=True)
	backlight = Signal(blPin, invert=True)

	buttons = InputShift(pins.get(Pins.SHIFT_DAT), pins.get(Pins.SHIFT_CLK), pins.get(Pins.SHIFT_PL))
	rgb = RGBSolidGPIO(pins.get(Pins.LED_R), pins.get(Pins.LED_G), pins.get(Pins.LED_B))

display = Display(panel)


def begin():
	display.fill(display.Color.Black)
	display.commit()

	backlight.on()

	buttons.scan()

from machine import Pin, I2C
from CircuitOS import InputGPIO, PCA95XX
from .Pins import *
from .Motors import Motors, Motor
from ._LED import LED

pins = Pins(0)
btn_pins = Buttons(pins)
led_pins = LEDs(pins)

# GPIO4 is the power latch - driving it low powers the device off. Keep it hi-Z (input, no pulls)
pwdn = Pin(pins.get(Pins.PIN_PWDN), mode=Pin.IN, pull=None)

i2c = I2C(0, sda=Pin(pins.get(Pins.I2C_SDA)), scl=Pin(pins.get(Pins.I2C_SCL)))

pca9555 = PCA95XX(i2c, 0x20)
pca9555.begin()

leds = LED(pca9555, led_pins.pins)

# The button is active-high with external biasing - internal pulls would load the node, so leave them off
buttons = InputGPIO(btn_pins.get_pins_array(), inverted=False, pull=None)

motors = Motors(i2c)


def begin():
	pca9555.pin_mode(Pins.EXP_LED, Pin.OUT)
	leds.set_all(0)

	# The speaker amp's SD/mode pin floats after the expander reset - drive it low to mute
	pca9555.pin_mode(Pins.EXP_SD_MODE, Pin.OUT)
	pca9555.pin_write(Pins.EXP_SD_MODE, False)

	motors.begin()

	buttons.scan()

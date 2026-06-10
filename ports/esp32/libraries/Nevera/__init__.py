from machine import Pin, I2C
from CircuitOS import AW9523, InputTouch
from .Motors import *
from .Pins import *
from .Servo import Servo
from ._LED import LEDPair, RG_LEDs

pins = Pins(0)
btn_pins = Buttons(pins)
led_pins = LEDs(pins)

motor = Motors((pins.get(Pins.MOTOR_A), pins.get(Pins.MOTOR_B)))

i2c = I2C(0, sda=Pin(pins.get(Pins.I2C_SDA)), scl=Pin(pins.get(Pins.I2C_SCL)))
aw9523 = AW9523(i2c, 0x5b)
aw9523.begin()
aw9523.set_current_limit(3)  # Imax / 4

headlights = LEDPair(aw9523, pins.get(Pins.HEADLIGHT_L), pins.get(Pins.HEADLIGHT_R))
taillights = LEDPair(aw9523, pins.get(Pins.TAILLIGHT_L), pins.get(Pins.TAILLIGHT_R))
sidelights = RG_LEDs(aw9523, led_pins.get_pins_array())
buttons = InputTouch(btn_pins.get_pins_array(), btn_pins.Thresholds)

servo = Servo(pins.get(Pins.SERVO_STEER))


def begin():
	buttons.scan()
	servo.center()
	headlights.setBoth(0)
	taillights.setBoth(0)
	sidelights.setAll(0, 0)

from .Pins import *
from .MotorControl import *
from machine import Pin, Signal, I2C
from CircuitOS import AW9523, InputAW9523
from .Servos import ServoControl, Servo
from ._LED import LED

motors = MotorControl((
	(Pins.MOTOR_LEFT_A, Pins.MOTOR_LEFT_B),
	(Pins.MOTOR_RIGHT_A, Pins.MOTOR_RIGHT_B)
))

i2c = I2C(0, sda=Pin(Pins.I2C_SDA), scl=Pin(Pins.I2C_SCL))
aw9523 = AW9523(i2c, 0x5b)
aw9523.begin()
aw9523.set_current_limit(3)  # Imax / 4
aw9523.pin_mode(Pins.EXP_SPKR_EN, AW9523.OUT)
aw9523.write(Pins.EXP_SPKR_EN, False)

leds = LED(aw9523)

buttons = InputAW9523(aw9523)
buttons.register_button(Buttons.Pair)

servos = ServoControl((
	Pins.SERVO_1_PWM,
	Pins.SERVO_2_PWM,
	Pins.SERVO_3_PWM
))


def begin():
	servos.center()
	buttons.scan()

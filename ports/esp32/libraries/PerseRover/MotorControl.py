from machine import Pin, PWM
from micropython import const


class Motor:
	Left = const(0)
	Right = const(1)


class MotorControl:

	def __init__(self, pins: ((int, int), (int, int))):
		"""
		:param pins: Pin pairs for the motors. Order: Left, Right.
		"""
		self.pins = []
		self.PWM = []
		self.__values = [0] * 2

		for i in range(2):
			pinA = Pin(pins[i][0], mode=Pin.OUT, value=1)
			pinB = Pin(pins[i][1], mode=Pin.OUT, value=1)
			self.pins.append((pinA, pinB))

			pwm = PWM(self.pins[i][0], freq=1000, duty=1023)
			self.PWM.append(pwm)

	def set(self, motor: int, value: int):
		if motor < 0 or motor >= 2:
			return

		value = min(max(value, -100), 100)

		pins = self.pins[motor]
		pwm = self.PWM[motor]

		if value == 0:
			pwm.duty(1023)
			pins[0].value(1)
			pins[1].value(1)
			self.__values[motor] = 0
			return

		self.__values[motor] = value

		reverse = value > 0
		if motor == Motor.Right:
			reverse = not reverse

		value = abs(value)
		duty = int((value * 1023) / 100)

		if reverse:
			pins[1].value(1)
			duty = 1023 - duty
		else:
			pins[1].value(0)

		pwm.duty(duty)

	def get(self, motor: int):
		if motor < 0 or motor >= 2:
			return 0

		return self.__values[motor]

	def set_left(self, value: int):
		self.set(Motor.Left, value)

	def set_right(self, value: int):
		self.set(Motor.Right, value)

	def get_left(self):
		return self.get(Motor.Left)

	def get_right(self):
		return self.get(Motor.Right)

	def set_all(self, val: int | [int] | (int, int)):
		if type(val) == int:
			self.set_all((val, val))
			return

		if type(val) == tuple or type(val) == list:
			if len(val) != 2:
				return

		for i in range(2):
			self.set(i, val[i])

	def get_all(self):
		return tuple(self.get(i) for i in range(2))

	def stop_all(self):
		self.set_all((0, 0))

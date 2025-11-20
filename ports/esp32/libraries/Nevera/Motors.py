from machine import Pin, PWM
from micropython import const


class Motors:

	def __init__(self, pins: (int, int)):
		"""
		:param pins: Pin pair for the motors. Order: Left, Right.
		"""
		pinA = Pin(pins[0], mode=Pin.OUT, value=1)
		pinB = Pin(pins[1], mode=Pin.OUT, value=1)
		self.pins = (pinA, pinB)

		pwm = PWM(self.pins[0], freq=1000, duty=1023)
		self.PWM = pwm
		self.value = 0

	def set(self, value: int):
		"""
		:param value: [-100, 100], negative being reverse and positive forward direction
		"""
		value = min(max(value, -100), 100)

		if value == 0:
			self.PWM.duty(1023)
			self.pins[0].value(1)
			self.pins[1].value(1)
			self.value = 0
			return

		self.value = value

		reverse = value > 0
		value = abs(value)
		duty = int((value * 1023) / 100)

		if reverse:
			self.pins[1].value(1)
			duty = 1023 - duty
		else:
			self.pins[1].value(0)

		self.PWM.duty(duty)

	def get(self):
		return self.value

	def stop(self):
		self.set(0)

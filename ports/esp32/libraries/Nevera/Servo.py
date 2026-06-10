from machine import Pin, PWM
from micropython import const


class Servo:
	Limits = (245, 315)

	def __init__(self, pin: int):
		self.state = 0
		self.pwm = PWM(Pin(pin), freq=200)
		self.center()

	def set(self, pos: int):
		"""
		:param pos: integer [0 - 1023]
		"""
		self.state = pos
		self._send(pos)

	def get(self) -> int:
		return self.state

	def center(self):
		self.set(512)

	def _send(self, pos: int):
		value = self._map(pos)
		self.pwm.duty(value)

	def _map(self, value: int) -> int:
		limits = self.Limits
		return int((value / 1023) * (limits[1] - limits[0]) + limits[0])

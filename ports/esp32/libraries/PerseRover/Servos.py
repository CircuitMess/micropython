from machine import Pin, PWM
from micropython import const


class Servo:
	Arm = const(0)
	Pinch = const(1)
	Cam = const(2)


class ServoControl:
	Limits = [
		(216, 480),
		(216, 310),
		(180, 465)
	]

	def __init__(self, pins: tuple):
		self.pins = []
		self.state = [0] * 3

		for i in range(3):
			pwm = PWM(Pin(pins[i]), freq=200)
			self.pins.append(pwm)

		self.center()

	def set(self, motor: int, pos: int):
		self.state[motor] = pos
		self._send(motor, pos)

	def get(self, motor: int) -> int:
		return self.state[motor]

	def center(self):
		for i in range(3):
			self.set(i, 512)

	def _send(self, motor: int, pos: int):
		value = self._map(motor, pos)
		self.pins[motor].duty(value)

	def _map(self, motor: int, value: int) -> int:
		limits = self.Limits[motor]
		return int((value / 1023) * (limits[1] - limits[0]) + limits[0])

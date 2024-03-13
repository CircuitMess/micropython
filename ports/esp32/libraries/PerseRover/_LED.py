from CircuitOS import AW9523, SingleLED
from .Pins import *


class LED:

	def __init__(self, aw9523: AW9523):
		self.aw9523 = aw9523
		self.expanderPins = {
			LEDs.Camera: 0xFF,
			LEDs.Rear: 0xFF,
			LEDs.MotorLeft: 0xFF,
			LEDs.MotorRight: 0xFF,
			LEDs.Arm: 0xFF,
			LEDs.HeadlightLeft: 0x20,
			LEDs.HeadlightRight: 0x20,
			LEDs.StatusYellow: 0xFF,
			LEDs.StatusGreen: 0xFF,
			LEDs.StatusRed: 0xFF
		}

		for pin in self.expanderPins:
			self.aw9523.pin_mode(LEDs.Pins[pin], AW9523.LED)
			self.aw9523.dim(LEDs.Pins[pin], 0)

	def set(self, pin: int, value: int):
		"""
		@param pin: pin from LEDs
		@param value: value from 0 to 255
		@return:
		"""
		if pin in self.expanderPins:
			self.aw9523.dim(LEDs.Pins[pin], self.constrain_value(value, self.expanderPins[pin]))

	def constrain_value(self, value: int, limit: int) -> int:
		percent: float = max(min(1.0 * ((float(value) * float(limit)) / float(0xFF)) / float(limit), 1.0), 0.0)
		return int(percent * percent * float(limit))

from CircuitOS import AW9523, SingleLED
from .Pins import *


class LED:

	def __init__(self, aw9523: AW9523):
		self.aw9523 = aw9523
		self.expanderPins = [
			LEDs.Camera,
			LEDs.Rear,
			LEDs.MotorLeft,
			LEDs.MotorRight,
			LEDs.Arm,
			LEDs.HeadlightLeft,
			LEDs.HeadlightRight,
			LEDs.StatusYellow,
			LEDs.StatusGreen,
			LEDs.StatusRed,
		]

		for pin in self.expanderPins:
			self.aw9523.pin_mode(LEDs.Pins[pin], AW9523.LED)
			self.aw9523.dim(LEDs.Pins[pin], 0)

	def set(self, pin: int, value: int):
		"""
		@param pin: pin from LEDs
		@param value: value from 0 to 100
		@return:
		"""
		value = min(max(value, 0), 100)

		if pin in self.expanderPins:
				scaled = float(value) / 100
				scaled = scaled * scaled
				scaled = scaled * 255
				self.aw9523.dim(LEDs.Pins[pin], int(scaled))

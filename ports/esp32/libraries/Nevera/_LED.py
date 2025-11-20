from CircuitOS import AW9523, SingleLED
from .Pins import *


def scaleValue(value: int) -> int:
	"""
	Scales a value from 0-100 to 0-255, while applying square non-linearity reduction.
	:param value: [0-100]
	"""
	value = min(max(value, 0), 100)
	scaled = float(value) / 100
	scaled = scaled * scaled
	scaled = scaled * 255
	return int(scaled)


class LEDPair:
	def __init__(self, aw9523: AW9523, pinLeft: int, pinRight: int):
		self.aw9523 = aw9523
		self.pinLeft = pinLeft
		self.pinRight = pinRight

		self.aw9523.pin_mode(self.pinLeft, AW9523.LED)
		self.aw9523.dim(self.pinLeft, 0)

		self.aw9523.pin_mode(self.pinRight, AW9523.LED)
		self.aw9523.dim(self.pinRight, 0)

	def setBoth(self, value: int):
		"""
		:param value: brightness value [0-100]
		"""
		self.setLeft(scaleValue(value))
		self.setRight(scaleValue(value))

	def setLeft(self, value: int):
		self.aw9523.dim(self.pinLeft, scaleValue(value))

	def setRight(self, value: int):
		self.aw9523.dim(self.pinRight, scaleValue(value))


class RG_LEDs:
	def __init__(self, aw9523: AW9523, RGPins: [(int, int)]):
		self.aw9523 = aw9523
		self.RGPins = RGPins

		for RG in self.RGPins:
			self.aw9523.pin_mode(RG[0], AW9523.LED)
			self.aw9523.dim(RG[0], 0)
			self.aw9523.pin_mode(RG[1], AW9523.LED)
			self.aw9523.dim(RG[1], 0)

	def set(self, index: int, red: int, green: int):
		"""
		@param pin: pin from LEDs
		@param red: value from 0 to 100
		@param green: value from 0 to 100
		@return:
		"""
		self.aw9523.dim(self.RGPins[index][0], scaleValue(red))
		self.aw9523.dim(self.RGPins[index][1], scaleValue(green))

	def setAll(self, red: int, green: int):
		for index in [LEDs.Left1, LEDs.Left2, LEDs.Left3, LEDs.Right1, LEDs.Right2, LEDs.Right3]:
			self.set(index, red, green)

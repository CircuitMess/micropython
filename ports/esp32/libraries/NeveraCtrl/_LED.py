from CircuitOS import AW9523, SingleLED
from .Pins import *


class LED:
	def __init__(self, aw9523: AW9523, pins: [int]):
		self.aw9523 = aw9523
		self.pins = pins

		self.expanderLEDs = [
			LEDs.Slider0,
			LEDs.Boost0,
			LEDs.Boost1,
			LEDs.Slider4,
			LEDs.Slider3,
			LEDs.Slider2,
			LEDs.Slider1,
			LEDs.BatteryFull,
			LEDs.BatteryLow
		]

		self.gpioLEDs = [
			LEDs.Power
		]

		self.gpioLeds = [SingleLED(self.pins[led]) for led in self.gpioLEDs]

		for led in self.expanderLEDs:
			self.aw9523.pin_mode(self.pins[led], AW9523.LED)
			self.aw9523.dim(self.pins[led], 0)

		for led in self.gpioLeds:
			led.set(0)

	def set(self, pin: int, value: int):
		"""
		@param pin: pin from LEDs
		@param value: value from 0 to 100
		@return:
		"""
		value = min(max(value, 0), 100)

		if pin in self.expanderLEDs:
			scaled = float(value) / 100
			scaled = scaled * scaled
			scaled = scaled * 255
			self.aw9523.dim(self.pins[pin], int(scaled))
		elif pin in self.gpioLEDs:
			self.gpioLeds[pin].set(value)
		else:
			return

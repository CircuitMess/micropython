from CircuitOS import SingleLED


class LED:
	def __init__(self, pins: [int]):
		self.leds = [SingleLED(pin) for pin in pins]

	def set(self, led: int, value: int):
		"""
		@param led: LED from LEDs
		@param value: value from 0 to 100
		"""
		if led < 0 or led >= len(self.leds):
			return

		self.leds[led].set(value)

	def set_all(self, value: int):
		for led in self.leds:
			led.set(value)
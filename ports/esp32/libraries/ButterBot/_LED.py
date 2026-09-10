from CircuitOS import PCA95XX


class LED:
	def __init__(self, expander: PCA95XX, pins: [int]):
		self.expander = expander
		self.pins = pins

	def set(self, led: int, value: int):
		"""
		@param led: LED from LEDs
		@param value: value from 0 to 100. The LED is on the TCA9555 expander and can't be
		dimmed - any value above 0 turns it on
		"""
		if led < 0 or led >= len(self.pins):
			return

		self.expander.pin_write(self.pins[led], value > 0)

	def set_all(self, value: int):
		for pin in self.pins:
			self.expander.pin_write(pin, value > 0)

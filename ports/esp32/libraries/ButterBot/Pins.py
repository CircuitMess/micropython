from micropython import const


class Pins:
	BTN_POWER: int = const(0)
	I2C_SDA: int = const(1)
	I2C_SCL: int = const(2)
	PIN_PWDN: int = const(3)

	# TCA9555 expander pins (not ESP32 GPIOs - don't pass these to get())
	EXP_LED: int = const(0)
	EXP_SD_MODE: int = const(4)

	Rev1Map = {
		BTN_POWER: const(42),
		I2C_SDA: const(47),
		I2C_SCL: const(48),
		PIN_PWDN: const(4),
	}

	def __init__(self, revision):
		self.currentMap = None
		if revision == 0:
			self.currentMap = self.Rev1Map
		else:
			print("Unknown revision", revision)

	def get(self, pin: int) -> int:
		if not pin in self.currentMap:
			print("Pin", pin, "not in map")
			return -1
		return self.currentMap[pin]


class Buttons:
	Power: int = const(0)

	def __init__(self, pins: Pins):
		# Maps Buttons [0] to their respective GPIO pins
		self.Pins: [int] = const([
			pins.get(Pins.BTN_POWER)
		])

	def get_pins_array(self) -> [int]:
		return self.Pins


class LEDs:
	Status: int = const(0)

	def __init__(self, pins: Pins):
		# Maps LEDs to their respective TCA9555 expander pins
		self.pins: [int] = const([
			Pins.EXP_LED
		])

	def get_pins_array(self) -> [int]:
		return self.pins

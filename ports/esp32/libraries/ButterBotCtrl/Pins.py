from micropython import const


class Pins:
	LED_WIFI: int = const(0)
	LED_POWER: int = const(1)
	LED_BATTLOW: int = const(2)
	LED_BIG: int = const(3)

	BTN_MANOVER: int = const(4)
	BTN_POKE: int = const(5)
	BTN_SHUTUP: int = const(6)
	BTN_SUMMON: int = const(7)
	BTN_JOY: int = const(8)

	JOY_V: int = const(9)
	JOY_H: int = const(10)

	TFT_SCK: int = const(11)
	TFT_SDA: int = const(12)
	TFT_DC: int = const(13)
	TFT_RST: int = const(14)
	LED_BACKLIGHT: int = const(15)

	PIN_BATT: int = const(16)
	PIN_VREF: int = const(17)

	Rev1Map = {
		LED_WIFI: const(7),
		LED_POWER: const(8),
		LED_BATTLOW: const(9),
		LED_BIG: const(46),

		BTN_MANOVER: const(10),
		BTN_POKE: const(11),
		BTN_SHUTUP: const(18),
		BTN_SUMMON: const(13),
		BTN_JOY: const(21),

		JOY_V: const(4),
		JOY_H: const(5),

		TFT_SCK: const(14),
		TFT_SDA: const(15),
		TFT_DC: const(16),
		TFT_RST: const(17),
		LED_BACKLIGHT: const(45),

		PIN_BATT: const(6),
		PIN_VREF: const(19),
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
	ManualOverride: int = const(0)
	Poke: int = const(1)
	ShutUp: int = const(2)
	Summon: int = const(3)
	Joystick: int = const(4)

	def __init__(self, pins: Pins):
		# Maps Buttons [0-4] to their respective GPIO pins
		self.Pins: [int] = const([
			pins.get(Pins.BTN_MANOVER), pins.get(Pins.BTN_POKE), pins.get(Pins.BTN_SHUTUP),
			pins.get(Pins.BTN_SUMMON), pins.get(Pins.BTN_JOY)
		])

	def get_pins_array(self) -> [int]:
		return self.Pins


class LEDs:
	BigGreen: int = const(0)
	Wifi: int = const(1)
	Power: int = const(2)
	BatteryLow: int = const(3)

	def __init__(self, pins: Pins):
		# Maps LEDs to their respective GPIO pins
		self.pins: [int] = const([
			pins.get(Pins.LED_BIG), pins.get(Pins.LED_WIFI), pins.get(Pins.LED_POWER),
			pins.get(Pins.LED_BATTLOW)
		])

	def get_pins_array(self) -> [int]:
		return self.pins
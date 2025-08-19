from micropython import const


class Pins:
	BL: int = const(0)
	BATT: int = const(1)
	CHARGE: int = const(2)

	TFT_SCK: int = const(3)
	TFT_MOSI: int = const(4)
	TFT_DC: int = const(5)
	TFT_RST: int = const(6)

	I2C_SDA: int = const(7)
	I2C_SCL: int = const(8)

	LED_R: int = const(9)
	LED_G: int = const(10)
	LED_B: int = const(11)

	BUZZ: int = const(12)

	BtnUp: int = const(13)
	BtnDown: int = const(14)
	BtnSelect: int = const(15)
	BtnBack: int = const(16)

	Rev2Map = {
		BL: const(9),
		BATT: const(10),
		CHARGE: const(36),
		TFT_SCK: const(48),
		TFT_MOSI: const(34),
		TFT_DC: const(33),
		TFT_RST: const(47),
		I2C_SDA: const(4),
		I2C_SCL: const(5),
		LED_R: const(8),
		LED_G: const(7),
		LED_B: const(6),
		BUZZ: const(11),
		BtnUp: const(40),
		BtnDown: const(38),
		BtnSelect: const(39),
		BtnBack: const(37)
	}

	def __init__(self, revision):
		self.currentMap = None
		if revision == 1:
			self.currentMap = self.Rev2Map
		else:
			print("Unknown revision", revision)

	def get(self, pin: int) -> int:
		if not pin in self.currentMap:
			print("Pin", pin, "not in map")
			return -1

		return self.currentMap[pin]


class Buttons:
	Up: int = const(0)
	Down: int = const(1)
	Select: int = const(2)
	Back: int = const(3)

	def __init__(self, pins: Pins):
		# Maps Buttons [0-3] to their respective GPIO pins
		self.Pins: [int] = const([
			pins.get(Pins.BtnUp),
			pins.get(Pins.BtnDown),
			pins.get(Pins.BtnSelect),
			pins.get(Pins.BtnBack)
		])

	def get_pins_array(self) -> [int]:
		return self.Pins

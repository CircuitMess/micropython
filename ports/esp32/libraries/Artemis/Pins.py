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

	RGB_R: int = const(9)
	RGB_G: int = const(10)
	RGB_B: int = const(11)

	BUZZ: int = const(12)

	LED_1: int = const(13)
	LED_2: int = const(14)
	LED_3: int = const(15)
	LED_4: int = const(16)
	LED_5: int = const(17)
	LED_6: int = const(18)

	BtnUp: int = const(19)
	BtnDown: int = const(20)
	BtnSelect: int = const(21)
	BtnBack: int = const(22)

	Rev1Map = {
		BL: const(37),
		BATT: const(6),
		CHARGE: const(47),
		TFT_SCK: const(41),
		TFT_MOSI: const(40),
		TFT_DC: const(39),
		TFT_RST: const(38),
		I2C_SDA: const(35),
		I2C_SCL: const(36),
		RGB_R: const(33),
		RGB_G: const(34),
		RGB_B: const(48),
		BUZZ: const(11),
		LED_1: const(46),
		LED_2: const(45),
		LED_3: const(44),
		LED_4: const(43),
		LED_5: const(18),
		LED_6: const(17),
		BtnUp: const(9),
		BtnDown: const(10),
		BtnSelect: const(8),
		BtnBack: const(21)
	}

	Rev2Map = {
		BL: const(33),
		BATT: const(5),
		CHARGE: const(42),
		TFT_SCK: const(36),
		TFT_MOSI: const(35),
		TFT_DC: const(48),
		TFT_RST: const(34),
		I2C_SDA: const(40),
		I2C_SCL: const(41),
		RGB_R: const(14),
		RGB_G: const(12),
		RGB_B: const(13),
		BUZZ: const(47),
		LED_1: const(46),
		LED_2: const(45),
		LED_3: const(44),
		LED_4: const(43),
		LED_5: const(18),
		LED_6: const(17),
		BtnUp: const(1),
		BtnDown: const(2),
		BtnSelect: const(3),
		BtnBack: const(21)
	}

	def __init__(self, revision):
		self.currentMap = None
		if revision == 0 or revision == 1:
			self.currentMap = self.Rev1Map
		elif revision == 2:
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

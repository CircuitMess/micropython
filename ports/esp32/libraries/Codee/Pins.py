from micropython import const


class Pins:
	BL: int = const(0)
	BATT: int = const(1)

	TFT_SCK: int = const(2)
	TFT_MOSI: int = const(3)
	TFT_DC: int = const(4)
	TFT_RST: int = const(5)

	BUZZ: int = const(6)

	I2C_SDA: int = const(7)
	I2C_SCL: int = const(8)

	LED: int = const(9)

	BtnA: int = const(10)
	BtnB: int = const(11)
	BtnC: int = const(12)
	BtnD: int = const(13)

	Rev1Map = {
		BL: const(45),
		BATT: const(6),
		TFT_SCK: const(39),
		TFT_MOSI: const(40),
		TFT_DC: const(41),
		TFT_RST: const(42),
		BUZZ: const(44),
		I2C_SDA: const(33),
		I2C_SCL: const(34),
		LED: const(38),
		BtnA: const(2),
		BtnB: const(3),
		BtnC: const(4),
		BtnD: const(5)
	}

	Rev2Map = {
		BL: const(6),
		BATT: const(1),
		TFT_SCK: const(2),
		TFT_MOSI: const(3),
		TFT_DC: const(4),
		TFT_RST: const(5),
		BUZZ: const(7),
		I2C_SDA: const(36),
		I2C_SCL: const(35),
		LED: const(10),
		BtnA: const(8),
		BtnB: const(9),
		BtnC: const(17),
		BtnD: const(16)
	}

	def __init__(self, revision):
		self.currentMap = None
		if revision == 0:
			self.currentMap = self.Rev1Map
		elif revision == 1:
			self.currentMap = self.Rev2Map
		else:
			print("Unknown revision", revision)

	def get(self, pin: int) -> int:
		if not pin in self.currentMap:
			print("Pin", pin, "not in map")
			return -1

		return self.currentMap[pin]


class Buttons:
	A: int = const(0)
	B: int = const(1)
	C: int = const(2)
	D: int = const(3)

	def __init__(self, pins: Pins):
		# Maps Buttons [0-3] to their respective GPIO pins
		self.Pins: [int] = const([
			pins.get(Pins.BtnA),
			pins.get(Pins.BtnB),
			pins.get(Pins.BtnC),
			pins.get(Pins.BtnD)
		])

	def get_pins_array(self) -> [int]:
		return self.Pins

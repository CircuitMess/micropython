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

	BtnUp: int = const(9)
	BtnDown: int = const(10)
	BtnLeft: int = const(11)
	BtnRight: int = const(12)
	BtnA: int = const(13)
	BtnB: int = const(14)
	BtnC: int = const(15)

	LEDUp: int = const(16)
	LEDDown: int = const(17)
	LEDLeft: int = const(18)
	LEDRight: int = const(19)
	LEDA: int = const(20)
	LEDB: int = const(21)
	LEDC: int = const(22)

	# For Bit v1 and v2
	Rev1_2Map = {
		BL: const(12),
		BATT: const(10),
		TFT_SCK: const(13),
		TFT_MOSI: const(14),
		TFT_DC: const(15),
		TFT_RST: const(16),
		BUZZ: const(11),
		I2C_SDA: const(1),
		I2C_SCL: const(2),
		BtnUp: const(5),
		BtnDown: const(4),
		BtnLeft: const(3),
		BtnRight: const(6),
		BtnA: const(7),
		BtnB: const(8),
		BtnC: const(9),
		LEDUp: const(47),
		LEDDown: const(48),
		LEDLeft: const(0),
		LEDRight: const(18),
		LEDA: const(17),
		LEDB: const(45),
		LEDC: const(46),
	}

	# For Bit v3
	Rev3Map = {
		BL: const(8),
		BATT: const(3),
		TFT_SCK: const(4),
		TFT_MOSI: const(5),
		TFT_DC: const(6),
		TFT_RST: const(7),
		BUZZ: const(16),
		I2C_SDA: const(1),
		I2C_SCL: const(0),
		BtnUp: const(11),
		BtnDown: const(13),
		BtnLeft: const(12),
		BtnRight: const(9),
		BtnA: const(14),
		BtnB: const(15),
		BtnC: const(21),
		LEDUp: const(-1),
		LEDDown: const(-1),
		LEDLeft: const(-1),
		LEDRight: const(-1),
		LEDA: const(-1),
		LEDB: const(-1),
		LEDC: const(-1),
	}

	def __init__(self, revision):
		self.currentMap = None
		if revision == 0 or revision == 1 or revision == 2:
			self.currentMap = self.Rev1_2Map
		elif revision == 3:
			self.currentMap = self.Rev3Map
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
	Left: int = const(2)
	Right: int = const(3)
	A: int = const(4)
	B: int = const(5)
	C: int = const(6)

	def __init__(self, pins: Pins):
		# Maps Buttons "enum" to their respective GPIO pins
		self.Pins: [int] = const([
			pins.get(Pins.BtnUp),
			pins.get(Pins.BtnDown),
			pins.get(Pins.BtnLeft),
			pins.get(Pins.BtnRight),
			pins.get(Pins.BtnA),
			pins.get(Pins.BtnB),
			pins.get(Pins.BtnC)
		])

	def get_pins_array(self) -> [int]:
		return self.Pins


class LEDs:
	Up: int = const(0)
	Down: int = const(1)
	Left: int = const(2)
	Right: int = const(3)
	A: int = const(4)
	B: int = const(5)
	C: int = const(6)

	def __init__(self, pins: Pins):
		# Maps LED's "enum" to their respective GPIO pins
		self.Pins: [int] = const([
			pins.get(Pins.LEDUp),
			pins.get(Pins.LEDDown),
			pins.get(Pins.LEDLeft),
			pins.get(Pins.LEDRight),
			pins.get(Pins.LEDA),
			pins.get(Pins.LEDB),
			pins.get(Pins.LEDC)
		])

	def get_pins_array(self) -> [int]:
		return self.Pins

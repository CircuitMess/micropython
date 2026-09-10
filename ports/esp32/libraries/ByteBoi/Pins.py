from micropython import const


class Pins:
	BL: int = const(0)
	BATT: int = const(1)
	CHARGE: int = const(2)
	SD_SENSE: int = const(3)

	LED_R: int = const(4)
	LED_G: int = const(5)
	LED_B: int = const(6)

	SPI_SCK: int = const(7)
	SPI_MISO: int = const(8)
	SPI_MOSI: int = const(9)
	SD_CS: int = const(10)

	TFT_SCK: int = const(11)
	TFT_MOSI: int = const(12)
	TFT_CS: int = const(13)
	TFT_DC: int = const(14)
	TFT_RST: int = const(15)

	I2C_SDA: int = const(16)
	I2C_SCL: int = const(17)

	SHIFT_CLK: int = const(18)
	SHIFT_DAT: int = const(19)
	SHIFT_PL: int = const(20)

	# Button IDs as seen by the input driver (expander pin or shift register bit)
	BTN_UP: int = const(21)
	BTN_DOWN: int = const(22)
	BTN_LEFT: int = const(23)
	BTN_RIGHT: int = const(24)
	BTN_A: int = const(25)
	BTN_B: int = const(26)
	BTN_C: int = const(27)

	# ByteBoi v1.0 (eFuse revision 0, PCA95XX expander present)
	# BL, CHARGE, SD_SENSE, LED_* and BTN_* are expander pins, the display shares the SD SPI bus
	Rev1Map = {
		BL: const(12),
		BATT: const(36),
		CHARGE: const(10),
		SD_SENSE: const(8),

		LED_R: const(14),
		LED_G: const(15),
		LED_B: const(13),

		SPI_SCK: const(26),
		SPI_MISO: const(5),
		SPI_MOSI: const(32),
		SD_CS: const(2),

		TFT_SCK: const(26),
		TFT_MOSI: const(32),
		TFT_CS: const(33),
		TFT_DC: const(21),
		TFT_RST: const(27),

		I2C_SDA: const(23),
		I2C_SCL: const(22),

		SHIFT_CLK: const(-1),
		SHIFT_DAT: const(-1),
		SHIFT_PL: const(-1),

		BTN_UP: const(0),
		BTN_DOWN: const(3),
		BTN_LEFT: const(1),
		BTN_RIGHT: const(2),
		BTN_A: const(6),
		BTN_B: const(5),
		BTN_C: const(4),
	}

	# ByteBoi v1.1 (eFuse revision 0, no expander) - shift register input, GPIO RGB LED
	Rev2Map = {
		BL: const(18),
		BATT: const(36),
		CHARGE: const(35),
		SD_SENSE: const(7),

		LED_R: const(22),
		LED_G: const(23),
		LED_B: const(19),

		SPI_SCK: const(14),
		SPI_MISO: const(5),
		SPI_MOSI: const(32),
		SD_CS: const(2),

		TFT_SCK: const(26),
		TFT_MOSI: const(33),
		TFT_CS: const(-1),  # CS isn't connected in this variant
		TFT_DC: const(21),
		TFT_RST: const(27),

		I2C_SDA: const(-1),
		I2C_SCL: const(-1),

		SHIFT_CLK: const(15),
		SHIFT_DAT: const(4),
		SHIFT_PL: const(0),

		BTN_UP: const(7),
		BTN_DOWN: const(4),
		BTN_LEFT: const(5),
		BTN_RIGHT: const(6),
		BTN_A: const(3),
		BTN_B: const(2),
		BTN_C: const(1),
	}

	# ByteBoi v2.0 (eFuse revision 1) - no RGB LED
	Rev3Map = {
		BL: const(18),
		BATT: const(36),
		CHARGE: const(39),
		SD_SENSE: const(34),

		LED_R: const(-1),
		LED_G: const(-1),
		LED_B: const(-1),

		SPI_SCK: const(14),
		SPI_MISO: const(5),
		SPI_MOSI: const(32),
		SD_CS: const(2),

		TFT_SCK: const(26),
		TFT_MOSI: const(33),
		TFT_CS: const(-1),  # CS isn't connected in this variant
		TFT_DC: const(21),
		TFT_RST: const(27),

		I2C_SDA: const(-1),
		I2C_SCL: const(-1),

		SHIFT_CLK: const(15),
		SHIFT_DAT: const(4),
		SHIFT_PL: const(0),

		BTN_UP: const(7),
		BTN_DOWN: const(4),
		BTN_LEFT: const(5),
		BTN_RIGHT: const(6),
		BTN_A: const(3),
		BTN_B: const(2),
		BTN_C: const(1),
	}

	# ByteBoi v2.6 (eFuse revision 2) - shift register moved, SD on SDMMC
	Rev4Map = {
		BL: const(18),
		BATT: const(36),
		CHARGE: const(39),
		SD_SENSE: const(34),

		LED_R: const(-1),
		LED_G: const(-1),
		LED_B: const(-1),

		# SD is on the native SDMMC slot-1 pins, driven in 1-bit mode. The SPI_* names carry
		# CLK/D0/CMD. DAT3/CS isn't GPIO-connected (pulled up), so SPI mode is impossible - no SD_CS.
		SPI_SCK: const(14),
		SPI_MISO: const(2),
		SPI_MOSI: const(15),
		SD_CS: const(-1),

		TFT_SCK: const(26),
		TFT_MOSI: const(33),
		TFT_CS: const(-1),  # CS isn't connected in this variant
		TFT_DC: const(21),
		TFT_RST: const(27),

		I2C_SDA: const(-1),
		I2C_SCL: const(-1),

		SHIFT_CLK: const(22),
		SHIFT_DAT: const(4),
		SHIFT_PL: const(19),

		BTN_UP: const(7),
		BTN_DOWN: const(4),
		BTN_LEFT: const(5),
		BTN_RIGHT: const(6),
		BTN_A: const(3),
		BTN_B: const(2),
		BTN_C: const(1),
	}

	def __init__(self, variant):
		self.currentMap = None
		if variant == 0:
			self.currentMap = self.Rev1Map
		elif variant == 1:
			self.currentMap = self.Rev2Map
		elif variant == 2:
			self.currentMap = self.Rev3Map
		elif variant == 3:
			self.currentMap = self.Rev4Map
		else:
			print("Unknown variant", variant)

	def get(self, pin: int) -> int:
		if not pin in self.currentMap:
			print("Pin", pin, "not in map")
			return -1

		return self.currentMap[pin]


class Buttons:
	# Defaults match the v1.0 expander layout; Buttons.init(pins) applies the current variant's IDs
	Up: int = 0
	Down: int = 3
	Left: int = 1
	Right: int = 2
	A: int = 6
	B: int = 5
	C: int = 4

	@classmethod
	def init(cls, pins: Pins):
		cls.Up = pins.get(Pins.BTN_UP)
		cls.Down = pins.get(Pins.BTN_DOWN)
		cls.Left = pins.get(Pins.BTN_LEFT)
		cls.Right = pins.get(Pins.BTN_RIGHT)
		cls.A = pins.get(Pins.BTN_A)
		cls.B = pins.get(Pins.BTN_B)
		cls.C = pins.get(Pins.BTN_C)

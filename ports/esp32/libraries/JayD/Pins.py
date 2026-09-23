from micropython import const


class Pins:
	I2C_SDA: int = const(0)
	I2C_SCL: int = const(1)

	BL: int = const(2)

	SPI_SCK: int = const(3)
	SPI_MISO: int = const(4)
	SPI_MOSI: int = const(5)

	SD_CS: int = const(6)

	TFT_CS: int = const(7)
	TFT_DC: int = const(8)
	TFT_RST: int = const(9)

	NUVO_RESET: int = const(10)

	# For original Jay-D and Jay-D v1.7 (eFuse revision 0, 1, 2)
	Rev1Map = {
		I2C_SDA: const(26),
		I2C_SCL: const(27),

		BL: const(25),

		SPI_SCK: const(18),
		SPI_MISO: const(19),
		SPI_MOSI: const(23),

		SD_CS: const(22),

		TFT_CS: const(32),
		TFT_DC: const(33),
		TFT_RST: const(2),

		NUVO_RESET: const(13),
	}

	# For Jay-D v1.9 (eFuse revision 3) - SD card moved to SD-MMC, so there is no
	# SPI MISO / SD_CS; GPIO19 is I2S data out and the TFT reset moved to GPIO12
	Rev2Map = {
		I2C_SDA: const(26),
		I2C_SCL: const(27),

		BL: const(25),

		SPI_SCK: const(18),
		SPI_MISO: const(-1),
		SPI_MOSI: const(23),

		SD_CS: const(-1),

		TFT_CS: const(32),
		TFT_DC: const(33),
		TFT_RST: const(12),

		NUVO_RESET: const(13),
	}

	def __init__(self, revision):
		self.currentMap = None
		if revision == 0 or revision == 1 or revision == 2:
			self.currentMap = self.Rev1Map
		elif revision == 3:
			self.currentMap = self.Rev2Map
		else:
			print("Unknown revision", revision)

	def get(self, pin: int) -> int:
		if not pin in self.currentMap:
			print("Pin", pin, "not in map")
			return -1

		return self.currentMap[pin]


class Buttons:
	Left: int = 0
	Right: int = 1
	Enc_Mid: int = const(2)
	Enc_Left1: int = const(3)
	Enc_Left2: int = const(8)
	Enc_Left3: int = const(7)
	Enc_Right1: int = const(6)
	Enc_Right2: int = const(5)
	Enc_Right3: int = const(4)


class Encoders:
	Mid: int = 0
	Left1: int = const(1)
	Left2: int = const(6)
	Left3: int = const(5)
	Right1: int = const(4)
	Right2: int = const(3)
	Right3: int = const(2)


class Sliders:
	Mid: int = const(0)
	Left: int = const(1)
	Right: int = const(2)

from micropython import const


class Pins:
	BL: int = const(45)
	BATT: int = const(6)

	TFT_SCK: int = const(39)
	TFT_MOSI: int = const(40)
	TFT_DC: int = const(41)
	TFT_RST: int = const(42)

	BUZZ: int = const(44)

	I2C_SDA: int = const(33)
	I2C_SCL: int = const(34)

	LED: int = const(38)


class Buttons:
	A: int = const(0)
	B: int = const(1)
	C: int = const(2)
	D: int = const(3)

	# Maps Buttons [0-3] to their respective GPIO pins
	Pins: [int] = const([
		const(2),
		const(3),
		const(4),
		const(5)
	])

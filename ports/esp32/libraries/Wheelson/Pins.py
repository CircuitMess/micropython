from micropython import const


class Pins:
	TFT_SCK: int = const(0)
	TFT_MOSI: int = const(1)
	TFT_DC: int = const(2)
	TFT_RST: int = const(3)
	TFT_CS: int = const(4)

	I2C_SDA: int = const(5)
	I2C_SCL: int = const(6)
	NUVO_RESET: int = const(7)

	BtnUp: int = const(8)
	BtnDown: int = const(9)
	BtnLeft: int = const(10)
	BtnRight: int = const(11)
	BtnA: int = const(12)
	BtnB: int = const(13)

	MotorFrontLeft: int = const(14)
	MotorBackLeft: int = const(15)
	MotorFrontRight: int = const(16)
	MotorBackRight: int = const(17)

	Rev12Map = {
		TFT_SCK: const(2),
		TFT_MOSI: const(13),
		TFT_DC: const(12),
		TFT_RST: const(0),
		TFT_CS: const(32),

		I2C_SDA: const(14),
		I2C_SCL: const(15),
		NUVO_RESET: const(33),

		BtnUp: const(3),
		BtnDown: const(1),
		BtnLeft: const(0),
		BtnRight: const(2),
		BtnA: const(4),
		BtnB: const(5),

		MotorFrontLeft: const(0),
		MotorBackLeft: const(1),
		MotorFrontRight: const(2),
		MotorBackRight: const(3)
	}

	Rev3Map = {
		TFT_SCK: const(2),
		TFT_MOSI: const(13),
		TFT_DC: const(12),
		TFT_RST: const(0),
		TFT_CS: const(32),

		I2C_SDA: const(14),
		I2C_SCL: const(15),
		NUVO_RESET: const(33),

		BtnUp: const(0),
		BtnDown: const(1),
		BtnLeft: const(2),
		BtnRight: const(3),
		BtnA: const(4),
		BtnB: const(5),

		MotorFrontLeft: const(0),
		MotorBackLeft: const(1),
		MotorFrontRight: const(2),
		MotorBackRight: const(3)
	}

	def __init__(self, revision):
		self.currentMap = None
		if revision == 0 or revision == 1:
			self.currentMap = self.Rev12Map
		elif revision == 2:
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

	def __init__(self, pins: Pins):
		Buttons.Up = pins.get(Pins.BtnUp)
		Buttons.Down = pins.get(Pins.BtnDown)
		Buttons.Left = pins.get(Pins.BtnLeft)
		Buttons.Right = pins.get(Pins.BtnRight)
		Buttons.A = pins.get(Pins.BtnA)
		Buttons.B = pins.get(Pins.BtnB)


class Motor:
	FrontLeft: int = const(0)
	BackLeft: int = const(1)
	FrontRight: int = const(2)
	BackRight: int = const(3)

	def __init__(self, pins: Pins):
		Motor.FrontLeft = pins.get(Pins.MotorFrontLeft)
		Motor.BackLeft = pins.get(Pins.MotorBackLeft)
		Motor.FrontRight = pins.get(Pins.MotorFrontRight)
		Motor.BackRight = pins.get(Pins.MotorBackRight)

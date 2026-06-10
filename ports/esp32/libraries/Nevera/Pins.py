from micropython import const


class Pins:
	I2C_SDA: int = const(0)
	I2C_SCL: int = const(1)
	BTN_PAIR: int = const(2)
	MOTOR_A: int = const(3)
	MOTOR_B: int = const(4)
	SERVO_STEER: int = const(5)

	HEADLIGHT_L: int = const(6)
	HEADLIGHT_R: int = const(7)
	TAILLIGHT_L: int = const(8)
	TAILLIGHT_R: int = const(9)
	LEFT1_R: int = const(10)
	LEFT1_G: int = const(11)
	LEFT2_R: int = const(12)
	LEFT2_G: int = const(13)
	LEFT3_R: int = const(14)
	LEFT3_G: int = const(15)
	RIGHT1_R: int = const(16)
	RIGHT1_G: int = const(17)
	RIGHT2_R: int = const(18)
	RIGHT2_G: int = const(19)
	RIGHT3_R: int = const(20)
	RIGHT3_G: int = const(21)

	Rev1Map = {
		I2C_SDA: const(35),
		I2C_SCL: const(36),
		BTN_PAIR: const(1),
		MOTOR_A: const(37),
		MOTOR_B: const(38),
		SERVO_STEER: const(39),

		# AW9523 pins
		HEADLIGHT_L: const(9),
		HEADLIGHT_R: const(8),
		TAILLIGHT_L: const(4),
		TAILLIGHT_R: const(5),
		LEFT1_R: const(11),
		LEFT1_G: const(10),
		LEFT2_R: const(1),
		LEFT2_G: const(0),
		LEFT3_R: const(3),
		LEFT3_G: const(2),
		RIGHT1_R: const(15),
		RIGHT1_G: const(14),
		RIGHT2_R: const(13),
		RIGHT2_G: const(12),
		RIGHT3_R: const(7),
		RIGHT3_G: const(6),
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
	Pair: int = const(0)

	Thresholds: [int] = const([
		35000,  # Pair, TODO - maybe check and adjust threshold after measuring on multiple devices
	])

	def __init__(self, pins: Pins):
		# Maps Buttons [0-3] to their respective GPIO pins
		self.Pins: [int] = const([
			pins.get(Pins.BTN_PAIR),
		])

	def get_pins_array(self) -> [int]:
		return self.Pins


class LEDs:
	Left1: int = const(0)
	Left2: int = const(1)
	Left3: int = const(2)
	Right1: int = const(3)
	Right2: int = const(4)
	Right3: int = const(5)

	# Maps LEDs to their respective GPIO or expander pins
	def __init__(self, pins: Pins):
		self.Pins: [(int, int)] = const([
			(pins.get(Pins.LEFT1_R), pins.get(Pins.LEFT1_G)),
			(pins.get(Pins.LEFT2_R), pins.get(Pins.LEFT2_G)),
			(pins.get(Pins.LEFT3_R), pins.get(Pins.LEFT3_G)),
			(pins.get(Pins.RIGHT1_R), pins.get(Pins.RIGHT1_G)),
			(pins.get(Pins.RIGHT2_R), pins.get(Pins.RIGHT2_G)),
			(pins.get(Pins.RIGHT3_R), pins.get(Pins.RIGHT3_G)),
		])

	def get_pins_array(self) -> [(int, int)]:
		return self.Pins

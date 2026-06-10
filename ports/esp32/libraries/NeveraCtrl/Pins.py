from micropython import const


class Pins:
	I2C_SDA: int = const(0)
	I2C_SCL: int = const(1)

	# AW9523 pins
	LED_SLIDER0: int = const(2)
	LED_BOOST0: int = const(3)
	LED_BOOST1: int = const(4)
	LED_SLIDER4: int = const(5)
	LED_SLIDER3: int = const(6)
	LED_SLIDER2: int = const(7)
	LED_SLIDER1: int = const(8)
	LED_BATTFULL: int = const(9)
	LED_BATTLOW: int = const(10)
	# end AW9523 pins

	TFT_SCK: int = const(11)
	TFT_SDA: int = const(12)
	TFT_DC: int = const(13)
	TFT_RST: int = const(14)

	BTN_FWD: int = const(15)
	BTN_BCK: int = const(16)
	BTN_UP: int = const(17)
	BTN_DOWN: int = const(18)
	BTN_LEFT: int = const(19)
	BTN_RIGHT: int = const(20)

	LED_PWR: int = const(22)
	LED_BACKLIGHT: int = const(23)

	SLIDER_0: int = const(24)
	SLIDER_1: int = const(25)
	SLIDER_2: int = const(26)
	SLIDER_3: int = const(27)
	SLIDER_4: int = const(28)

	Rev1Map = {
		I2C_SDA: const(12),
		I2C_SCL: const(13),

		# AW9523 pins
		LED_SLIDER0: const(0),
		LED_BOOST0: const(1),
		LED_BOOST1: const(2),
		LED_SLIDER4: const(8),
		LED_SLIDER3: const(9),
		LED_SLIDER2: const(10),
		LED_SLIDER1: const(11),
		LED_BATTFULL: const(13),
		LED_BATTLOW: const(14),

		TFT_SCK: const(47),
		TFT_SDA: const(33),
		TFT_DC: const(34),
		TFT_RST: const(48),

		BTN_FWD: const(15),
		BTN_BCK: const(16),
		BTN_UP: const(37),
		BTN_DOWN: const(39),
		BTN_LEFT: const(38),
		BTN_RIGHT: const(36),

		LED_PWR: const(14),
		LED_BACKLIGHT: const(40),

		SLIDER_0: const(2),
		SLIDER_1: const(4),
		SLIDER_2: const(5),
		SLIDER_3: const(6),
		SLIDER_4: const(7),
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
	Forward: int = const(0)
	Backward: int = const(1)
	Up: int = const(2)
	Down: int = const(3)
	Left: int = const(4)
	Right: int = const(5)

	def __init__(self, pins: Pins):
		# Maps Buttons [0-3] to their respective GPIO pins
		self.Pins: [int] = const([
			pins.get(Pins.BTN_FWD), pins.get(Pins.BTN_BCK), pins.get(Pins.BTN_UP), pins.get(Pins.BTN_DOWN),
			pins.get(Pins.BTN_LEFT), pins.get(Pins.BTN_RIGHT)
		])

	def get_pins_array(self) -> [int]:
		return self.Pins


class Touchpads:
	Slider0: int = const(2)
	Slider1: int = const(4)
	Slider2: int = const(5)
	Slider3: int = const(6)
	Slider4: int = const(7)

	Thresholds: [int] = const([
		35000,  # Slider0
		35000,
		35000,
		35000,
		35000  # Slider4
	])

	def __init__(self, pins: Pins):
		# Maps Buttons [0-3] to their respective GPIO pins
		self.Pins: [int] = const([
			pins.get(Pins.SLIDER_0), pins.get(Pins.SLIDER_1), pins.get(Pins.SLIDER_2), pins.get(Pins.SLIDER_3),
			pins.get(Pins.SLIDER_4)
		])

	def get_pins_array(self) -> [int]:
		return self.Pins


class LEDs:
	# AW9523 pins
	Slider0: int = const(0)
	Boost0: int = const(1)
	Boost1: int = const(2)
	Slider4: int = const(3)
	Slider3: int = const(4)
	Slider2: int = const(5)
	Slider1: int = const(6)
	BatteryFull: int = const(7)
	BatteryLow: int = const(8)

	# GPIO pins
	Power: int = const(9)

	def __init__(self, pins: Pins):
		# Maps LEDs to their respective GPIO or expander pins
		self.pins: [int] = const([
			pins.get(Pins.LED_SLIDER0), pins.get(Pins.LED_BOOST0), pins.get(Pins.LED_BOOST1),
			pins.get(Pins.LED_SLIDER4), pins.get(Pins.LED_SLIDER3), pins.get(Pins.LED_SLIDER2),
			pins.get(Pins.LED_SLIDER1), pins.get(Pins.LED_BATTFULL), pins.get(Pins.LED_BATTLOW), pins.get(Pins.LED_PWR)
		])

	def get_pins_array(self) -> [int]:
		return self.pins

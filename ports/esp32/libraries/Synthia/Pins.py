from micropython import const


class Pins:
	I2C_SDA: int = const(0)
	I2C_SCL: int = const(1)

	INP_SCK: int = const(2)
	INP_DATA: int = const(3)
	INP_PL: int = const(4)

	I2S_BCK: int = const(5)
	I2S_WS: int = const(6)
	I2S_DO: int = const(7)
	I2S_DI: int = const(8)

	ENC_L1: int = const(9)
	ENC_L2: int = const(10)

	ENC_R1: int = const(11)
	ENC_R2: int = const(12)

	POT_L: int = const(13)
	POT_R: int = const(14)

	RGB_CLK: int = const(15)
	RGB_DATA: int = const(16)

	BtnSlot_5: int = const(17)
	BtnSlot_4: int = const(18)
	BtnSlot_3: int = const(19)
	BtnSlot_2: int = const(20)
	BtnSlot_1: int = const(21)
	BtnEnc_L: int = const(22)
	BtnEnc_R: int = const(23)

	LED_B2: int = const(24)
	LED_B1: int = const(25)
	LED_R5: int = const(26)
	LED_R4: int = const(27)
	LED_R3: int = const(28)
	LED_R2: int = const(29)
	LED_R1: int = const(30)
	LED_G5: int = const(31)
	LED_B5: int = const(32)
	LED_B4: int = const(33)
	LED_B3: int = const(34)
	LED_G4: int = const(35)
	LED_G3: int = const(36)
	LED_G2: int = const(37)
	LED_G1: int = const(38)

	LED_G9: int = const(39)
	LED_R9: int = const(40)
	LED_B9: int = const(41)
	LED_G8: int = const(42)
	LED_R8: int = const(43)
	LED_B8: int = const(44)
	LED_G7: int = const(45)
	LED_R7: int = const(46)
	LED_G10: int = const(47)
	LED_R10: int = const(48)
	LED_B10: int = const(49)
	LED_B7: int = const(50)
	LED_G6: int = const(51)
	LED_R6: int = const(52)
	LED_B6: int = const(53)

	I2C2_SDA: int = const(54)
	I2C2_SCL: int = const(55)

	Rev1Map = {
		I2C_SDA: const(23),
		I2C_SCL: const(22),
		INP_SCK: const(25),
		INP_DATA: const(27),
		INP_PL: const(19),
		I2S_BCK: const(21),
		I2S_WS: const(4),
		I2S_DO: const(14),
		I2S_DI: const(15),
		ENC_L1: const(34),
		ENC_L2: const(35),
		ENC_R1: const(32),
		ENC_R2: const(33),
		POT_L: const(39),
		POT_R: const(36),
		RGB_CLK: const(12),
		RGB_DATA: [5, 2, 26, 13],
		BtnSlot_5: const(6),
		BtnSlot_4: const(3),
		BtnSlot_3: const(2),
		BtnSlot_2: const(1),
		BtnSlot_1: const(0),
		BtnEnc_L: const(5),
		BtnEnc_R: const(4)
	}

	Rev2Map = {
		I2C_SDA: const(22),
		I2C_SCL: const(23),

		I2S_BCK: const(21),
		I2S_WS: const(4),
		I2S_DO: const(14),
		I2S_DI: const(15),

		ENC_L1: const(25),
		ENC_L2: const(26),
		ENC_R1: const(32),
		ENC_R2: const(33),

		POT_L: const(39),
		POT_R: const(36),
		BtnSlot_5: const(4),
		BtnSlot_4: const(3),
		BtnSlot_3: const(2),
		BtnSlot_2: const(1),
		BtnSlot_1: const(0),
		BtnEnc_L: const(15),
		BtnEnc_R: const(14),

		# Schematic footprints had errors in v2.6 which swapped G and B channels for following LEDs:
		# First AW9523 expander (track RGBs)
		LED_B2: const(0),
		LED_B1: const(1),
		LED_R5: const(2),
		LED_R4: const(3),
		LED_R3: const(4),
		LED_R2: const(5),
		LED_R1: const(6),
		LED_G5: const(7),
		LED_B5: const(9),
		LED_B4: const(10),
		LED_B3: const(11),
		LED_G4: const(12),
		LED_G3: const(13),
		LED_G2: const(14),
		LED_G1: const(15),

		# Second AW9523 expander (slot RGBs)
		LED_G9: const(0),
		LED_R9: const(1),
		LED_B9: const(2),
		LED_G8: const(3),
		LED_R8: const(4),
		LED_B8: const(5),
		LED_G7: const(6),
		LED_R7: const(7),
		LED_G10: const(9),
		LED_R10: const(10),
		LED_B10: const(11),
		LED_B7: const(12),
		LED_G6: const(13),
		LED_R6: const(14),
		LED_B6: const(15),

		I2C2_SDA: const(5),
		I2C2_SCL: const(18)
	}

	def __init__(self, revision):
		self.currentMap = None
		if revision == 0:
			print("Rev1")
			self.currentMap = self.Rev1Map
		elif revision == 1:
			print("Rev2")
			self.currentMap = self.Rev2Map
		else:
			print("Unknown revision", revision)

	def get(self, pin: int) -> int | [int]:
		if not pin in self.currentMap:
			print("Pin", pin, "not in map")
			return -1

		return self.currentMap[pin]


class Buttons:
	Slot_5 = const(0)
	Slot_4 = const(1)
	Slot_3 = const(2)
	Slot_2 = const(3)
	Slot_1 = const(4)
	Enc_L = const(5)
	Enc_R = const(6)

	def __init__(self, pins: Pins):
		Buttons.Slot_5 = pins.get(Pins.BtnSlot_5)
		Buttons.Slot_4 = pins.get(Pins.BtnSlot_4)
		Buttons.Slot_3 = pins.get(Pins.BtnSlot_3)
		Buttons.Slot_2 = pins.get(Pins.BtnSlot_2)
		Buttons.Slot_1 = pins.get(Pins.BtnSlot_1)
		Buttons.Enc_L = pins.get(Pins.BtnEnc_L)
		Buttons.Enc_R = pins.get(Pins.BtnEnc_R)

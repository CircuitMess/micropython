from micropython import const


class Pins:
	PIN_BATT = const(6)

	I2C_SDA = const(11)
	I2C_SCL = const(10)

	MOTOR_LEFT_A = const(13)
	MOTOR_LEFT_B = const(12)
	MOTOR_RIGHT_A = const(15)
	MOTOR_RIGHT_B = const(14)

	SERVO_1_PWM = const(16)
	SERVO_2_PWM = const(17)
	SERVO_3_PWM = const(18)

	A_CTRL_1 = const(9)
	A_CTRL_2 = const(8)
	B_CTRL_1 = const(5)
	B_CTRL_2 = const(4)

	# TCA9555 pins:
	TCA_A_ADDR_1 = const(6)
	TCA_A_ADDR_2 = const(5)
	TCA_A_ADDR_3 = const(4)
	TCA_A_ADDR_4 = const(3)
	TCA_A_ADDR_5 = const(2)
	TCA_A_ADDR_6 = const(1)
	TCA_A_DET_1 = const(7)
	TCA_A_DET_2 = const(0)
	TCA_B_ADDR_1 = const(14)
	TCA_B_ADDR_2 = const(13)
	TCA_B_ADDR_3 = const(12)
	TCA_B_ADDR_4 = const(11)
	TCA_B_ADDR_5 = const(10)
	TCA_B_ADDR_6 = const(9)
	TCA_B_DET_1 = const(15)
	TCA_B_DET_2 = const(8)

	EXP_SPKR_EN = const(7)


# Expander button
class Buttons:
	Pair: int = const(6)


class LEDs:
	Camera = const(0)
	Rear = const(1)
	MotorLeft = const(2)
	MotorRight = const(3)
	Arm = const(4)
	HeadlightLeft = const(5)
	HeadlightRight = const(6)
	StatusYellow = const(7)
	StatusGreen = const(8)
	StatusRed = const(9)

	# Maps LEDs to their respective expander pins
	Pins: [int] = const([
		const(0),
		const(5),
		const(12),
		const(8),
		const(9),
		const(10),
		const(11),
		const(13),
		const(14),
		const(15)
	])

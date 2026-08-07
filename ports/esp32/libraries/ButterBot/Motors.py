import time
import ustruct
from machine import I2C, Timer
from micropython import const


class Motor:
	Left = const(0)
	Right = const(1)


class Motors:
	REG_IDENTIFY = 0x00
	REG_RESET = 0x01
	REG_MOTOR_L = 0x02

	# The base board stops both motors if it doesn't receive a motor command within 500ms
	# (dead-man switch), so the current speeds are re-sent every 250ms while any motor is running.
	RESEND_PERIOD = 250

	# Setup time needed between a reset and the following command [ms]
	RESET_DELAY = 200

	def __init__(self, bus: I2C, addr: int = 0x69, timer_id: int = 0):
		self.bus = bus
		self.addr = addr
		self.timer = Timer(timer_id)
		self.__values = [0] * 2

	def begin(self) -> bool:
		try:
			ident = self.bus.readfrom_mem(self.addr, self.REG_IDENTIFY, 1)[0]
		except OSError:
			print("Motor base board not responding on address", self.addr)
			return False

		if ident != self.addr:
			print("Motor base board ID mismatch: expected", self.addr, ", got", ident)
			return False

		self.timer.deinit()
		self.__values = [0, 0]

		# Reset is a bare command byte with no register data
		self.bus.writeto(self.addr, bytes([self.REG_RESET]))
		time.sleep_ms(self.RESET_DELAY)

		return True

	def set(self, motor: int, value: int):
		if motor < 0 or motor >= 2:
			return

		value = min(max(value, -100), 100)
		if value == self.__values[motor]:
			return

		self.__values[motor] = value
		self.__send()

	def get(self, motor: int):
		if motor < 0 or motor >= 2:
			return 0

		return self.__values[motor]

	def set_left(self, value: int):
		self.set(Motor.Left, value)

	def set_right(self, value: int):
		self.set(Motor.Right, value)

	def get_left(self):
		return self.get(Motor.Left)

	def get_right(self):
		return self.get(Motor.Right)

	def set_all(self, val: int | [int] | (int, int)):
		if type(val) == int:
			self.set_all((val, val))
			return

		if type(val) == tuple or type(val) == list:
			if len(val) != 2:
				return

		values = [min(max(v, -100), 100) for v in val]
		if values == self.__values:
			return

		self.__values = values
		self.__send()

	def get_all(self):
		return tuple(self.get(i) for i in range(2))

	def stop_all(self):
		self.set_all((0, 0))

	def __send(self):
		self.__write()

		if self.__values[Motor.Left] == 0 and self.__values[Motor.Right] == 0:
			self.timer.deinit()
		else:
			self.timer.init(mode=Timer.PERIODIC, period=self.RESEND_PERIOD, callback=self.__resend)

	def __resend(self, timer):
		self.__write()

	def __write(self):
		# Motor direction is inverted between the user-facing API and the base board.
		# Both motor registers are written in a single sequential transfer.
		data = ustruct.pack("<bb", -self.__values[Motor.Left], -self.__values[Motor.Right])
		self.bus.writeto_mem(self.addr, self.REG_MOTOR_L, data)

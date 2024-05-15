from micropython import const
from machine import Pin, ADC, I2C

from CircuitOS import PCA95XX
from .AltPressModule import *
from .CO2Sensor import *
from PerseRover.Pins import *


class ModuleType:
	TempHum = const(1)
	Gyro = const(2)
	AltPress = const(3)
	LED = const(4)
	RGB = const(5)
	PhotoRes = const(6)
	Motion = const(7)
	CO2 = const(8)
	Unknown = const(9)


class Modules:
	class Side:
		LEFT = const(0)
		RIGHT = const(1)

	I2CModuleAddress = const(63)

	AddressDict = {
		const(10): ModuleType.LED,
		const(11): ModuleType.RGB,
		const(12): ModuleType.PhotoRes,
		const(13): ModuleType.Motion,
		const(14): ModuleType.CO2
	}

	I2CAddressDict = {
		const(0x38): ModuleType.TempHum,
		const(0x18): ModuleType.Gyro,
		const(0x76): ModuleType.AltPress
	}

	ModuleInstanceDict: dict = {}

	class BusContext:
		def __init__(self, addrPins: [], detPins: [], inserted, current):
			self.addrPins = addrPins
			self.detPins = detPins
			self.inserted = inserted
			self.current = current

	leftContext: BusContext = BusContext(
		[Pins.TCA_A_ADDR_1, Pins.TCA_A_ADDR_2, Pins.TCA_A_ADDR_3, Pins.TCA_A_ADDR_4, Pins.TCA_A_ADDR_5,
		 Pins.TCA_A_ADDR_6],
		[Pins.TCA_A_DET_1, Pins.TCA_A_DET_2], False, ModuleType.Unknown)

	rightContext: BusContext = BusContext(
		[Pins.TCA_B_ADDR_1, Pins.TCA_B_ADDR_2, Pins.TCA_B_ADDR_3, Pins.TCA_B_ADDR_4, Pins.TCA_B_ADDR_5,
		 Pins.TCA_B_ADDR_6],
		[Pins.TCA_B_DET_1, Pins.TCA_B_DET_2], False, ModuleType.Unknown)

	def __init__(self, i2c: I2C, pca9555: PCA95XX):
		self.insert_callback = None
		self.remove_callback = None
		self.i2c = i2c
		self.tca = pca9555
		self.construct_modules()

	def on_insert(self, callback: callable):
		self.insert_callback = callback

	def on_remove(self, callback: callable):
		self.remove_callback = callback

	def get_context(self, side: Side) -> BusContext:
		return self.leftContext if side == self.Side.LEFT else self.rightContext

	def check_inserted(self, bus: Side) -> bool:
		scan = self.tca.state_read()

		context = self.get_context(bus)
		det1: bool = scan & (1 << context.detPins[0])
		det2: bool = scan & (1 << context.detPins[1])
		return det1 == 0 and det2 > 0

	def check_i2c(self, addr: int) -> bool:
		buf = bytearray(1)
		buf[0] = (addr << 1)

		try:
			i = self.i2c.writeto(addr, buf)
		except OSError:
			return False

		if i > 0:
			return True

	def check_addr(self, bus: Side) -> ModuleType:
		scan = self.tca.state_read()

		context = self.get_context(bus)
		addr = 0
		for i in range(6):
			if (scan & (1 << context.addrPins[i])):
				addr |= 1 << i

		if addr != self.I2CModuleAddress:
			if addr not in self.AddressDict:
				return ModuleType.Unknown
			return self.AddressDict.get(addr)

		for addr in self.I2CAddressDict:
			if self.check_i2c(addr):
				return self.I2CAddressDict.get(addr)

		return ModuleType.Unknown

	def bus_check(self, bus: Side):
		now_inserted = self.check_inserted(bus)
		context = self.get_context(bus)

		if context.inserted and not now_inserted:
			context.inserted = False
			removed = context.current
			context.current = ModuleType.Unknown

			self.remove_callback()

			if removed in self.ModuleInstanceDict:
				module: Module = self.ModuleInstanceDict.get(removed)
				module.deinitialize()

		elif not context.inserted and now_inserted:
			context.current = self.check_addr(bus)
			context.inserted = True

			self.insert_callback()

			if context.current in self.ModuleInstanceDict:
				module: Module = self.ModuleInstanceDict.get(context.current)
				module.initialize(bus)

	def update(self):
		self.bus_check(self.Side.LEFT)
		self.bus_check(self.Side.RIGHT)

	def is_inserted(self, type: ModuleType) -> bool:
		if type in self.ModuleInstanceDict:
			module: Module = self.ModuleInstanceDict.get(type)
			return module.inited
		return False

	def construct_modules(self):
		self.altPressModule = AltPressModule(self.i2c)
		self.ModuleInstanceDict[ModuleType.AltPress] = self.altPressModule

		self.CO2Sensor = CO2Sensor()
		self.ModuleInstanceDict[ModuleType.CO2] = self.CO2Sensor

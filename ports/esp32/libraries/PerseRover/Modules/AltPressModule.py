from CircuitOS.Devices.HP203B import HP203B
from .Modules import *
from .Module import *


class AltPressModule(Module):
	Addr = const(0x76)

	def __init__(self, i2c):
		super().__init__()
		self.sensor = HP203B(i2c, self.Addr)

	def _init(self, bus: Modules.Side):
		self.sensor.begin()

	def _deinit(self):
		pass

	def get_pressure(self) -> int:
		return self.sensor.get_baro()

	def get_alt(self) -> int:
		return self.sensor.get_alt()

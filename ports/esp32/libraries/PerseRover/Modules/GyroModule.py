from CircuitOS.Devices.LIS2DW12 import *
from . import _Modules
from .Module import *


class GyroModule(Module):
	Addr = const(0x18)

	def __init__(self, i2c):
		super().__init__()
		self.sensor = LIS2DW12(i2c, self.Addr)

	def _init(self, bus: _Modules.Modules.Side):
		self.sensor.begin()
		self.side = bus

	def _deinit(self):
		pass

	def get_data(self) -> tuple:
		res = self.sensor.get_accel()
		if self.side == _Modules.Modules.Side.LEFT:
			return -res[0], -res[1], res[2]

		return res

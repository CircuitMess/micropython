from CircuitOS.Devices.AHT20 import *
from . import _Modules
from .Module import *


class TempHumModule(Module):
	Addr = const(0x38)

	def __init__(self, i2c):
		super().__init__()
		self.sensor = AHT20(i2c)

	def _init(self, bus: _Modules.Modules.Side):
		self.sensor.begin()

	def _deinit(self):
		pass

	def get_hum(self) -> float:
		return self.sensor.get_hum()

	def get_temp(self) -> float:
		return self.sensor.get_temp()

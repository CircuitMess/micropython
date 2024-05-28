from .Module import *
from . import _Modules
from machine import ADC, Pin
from micropython import const
from PerseRover.Pins import *


class CO2Sensor(Module):
	OKThreshold = const(2100)

	def __init__(self):
		super().__init__()
		self.adc = None

	def _init(self, bus: _Modules.Modules.Side):
		self.adc = ADC(Pin(Pins.A_CTRL_1 if bus == _Modules.Modules.Side.LEFT else Pins.B_CTRL_1, mode=Pin.IN))
		self.adc.atten(ADC.ATTN_11DB)
		self.adc.width(ADC.WIDTH_12BIT)

	def _deinit(self):
		self.adc = None
		pass

	def read(self) -> int:
		return self.adc.read()

	def is_ok(self) -> bool:
		return self.read() < self.OKThreshold

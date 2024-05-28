from . import _Modules
from .Module import *
from machine import Pin, Signal
from PerseRover.Pins import *


class MotionSensor(Module):

	def __init__(self):
		super().__init__()
		self.sensor = None

	def _init(self, bus: _Modules.Modules.Side):
		self.sensor = Signal(Pin(Pins.A_CTRL_1 if bus == _Modules.Modules.Side.LEFT else Pins.B_CTRL_1, mode=Pin.IN))

	def _deinit(self):
		self.sensor = None
		pass

	def read(self) -> bool:
		return self.sensor.value()

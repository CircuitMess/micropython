from . import _Modules
from .Module import *
from machine import Pin, Signal
from PerseRover.Pins import *


class LEDModule(Module):

	def __init__(self):
		super().__init__()
		self.led = None

	def _init(self, bus: _Modules.Modules.Side):
		self.led = Signal(Pin(Pins.A_CTRL_1 if bus == _Modules.Modules.Side.LEFT else Pins.B_CTRL_1, mode=Pin.OUT),
						  invert=True)

	def _deinit(self):
		self.led = None
		pass

	def on(self):
		self.led.on()

	def off(self):
		self.led.off()

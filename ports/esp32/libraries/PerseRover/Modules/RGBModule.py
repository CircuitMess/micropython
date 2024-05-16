from . import _Modules
from .Module import *
from machine import Pin
from neopixel import NeoPixel
from PerseRover.Pins import *


class RGBModule(Module):

	def __init__(self):
		super().__init__()
		self.np = None

	def _init(self, bus: _Modules.Modules.Side):
		self.np = NeoPixel(Pin(Pins.A_CTRL_1 if bus == _Modules.Modules.Side.LEFT else Pins.B_CTRL_1, mode=Pin.OUT), 3)

	def _deinit(self):
		self.np = None
		pass

	def set(self, index: int, r: int, g: int, b: int):
		self.np[index] = (r, g, b)
		self.np.write()

	def set_all(self, r: int, g: int, b: int):
		for i in range(3):
			self.np[i] = (r, g, b)
		self.np.write()

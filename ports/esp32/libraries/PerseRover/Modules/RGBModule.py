from . import _Modules
from .Module import *
from machine import Pin
from neopixel import NeoPixel
from PerseRover.Pins import *


class RGBModule(Module):
	class Index:
		A = 0
		B = 1
		C = 2

	def __init__(self):
		super().__init__()
		self.np = None

	def _init(self, bus: _Modules.Modules.Side):
		self.np = NeoPixel(Pin(Pins.A_CTRL_1 if bus == _Modules.Modules.Side.LEFT else Pins.B_CTRL_1, mode=Pin.OUT), 3)

	def _deinit(self):
		self.np = None
		pass

	def set(self, index: int, r: int, g: int, b: int):
		r = min(100, max(0, r))
		g = min(100, max(0, g))
		b = min(100, max(0, b))
		self.np[index] = (int(float(r) * 255.0 / 100.0), int(float(g) * 255.0 / 100.0), int(float(b) * 255.0 / 100.0))
		self.np.write()

	def set_all(self, r: int, g: int, b: int):
		r = min(100, max(0, r))
		g = min(100, max(0, g))
		b = min(100, max(0, b))
		for i in range(3):
			self.np[i] = (int(float(r) * 255.0 / 100.0), int(float(g) * 255.0 / 100.0), int(float(b) * 255.0 / 100.0))
		self.np.write()

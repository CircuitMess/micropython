from micropython import const
from .Nuvoton import Nuvoton
import ustruct


class Motors:
	BYTE_SET = const(0x30)
	BYTE_GET = const(0x31)

	def __init__(self, nuvo: Nuvoton):
		self.nuvo = nuvo

	def set(self, motor: int, intensity: int):
		if motor > 3:
			return

		intensity = min(127, max(-127, intensity))

		self.nuvo.write([self.BYTE_SET, motor, ustruct.pack("<b", intensity)[0]])

	def get(self, motor: int):
		if motor > 3:
			return 0

		data = self.nuvo.write_read([self.BYTE_GET, motor], 1)
		data = ustruct.unpack("<b", data)

		return data[0]

	def stop(self):
		for i in range(4):
			self.set(i, 0)

from CircuitOS import MatrixOutput
from CircuitOS.Devices.AW9523 import AW9523
from CircuitOS.Devices.ShiftOutput import ShiftOutput


class PixelPin:
	def __init__(self, index: int, pin: int):
		self.index = index
		self.pin = pin


class PixelMapping:
	def __init__(self, pin_r: PixelPin, pin_g: PixelPin, pin_b: PixelPin):
		self.pin_r = pin_r
		self.pin_g = pin_g
		self.pin_b = pin_b


class RGBShiftOutput(MatrixOutput):
	def __init__(self, shift: ShiftOutput, pixel_map: [PixelMapping]):
		super().__init__(10, 1, 2)
		self.output = shift
		self.map = pixel_map

	def init(self):
		self.output.set_all(True)

	def push(self, data):
		state = self.output.state

		for i in range(10):
			""" RGB888 format
			pixel = data[i * 3 : (i + 1) * 3]
			r, g, b = pixel[0], pixel[1], pixel[2]
			"""

			# RGB565 format
			rgb565 = int.from_bytes(data[i * 2:i * 2 + 2], "big")
			r = ((rgb565 >> 11) & 0x1F) << 3
			g = ((rgb565 >> 5) & 0x3F) << 2
			b = (rgb565 & 0x1F) << 3

			pin_r = self.map[i].pin_r
			pin_g = self.map[i].pin_g
			pin_b = self.map[i].pin_b

			state[pin_r.index][pin_r.pin] = r < 128
			state[pin_g.index][pin_g.pin] = g < 128
			state[pin_b.index][pin_b.pin] = b < 128

		self.output.state = state
		self.output.send(state)


class RGBExpanderOutput(MatrixOutput):
	def __init__(self, slotAW: AW9523, trackAW: AW9523, pixel_map: [PixelMapping]):
		super().__init__(10, 1, 2)
		self.slotAW = slotAW
		self.trackAW = trackAW
		self.map = pixel_map

	def init(self):
		for i in range(16):
			self.slotAW.pin_mode(i, AW9523.LED)
			self.slotAW.dim(i, 0)

			self.trackAW.pin_mode(i, AW9523.LED)
			self.trackAW.dim(i, 0)

	def push(self, data: bytearray):
		expanders: [AW9523] = [self.trackAW, self.slotAW]

		for i in range(10):
			# RGB565 format
			rgb565 = int.from_bytes(data[i * 2:i * 2 + 2], "big")
			r = ((rgb565 >> 11) & 0x1F) << 3
			g = ((rgb565 >> 5) & 0x3F) << 2
			b = (rgb565 & 0x1F) << 3

			pin_r = self.map[i].pin_r
			pin_g = self.map[i].pin_g
			pin_b = self.map[i].pin_b

			r_scaled: int = int((r / 255) ** 2 * 255)
			g_scaled: int = int((g / 255) ** 2 * 255)
			b_scaled: int = int((b / 255) ** 2 * 255)

			expanders[pin_r.index].dim(pin_r.pin, r_scaled)
			expanders[pin_g.index].dim(pin_g.pin, g_scaled)
			expanders[pin_b.index].dim(pin_b.pin, b_scaled)

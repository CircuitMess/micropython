from machine import Pin, I2C, ADC
from CircuitOS import InputShift, AW9523, InputPCA95XX, PCA95XX, Encoder, IS31FL3731, MatrixOutputCharlie, Matrix, \
	SliderADC, Encoders, Sliders, Display
from .MatrixMap import *
from .MatrixRGB import *
from .Pins import *
import efuse

revision = efuse.read_rev()

pins = Pins(revision)
btn_pins = Buttons(pins)

enc_l = Encoder(pins.get(Pins.ENC_L1), pins.get(Pins.ENC_L2))
enc_r = Encoder(pins.get(Pins.ENC_R1), pins.get(Pins.ENC_R2))
encoders = Encoders([enc_l, enc_r])

slider_l = SliderADC(pins.get(Pins.POT_L), ADC.WIDTH_10BIT, min=220, max=720, ema_a=0.01, reverse=True)
slider_r = SliderADC(pins.get(Pins.POT_R), ADC.WIDTH_10BIT, min=220, max=720, ema_a=0.01, reverse=True)
sliders = Sliders([slider_l, slider_r])

i2c1 = I2C(0, sda=Pin(pins.get(Pins.I2C_SDA)), scl=Pin(pins.get(Pins.I2C_SCL)))

charlie = IS31FL3731(i2c1)
matrix_out = MatrixOutputCharlie(charlie)
matrix_buf = MatrixOutputBuffered(matrix_out)

if revision == 1:
	i2c2 = I2C(1, sda=Pin(pins.get(Pins.I2C2_SDA)), scl=Pin(pins.get(Pins.I2C2_SCL)))
	expander = PCA95XX(i2c2, 0b0100000)

	buttons = InputPCA95XX(expander)
	for btn in dir(Buttons):
		attr = getattr(Buttons, btn)
		if type(attr) != int:
			continue
		buttons.register_button(attr)

	aw9523_track = AW9523(i2c1, 0x5B)
	aw9523_slot = AW9523(i2c2, 0x5B)

	aw9523_track.begin()
	aw9523_slot.begin()

	aw9523_slot.set_current_limit(3)
	aw9523_track.set_current_limit(3)

	RGB_exp_map = [
		PixelMapping(PixelPin(0, pins.get(Pins.LED_R1)), PixelPin(0, pins.get(Pins.LED_G1)),
					 PixelPin(0, pins.get(Pins.LED_B1))),
		PixelMapping(PixelPin(0, pins.get(Pins.LED_R2)), PixelPin(0, pins.get(Pins.LED_G2)),
					 PixelPin(0, pins.get(Pins.LED_B2))),
		PixelMapping(PixelPin(0, pins.get(Pins.LED_R3)), PixelPin(0, pins.get(Pins.LED_G3)),
					 PixelPin(0, pins.get(Pins.LED_B3))),
		PixelMapping(PixelPin(0, pins.get(Pins.LED_R4)), PixelPin(0, pins.get(Pins.LED_G4)),
					 PixelPin(0, pins.get(Pins.LED_B4))),
		PixelMapping(PixelPin(0, pins.get(Pins.LED_R5)), PixelPin(0, pins.get(Pins.LED_G5)),
					 PixelPin(0, pins.get(Pins.LED_B5))),
		PixelMapping(PixelPin(1, pins.get(Pins.LED_R6)), PixelPin(1, pins.get(Pins.LED_G6)),
					 PixelPin(1, pins.get(Pins.LED_B6))),
		PixelMapping(PixelPin(1, pins.get(Pins.LED_R7)), PixelPin(1, pins.get(Pins.LED_G7)),
					 PixelPin(1, pins.get(Pins.LED_B7))),
		PixelMapping(PixelPin(1, pins.get(Pins.LED_R8)), PixelPin(1, pins.get(Pins.LED_G8)),
					 PixelPin(1, pins.get(Pins.LED_B8))),
		PixelMapping(PixelPin(1, pins.get(Pins.LED_R9)), PixelPin(1, pins.get(Pins.LED_G9)),
					 PixelPin(1, pins.get(Pins.LED_B9))),
		PixelMapping(PixelPin(1, pins.get(Pins.LED_R10)), PixelPin(1, pins.get(Pins.LED_G10)),
					 PixelPin(1, pins.get(Pins.LED_B10)))
	]

	rgb_exp_out = RGBExpanderOutput(aw9523_slot, aw9523_track, RGB_exp_map)
	rgb_exp_out.init()
	rgb_buf = MatrixOutputBuffered(rgb_exp_out)
else:
	buttons = InputShift(pin_data=pins.get(Pins.INP_DATA), pin_clock=pins.get(Pins.INP_SCK),
						 pin_load=pins.get(Pins.INP_PL))
	shift_out = ShiftOutput(pins.get(Pins.RGB_CLK), pins.get(Pins.RGB_DATA))
	rgb_shift_out = RGBShiftOutput(shift_out, RGB_shift_map)
	rgb_buf = MatrixOutputBuffered(rgb_shift_out)

rgb_track = Matrix(TrackRGBOutput(rgb_buf))
rgb_slot = Matrix(SlotRGBOutput(rgb_buf))

matrix_track = Matrix(TrackMatrixOutput(matrix_buf))
matrix_cursor = Matrix(CursorMatrixOutput(matrix_buf))
matrix_sliders = Matrix(SlidersMatrixOutput(matrix_buf))


def begin():
	charlie.init()

	matrix_track.fill(0)
	matrix_cursor.fill(0)
	matrix_sliders.fill(0)
	matrix_track.commit()
	matrix_cursor.commit()
	matrix_sliders.commit()

	rgb_track.fill(0)
	rgb_slot.fill(0)
	rgb_track.commit()
	rgb_slot.commit()

	buttons.scan()
	encoders.scan()
	sliders.scan()

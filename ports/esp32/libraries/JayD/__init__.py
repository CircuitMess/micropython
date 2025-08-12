from machine import Pin, I2C, SPI, Signal
from CircuitOS import Display, PanelST7735, IS31FL3731, MatrixOutputCharlie, Matrix
from .MatrixMap import *
from .Nuvoton import Nuvoton
from .Pins import *
import efuse

revision = efuse.read_rev()

i2c = I2C(0, sda=Pin(Pins.I2C_SDA), scl=Pin(Pins.I2C_SCL), freq=100000)
charlie = IS31FL3731(i2c)
matrix_out = MatrixOutputCharlie(charlie)
matrix_buf = MatrixOutputBuffered(matrix_out)

matrix_big = Matrix(MatrixBig(matrix_buf, revision))
matrix_mid = Matrix(MatrixMid(matrix_buf))
matrix_left = Matrix(MatrixLeft(matrix_buf))
matrix_right = Matrix(MatrixRight(matrix_buf))

spiTFT: SPI = SPI(1, baudrate=27000000, polarity=0, phase=0, sck=Pin(Pins.SPI_SCK), mosi=Pin(Pins.SPI_MOSI),
				  miso=Pin(Pins.SPI_MISO))

if (revision == 2):  # rev3
	panel = PanelST7735(spiTFT, dc=Pin(Pins.TFT_DC, Pin.OUT), reset=Pin(Pins.TFT_RST, Pin.OUT),
						cs=Pin(Pins.TFT_CS, Pin.OUT), rotation=3, color_order_rgb=True)
elif (revision == 1):  # rev2
	panel = PanelST7735(spiTFT, dc=Pin(Pins.TFT_DC, Pin.OUT), reset=Pin(Pins.TFT_RST, Pin.OUT),
						cs=Pin(Pins.TFT_CS, Pin.OUT), rotation=1, color_order_rgb=True)
else:  # rev1
	panel = PanelST7735(spiTFT, dc=Pin(Pins.TFT_DC, Pin.OUT), reset=Pin(Pins.TFT_RST, Pin.OUT),
						cs=Pin(Pins.TFT_CS, Pin.OUT), rotation=1)
display = Display(panel)

blPin = Pin(Pins.BL, mode=Pin.OUT, value=True)
backlight = Signal(blPin, invert=True)

input = Nuvoton(i2c, revision)


def begin():
	charlie.init()

	matrix_big.fill(0)
	matrix_mid.fill(0)
	matrix_left.fill(0)
	matrix_right.fill(0)

	matrix_big.commit()
	matrix_mid.commit()
	matrix_left.commit()
	matrix_right.commit()

	input.begin()
	input.scan()

	panel.init()

	# Can't set TFT offset before this, since panel.init() resets it to default
	if (revision == 2 or revision == 1):
		panel.tft.offset(1, 2)

	display.fill(display.Color.Black)
	display.commit()

	backlight.on()

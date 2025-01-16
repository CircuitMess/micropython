from machine import SPI, Pin, Signal, I2C
from CircuitOS import Display, PanelST7735, PCA95XX, ADS1015, SliderADS1015, Sliders
from .Pins import *
from .Buttons import *

spi: SPI = SPI(1, baudrate=27000000, polarity=0, phase=0, sck=Pin(Pins.SPI_SCK), mosi=Pin(Pins.SPI_MOSI), miso=Pin(Pins.SPI_MISO))
panel = PanelST7735(spi, dc=Pin(Pins.TFT_DC, Pin.OUT), reset=Pin(Pins.TFT_RST, Pin.OUT), cs=Pin(Pins.TFT_CS, Pin.OUT), rotation=1)
blPin = Pin(Pins.BL, mode=Pin.OUT, value=True)
backlight = Signal(blPin, invert=True)

i2c = I2C(0, sda=Pin(Pins.I2C_SDA, Pin.OUT), scl=Pin(Pins.I2C_SCL, Pin.OUT))
expander = PCA95XX(i2c)
ads1015 = ADS1015(i2c)
buttons = ButtonInput(expander, ads1015)

joystick_x = SliderADS1015(ads1015, Pins.JOY_H, 0, 1080)
joystick_y = SliderADS1015(ads1015, Pins.JOY_V, 0, 1080)
joystick = Sliders([joystick_x, joystick_y])

display = Display(panel)


def begin():
	panel.init()
	display.fill(display.Color.Black)
	display.commit()

	backlight.on()

	buttons.scan()
	joystick.scan()

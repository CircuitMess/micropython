from machine import SPI, Pin, Signal, ADC
from CircuitOS import InputGPIO, Display, PanelST7735_128x128, SliderADC, Sliders
from .Pins import *
from ._LED import LED

pins = Pins(0)
btn_pins = Buttons(pins)
led_pins = LEDs(pins)

spiTFT: SPI = SPI(1, baudrate=40000000, polarity=0, phase=0, sck=Pin(pins.get(Pins.TFT_SCK)),
				  mosi=Pin(pins.get(Pins.TFT_SDA)))

blPin = Pin(pins.get(Pins.LED_BACKLIGHT), mode=Pin.OUT, value=True)
backlight = Signal(blPin, invert=True)

# GPIO19 high injects the 2.5V calibration reference onto the battery ADC node - keep it off
vref = Pin(pins.get(Pins.PIN_VREF), mode=Pin.OUT, value=False)

buttons = InputGPIO(btn_pins.get_pins_array(), inverted=True)

joystick_x = SliderADC(pins.get(Pins.JOY_H), min=0, max=4096, ema_a=0.05, width=ADC.WIDTH_12BIT)
joystick_y = SliderADC(pins.get(Pins.JOY_V), min=0, max=4096, ema_a=0.05, width=ADC.WIDTH_12BIT)
joystick = Sliders([joystick_x, joystick_y])

leds = LED(led_pins.pins)

dc = Pin(pins.get(Pins.TFT_DC), Pin.OUT)
reset = Pin(pins.get(Pins.TFT_RST), Pin.OUT)
panel = PanelST7735_128x128(spiTFT, dc=dc, reset=reset, rotation=0,
							rotations=[(0x00, 128, 128, 0, 0)])
display = Display(panel)


def begin():
	panel.init()

	display.fill(Display.Color.Black)
	display.commit()

	backlight.on()

	buttons.scan()
	joystick.scan()
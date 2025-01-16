from ST7735 import TFT
from machine import SPI, Pin, Signal, I2C, ADC
from CircuitOS import InputGPIO, Display, PanelST7735_128x128, SliderADC, Sliders, Encoder, Encoders, AW9523
from .Pins import *
from ._LED import LED

spiTFT: SPI = SPI(1, baudrate=27000000, polarity=0, phase=0, sck=Pin(Pins.TFT_SCK), mosi=Pin(Pins.TFT_MOSI))

blPin = Pin(Pins.BL, mode=Pin.OUT, value=True)
backlight = Signal(blPin, invert=True)

buttons = InputGPIO(Buttons.Pins, inverted=True)

enc_cam = Encoder(Pins.ENC_CAM_A, Pins.ENC_CAM_B)
enc_arm = Encoder(Pins.ENC_ARM_A, Pins.ENC_ARM_B)
enc_pinch = Encoder(Pins.ENC_PINCH_A, Pins.ENC_PINCH_B)
encoders = Encoders([enc_cam, enc_arm, enc_pinch])

pot_qual = SliderADC(Pins.POT_QUAL, min=0, max=4096, ema_a=0.05, reverse=False, width=ADC.WIDTH_12BIT)
joystick_x = SliderADC(Pins.JOY_H, min=0, max=4096, ema_a=0.05, reverse=False, width=ADC.WIDTH_12BIT)
joystick_y = SliderADC(Pins.JOY_V, min=0, max=4096, ema_a=0.05, reverse=False, width=ADC.WIDTH_12BIT)
potentiometers = Sliders([pot_qual, joystick_x, joystick_y])

i2c = I2C(0, sda=Pin(Pins.I2C_SDA), scl=Pin(Pins.I2C_SCL))
aw9523 = AW9523(i2c, 0x5b)
leds = LED(aw9523)  # LED does the initialization of AW9523

dc = Pin(Pins.TFT_DC, Pin.OUT)
reset = Pin(Pins.TFT_RST, Pin.OUT)
panel = PanelST7735_128x128(spiTFT, dc=dc, reset=reset, rotation=2)
display = Display(panel)


def begin():
    panel.init()

    display.fill(Display.Color.Black)
    display.commit()

    backlight.on()

    buttons.scan()
    encoders.scan()
    potentiometers.scan()

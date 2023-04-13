from ST7735 import TFT
from machine import SPI, Pin, Signal, I2C
from CircuitOS import InputGPIO, Display
from .Pins import *
from .Nuvoton import *
from .WheelsonMotors import *
from .WheelsonLED import *
from .WheelsonInput import *

spiTFT: SPI = SPI(1, baudrate=27000000, polarity=0, phase=0, sck=Pin(Pins.TFT_SCK), mosi=Pin(Pins.TFT_MOSI))
tft = TFT(spiTFT, aDC=Pins.TFT_DC, aReset=Pins.TFT_RST, aCS=Pins.TFT_CS)

display = Display(tft, 160, 128)
i2c = I2C(0, sda=Pin(Pins.I2C_SDA), scl=Pin(Pins.I2C_SCL))
nuvo = NuvotonInterface(i2c)
Motors = MotorControl(i2c)
LED = LEDControl(i2c)
buttons = WheelInput(i2c)


def begin():
    tft.initr()
    tft.rotation(1)
    tft.rgb(False)

    display.fill(display.Color.Black)
    display.commit()

    nuvo.begin()
    LED.setBacklight(True)

    buttons.scan()

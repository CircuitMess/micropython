from CircuitOS import AW9523, SingleLED
from .Pins import *


class LED:

    def __init__(self, aw9523: AW9523):
        self.aw9523 = aw9523
        self.expanderPins = [
            LEDs.CamL4,
            LEDs.CamL3,
            LEDs.CamL2,
            LEDs.CamL1,
            LEDs.CamCenter,
            LEDs.CamR1,
            LEDs.CamR2,
            LEDs.CamR3,
            LEDs.CamR4,
            LEDs.Warning,
            LEDs.Arm,
            LEDs.ArmUp,
            LEDs.ArmDown,
            LEDs.Light,
            LEDs.PinchOpen,
            LEDs.PinchClose
        ]

        self.gpioPins = [
            LEDs.Power,
            LEDs.Pair,
            LEDs.PanicL,
            LEDs.PanicR
        ]

        self.gpioLeds = [SingleLED(LEDs.Pins[pin]) for pin in self.gpioPins]

        self.aw9523.begin()
        self.aw9523.set_current_limit(3)  # Imax / 4
        for pin in self.expanderPins:
            self.aw9523.pin_mode(LEDs.Pins[pin], AW9523.LED)
            self.aw9523.dim(LEDs.Pins[pin], 0)

        for led in self.gpioLeds:
            led.set(0)

    def set(self, pin: int, value: int):
        """
        @param pin: pin from LEDs
        @param value: value from 0 to 100
        @return:
        """
        value = min(max(value, 0), 100)

        if pin in self.expanderPins:
            scaled = float(value) / 100
            scaled = scaled * scaled
            scaled = scaled * 255
            self.aw9523.dim(LEDs.Pins[pin], int(scaled))
        elif pin in self.gpioPins:
            self.gpioLeds[pin].set(value)
        else:
            return

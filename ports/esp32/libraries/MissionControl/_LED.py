from CircuitOS import AW9523, SingleLED
from .Pins import *


class LED:

    def __init__(self, aw9523: AW9523):
        self.aw9523 = aw9523
        self.expanderPins = {
            LEDs.CamL4: 0x10,
            LEDs.CamL3: 0x10,
            LEDs.CamL2: 0x10,
            LEDs.CamL1: 0x10,
            LEDs.CamCenter: 0x10,
            LEDs.CamR1: 0x10,
            LEDs.CamR2: 0x10,
            LEDs.CamR3: 0x10,
            LEDs.CamR4: 0x10,
            LEDs.Warning: 0x10,
            LEDs.Arm: 0x10,
            LEDs.ArmUp: 0x10,
            LEDs.ArmDown: 0x10,
            LEDs.Light: 0x10,
            LEDs.PinchOpen: 0x10,
            LEDs.PinchClose: 0x10,
        }

        self.gpioPins = {
            LEDs.Power: 150,
            LEDs.Pair: 150,
            LEDs.PanicL: 150,
            LEDs.PanicR: 150,
        }

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
        @param value: value from 0 to 255
        @return:
        """
        if pin in self.expanderPins:
            self.aw9523.dim(LEDs.Pins[pin], self.constrain_value(value, self.expanderPins[pin]))
        elif pin in self.gpioPins:
            constrained = float(self.constrain_value(value, self.gpioPins[pin])) * 100.0 / 255.0
            self.gpioLeds[pin].set(int(constrained))
        else:
            return

    def constrain_value(self, value: int, limit: int) -> int:
        percent: float = max(min(1.0 * ((float(value) * float(limit)) / float(0xFF)) / float(limit), 1.0), 0.0)
        return int(percent * percent * float(limit))

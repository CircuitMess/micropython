from machine import Pin, ADC
from CircuitOS.Devices import ADS1015


class Slider:
    def __init__(self, min: int = 0, max: int = 1024, ema_a: float = 0, reverse: bool = False):
        self.min = min
        self.max = max
        self.ema_a = ema_a
        self.reverse = reverse

        self.val = -1
        self.last_called_val = -1

        self._on_move = None

    def on_move(self, on_move: callable) -> None:
        self._on_move = on_move
        self.last_called_val = self.val

    def get(self):
        return round(self.val)

    def scan(self) -> None:
        mapped_value = self._read()

        if self.val == -1:
            self.val = mapped_value
            self.last_called_val = mapped_value
            return

        if self.ema_a != 0:
            self.val = self.ema_a * mapped_value + (1 - self.ema_a) * self.val
        else:
            self.val = mapped_value

        if self._on_move and (self.last_called_val is None or round(self.last_called_val) != round(self.val)):
            self._on_move(round(self.val))
            self.last_called_val = self.val

    def _raw_read(self) -> int:
        pass

    def _read(self) -> float:
        raw_value = self._raw_read()
        mapped_value = self.map_value(raw_value)
        if self.reverse:
            mapped_value = 100 - mapped_value
        return mapped_value

    def map_value(self, x: int) -> float:
        x = max(self.min, min(self.max, x))
        return (x - self.min) * 100.0 / (self.max - self.min)


class SliderADC(Slider):

    def __init__(self, pin: int, width: int, min: int = 0, max: int = 1024, ema_a: float = 0, reverse: bool = False):
        super().__init__(min, max, ema_a, reverse)
        self.pin = Pin(pin, mode=Pin.IN)
        self.adc = ADC(self.pin)
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(width)

    def _raw_read(self) -> int:
        return self.adc.read()

class SliderADS1015(Slider):

        def __init__(self, ads: ADS1015, channel: int, min: int = 0, max: int = 1024, ema_a: float = 0, reverse: bool = False):
            super().__init__(min, max, ema_a, reverse)
            self.ads = ads
            self.pin = channel

        def _raw_read(self) -> int:
            self.ads.read(self.pin)
            return self.ads.read(self.pin)



class Sliders:

    def __init__(self, sliders: [Slider]):
        self.sliders = sliders

    def on_move(self, i: int, listener: callable):
        if i < 0 or i >= len(self.sliders):
            return

        self.sliders[i].on_move(listener)

    def get(self, i: int):
        if i < 0 or i >= len(self.sliders):
            return 0

        return self.sliders[i].get()

    def scan(self):
        for slider in self.sliders:
            slider.scan()

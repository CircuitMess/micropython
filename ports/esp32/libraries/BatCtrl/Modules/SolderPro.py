from CircuitOS import AW9523
import time


class SolderPro:
    def __init__(self, i2c, address=0x5B):
        self.aw9523 = AW9523(i2c, address)
        self.num_buttons = 4
        self.button_pins = [i for i in range(11, 7, -1)]
        self.led_pins = [0, 1, 6, 7, 12, 13, 14, 15]
        self.control_pins = [i for i in range(6)]

        self.state = [False] * self.num_buttons
        self.on_press = [None] * self.num_buttons
        self.on_release = [None] * self.num_buttons

    def begin(self):
        if not self.aw9523.begin():
            return False

        for pin in self.button_pins:
            self.aw9523.pinMode(pin, AW9523.IN)

        for pin in self.led_pins:
            self.aw9523.pinMode(pin, AW9523.LED)

        return True

    def set_pin(self, pin, value):
        if pin not in self.control_pins:
            return
        self.aw9523.write(pin, value)

    def set_pin_mode(self, pin, mode):
        if pin not in self.control_pins:
            return
        self.aw9523.pinMode(pin, mode)

    def get_button(self, i):
        if i >= self.num_buttons:
            return False
        return self.state[i]

    def set_led(self, index, value):
        if index in self.led_pins:
            self.aw9523.dim(index, value)

    def on_press(self, i, callback):
        if i < self.num_buttons:
            self.on_press[i] = callback

    def on_release(self, i, callback):
        if i < self.num_buttons:
            self.on_release[i] = callback

    async def loop(self):
        while True:
            self.scan_buttons()
            await time.sleep_ms(1)

    def scan_buttons(self):
        state = []

        for pin in self.button_pins:
            state.append(not self.aw9523.read(pin))

        for i, s in enumerate(state):
            if s == 1:
                self.pressed(i)
            else:
                self.released(i)

    def pressed(self, i):
        if i < self.num_buttons:
            old = self.state[i]
            self.state[i] = True

            if old != self.state[i] and self.on_press[i] is not None:
                self.on_press[i]()

    def released(self, i):
        if i < self.num_buttons:
            old = self.state[i]
            self.state[i] = False

            if old != self.state[i] and self.on_release[i] is not None:
                self.on_release[i]()

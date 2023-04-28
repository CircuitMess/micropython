from machine import I2C
import time


class AW9523:
    DEFAULT_ADDR = 0x58

    IN, OUT, LED = range(3)
    IMAX, IMAX_3Q, IMAX_2Q, IMAX_1Q = range(4)

    def __init__(self, i2c: I2C, address: int = DEFAULT_ADDR):
        self._i2c = i2c
        self._addr = address
        self._regs = {
            'conf': 0,
            'dir': [0, 0],
            'output': [0, 0],
            'intr': [0, 0],
            'mode': [0xff, 0xff],
            'dim': [0] * 16
        }
        self._dimmap = [4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 12, 13, 14, 15]

    def _write_reg(self, reg, data):
        buf = bytearray([reg]) + data
        self._i2c.writeto(self._addr, buf)

    def _read_reg(self, reg):
        self._i2c.writeto(self._addr, bytearray([reg]))
        return self._i2c.readfrom(self._addr, 1)[0]

    def begin(self):
        try:
            self.reset()
            return self._read_reg(0x10) == 0x23
        except OSError:
            return False

    def reset(self):
        self._write_reg(0x7F, bytearray([0x00]))
        self._regs = {
            'conf': 0,
            'dir': [0, 0],
            'output': [0, 0],
            'intr': [0, 0],
            'mode': [0xff, 0xff],
            'dim': [0] * 16
        }
        time.sleep_us(50)

    def pinMode(self, pin, mode):
        if pin >= 16:
            return

        it = 0 if pin <= 7 else 1
        mask = 1 << (pin if pin <= 7 else pin - 8)
        regDir = 0x04 + it
        regMode = 0x12 + it

        if mode == self.LED:
            self._regs['mode'][it] &= ~mask
            self._write_reg(regMode, bytearray([self._regs['mode'][it]]))
        else:
            self._regs['mode'][it] |= mask
            self._write_reg(regMode, bytearray([self._regs['mode'][it]]))

            if mode == self.OUT:
                self._regs['dir'][it] &= ~mask
            else:
                self._regs['dir'][it] |= mask

            self._write_reg(regDir, bytearray([self._regs['dir'][it]]))

    def read(self, pin):
        if pin >= 16:
            return False

        reg = (0x00 if pin <= 7 else 0x01)
        return (self._read_reg(reg) & (1 << (pin if pin <= 7 else pin - 8))) != 0

    def write(self, pin, state):
        if pin >= 16:
            return

        it = 0 if pin <= 7 else 1
        mask = 1 << (pin if pin <= 7 else pin - 8)
        reg = 0x02 + it
        if state:
            self._regs['output'][it] |= mask
        else:
            self._regs['output'][it] &= ~mask

        self._write_reg(reg, bytearray([self._regs['output'][it]]))

    def dim(self, pin, factor):
        if pin >= 16:
            return

        pin = self._dimmap[pin]
        self._regs['dim'][pin] = factor
        self._write_reg(0x20 + pin, bytearray([factor]))

    def setInterrupt(self, pin, enabled):
        if pin >= 16:
            return

        it = 0 if pin <= 7 else 1
        mask = 1 << (pin if pin <= 7 else pin - 8)
        reg = 0x06 + it

        if enabled:
            self._regs['intr'][it] |= mask
        else:
            self._regs['intr'][it] &= ~mask

        self._write_reg(reg, bytearray([self._regs['intr'][it]]))

    def setCurrentLimit(self, limit):
        mask = 0b00000011
        self._regs['conf'] = (self._regs['conf'] & ~mask) | (limit & mask)
        self._write_reg(0x11, bytearray([self._regs['conf'] & 0b00010011]))

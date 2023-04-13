from machine import Pin, I2C
import time
from .Nuvoton import WSNV_ADDR

MOTOR_SET_BYTE = 0x30
MOTOR_GET_BYTE = 0x31


class MotorControl:
    def __init__(self, i2c):
        self.i2c = i2c
        self.state = [0, 0, 0, 0]

    def setMotor(self, id, intensity):
        if id > 3:
            return
        if self.state[id] == intensity:
            return
        if intensity <= -128:
            intensity = -127
        self.state[id] = intensity
        msg = bytearray([MOTOR_SET_BYTE, id, int(intensity)])
        self.i2c.writeto(WSNV_ADDR, msg)

    def getMotor(self, id):
        if id > 3:
            return 0
        msg = bytearray([MOTOR_GET_BYTE, id])
        self.i2c.writeto(WSNV_ADDR, msg)
        time.sleep_ms(1)
        data = bytearray(1)
        self.i2c.readfrom_into(WSNV_ADDR, data)
        self.state[id] = data[0]
        return (self.state[id])

    def stopAll(self):
        for i in range(4):
            self.setMotor(i, 0)

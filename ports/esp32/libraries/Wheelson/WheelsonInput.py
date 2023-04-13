from CircuitOS import Input
from micropython import const
from .Nuvoton import WSNV_ADDR

GET_NUM_EVENTS_BYTE = const(0x40)
GET_EVENTS_BYTE = const(0x41)
NUM_BUTTONS = const(6)


class WheelInput(Input):
    def __init__(self, i2c):
        super().__init__(NUM_BUTTONS)
        self.i2c = i2c

    def get_num_events(self):
        self.i2c.writeto(WSNV_ADDR, bytes([GET_NUM_EVENTS_BYTE]))
        num_events = self.i2c.readfrom(WSNV_ADDR, 1)
        return num_events[0]

    def scan(self):
        num_events = self.get_num_events()
        if num_events == 0:
            return
        self.handle_events(num_events)

    def handle_events(self, num_events):
        msg = bytearray([GET_EVENTS_BYTE, num_events])
        data = bytearray(num_events)
        self.i2c.writeto(WSNV_ADDR, msg)
        self.i2c.readfrom_into(WSNV_ADDR, data)
        for event in data:
            event_id = event & 0x7F
            state = event >> 7
            self.handle_single_event(event_id, state)

    def handle_single_event(self, event_id, state):
        if state:
            self.pressed(event_id)
        else:
            self.released(event_id)

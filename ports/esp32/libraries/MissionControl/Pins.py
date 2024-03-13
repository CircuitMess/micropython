from micropython import const


class Pins:
    BL: int = const(39)
    BATT: int = const(9)

    TFT_SCK: int = const(40)
    TFT_MOSI: int = const(41)
    TFT_DC: int = const(42)
    TFT_RST: int = const(43)

    I2C_SDA: int = const(15)
    I2C_SCL: int = const(16)

    POT_QUAL: int = const(8)
    JOY_H: int = const(2)
    JOY_V: int = const(1)

    ENC_CAM_A: int = const(38)
    ENC_CAM_B: int = const(36)
    ENC_ARM_A: int = const(10)
    ENC_ARM_B: int = const(12)
    ENC_PINCH_A: int = const(5)
    ENC_PINCH_B: int = const(7)


class Buttons:
    Pair: int = const(0)
    Panic: int = const(1)
    Joystick: int = const(2)
    CamEncoder: int = const(3)
    ArmEncoder: int = const(4)
    PinchEncoder: int = const(5)
    SwitchArm: int = const(6)
    SwitchLight: int = const(7)

    # Maps Buttons [0-3] to their respective GPIO pins
    Pins: [int] = const([
        const(35),
        const(14),
        const(13),
        const(37),
        const(11),
        const(6),
        const(4),
        const(44)
    ])


class LEDs:
    # GPIO pins
    Power: int = const(0)
    Pair: int = const(1)
    PanicL: int = const(2)
    PanicR: int = const(3)

    # Expander pins
    Warning: int = const(4)
    Arm: int = const(5)
    Light: int = const(6)
    ArmUp: int = const(7)
    ArmDown: int = const(8)
    PinchOpen: int = const(9)
    PinchClose: int = const(10)

    CamCenter: int = const(11)
    CamL1: int = const(12)
    CamL2: int = const(13)
    CamL3: int = const(14)
    CamL4: int = const(15)
    CamR1: int = const(16)
    CamR2: int = const(17)
    CamR3: int = const(18)
    CamR4: int = const(19)

    # Maps LEDs to their respective GPIO or expander pins
    Pins: [int] = const([
        const(17),
        const(34),
        const(33),
        const(18),

        const(1),
        const(9),
        const(15),
        const(11),
        const(0),
        const(8),
        const(10),

        const(6),
        const(5),
        const(4),
        const(3),
        const(2),
        const(14),
        const(13),
        const(12),
        const(7)
    ])

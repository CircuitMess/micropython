#define MICROPY_HW_BOARD_NAME "CircuitMess Butter Bot Controller"
#define MICROPY_HW_MCU_NAME "ESP32S3"

#define MICROPY_PY_MACHINE_DAC              (0)

// Enable UART REPL for modules that have an external USB-UART and don't use native USB. - set to 1 to enable
// Butter Bot Controller has no native USB (GPIO19/D- is used as the battery calibration
// reference); its USB-C routes through an onboard CH340 to UART0.
#define MICROPY_HW_ENABLE_UART_REPL         (1)
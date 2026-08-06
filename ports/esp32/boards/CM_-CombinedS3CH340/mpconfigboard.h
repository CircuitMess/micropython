#define MICROPY_HW_BOARD_NAME "CircuitMess ESP32S3 CH340 Devices"
#define MICROPY_HW_MCU_NAME "ESP32S3"

#define MICROPY_PY_MACHINE_DAC              (0)

// Enable UART REPL for modules that have an external USB-UART and don't use native USB. - set to 1 to enable
// These devices route USB-C through an onboard CH340 to UART0; the S3's native USB pins
// (GPIO19/20) are repurposed as regular GPIOs.
#define MICROPY_HW_ENABLE_UART_REPL         (1)

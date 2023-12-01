LD_FILES = boards/esp8266_2MiB.ld

MICROPY_PY_BTREE ?= 1
MICROPY_VFS_FAT ?= 1
MICROPY_VFS_LFS2 ?= 1

FROZEN_MANIFEST ?= $(BOARD_DIR)/manifest.py

CFLAGS += -DMICROPY_ESP8266_2M
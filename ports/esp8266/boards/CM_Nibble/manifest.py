# base modules
include("$(PORT_DIR)/boards/manifest.py")

package("Nibble", base_path="$(PORT_DIR)/libraries")

# asyncio
include("$(MPY_DIR)/extmod/asyncio")

# drivers
require("ssd1306")

# micropython-lib: file utilities
require("upysh")

# micropython-lib: requests
require("urequests")
require("urllib.urequest")

# micropython-lib: umqtt
require("umqtt.simple")
require("umqtt.robust")

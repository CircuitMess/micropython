from machine import I2C
import time
from micropython import const
from uasyncio import sleep_ms
import uctypes

'''
Library for the ADS1015 ADC (https:#www.ti.com/lit/ds/symlink/ads1015.pdf)
'''


class ADS1015:
	ADDR = const(0x48)

	# POINTER REGISTER
	ADS1015_REG_POINTER_MASK = const(0x03)
	ADS1015_REG_POINTER_CONVERT = const(0x00)
	ADS1015_REG_POINTER_CONFIG = const(0x01)
	ADS1015_REG_POINTER_LOWTHRESH = const(0x02)
	ADS1015_REG_POINTER_HITHRESH = const(0x03)

	# CONFIG	REGISTER
	ADS1015_REG_CONFIG_OS_MASK = const(0x8000)
	ADS1015_REG_CONFIG_OS_SINGLE = const(0x8000)  # Write: Set to start a single-conversion
	ADS1015_REG_CONFIG_OS_BUSY = const(0x0000)  # Read: Bit = 0 when conversion is in progress
	ADS1015_REG_CONFIG_OS_NOTBUSY = const(0x8000)  # Read: Bit = 1 when device is not performing a conversion

	ADS1015_REG_CONFIG_MUX_MASK = const(0x7000)
	ADS1015_REG_CONFIG_MUX_DIFF_0_1 = const(0x0000)  # Differential P = AIN0, N = AIN1 (default)
	ADS1015_REG_CONFIG_MUX_DIFF_0_3 = const(0x1000)  # Differential P = AIN0, N = AIN3
	ADS1015_REG_CONFIG_MUX_DIFF_1_3 = const(0x2000)  # Differential P = AIN1, N = AIN3
	ADS1015_REG_CONFIG_MUX_DIFF_2_3 = const(0x3000)  # Differential P = AIN2, N = AIN3
	ADS1015_REG_CONFIG_MUX_SINGLE_0 = const(0x4000)  # Single-ended AIN0
	ADS1015_REG_CONFIG_MUX_SINGLE_1 = const(0x5000)  # Single-ended AIN1
	ADS1015_REG_CONFIG_MUX_SINGLE_2 = const(0x6000)  # Single-ended AIN2
	ADS1015_REG_CONFIG_MUX_SINGLE_3 = const(0x7000)  # Single-ended AIN3

	ADS1015_REG_CONFIG_PGA_MASK = const(0x0E00)
	ADS1015_REG_CONFIG_PGA_6_144V = const(0x0000)  # +/-6.144V range = Gain 2/3
	ADS1015_REG_CONFIG_PGA_4_096V = const(0x0200)  # +/-4.096V range = Gain 1
	ADS1015_REG_CONFIG_PGA_2_048V = const(0x0400)  # +/-2.048V range = Gain 2 (default)
	ADS1015_REG_CONFIG_PGA_1_024V = const(0x0600)  # +/-1.024V range = Gain 4
	ADS1015_REG_CONFIG_PGA_0_512V = const(0x0800)  # +/-0.512V range = Gain 8
	ADS1015_REG_CONFIG_PGA_0_256V = const(0x0A00)  # +/-0.256V range = Gain 16

	ADS1015_REG_CONFIG_MODE_MASK = const(0x0100)
	ADS1015_REG_CONFIG_MODE_CONTIN = const(0x0000)  # Continuous conversion mode
	ADS1015_REG_CONFIG_MODE_SINGLE = const(0x0100)  # Power-down single-shot mode (default)

	ADS1015_REG_CONFIG_DR_MASK = const(0x00E0)
	ADS1015_REG_CONFIG_DR_128SPS = const(0x0000)  # 128 samples per second
	ADS1015_REG_CONFIG_DR_250SPS = const(0x0020)  # 250 samples per second
	ADS1015_REG_CONFIG_DR_490SPS = const(0x0040)  # 490 samples per second
	ADS1015_REG_CONFIG_DR_920SPS = const(0x0060)  # 920 samples per second
	ADS1015_REG_CONFIG_DR_1600SPS = const(0x0080)  # 1600 samples per second (default)
	ADS1015_REG_CONFIG_DR_2400SPS = const(0x00A0)  # 2400 samples per second
	ADS1015_REG_CONFIG_DR_3300SPS = const(0x00C0)  # 3300 samples per second

	ADS1015_REG_CONFIG_CMODE_MASK = const(0x0010)
	ADS1015_REG_CONFIG_CMODE_TRAD = const(0x0000)  # Traditional comparator with hysteresis (default)
	ADS1015_REG_CONFIG_CMODE_WINDOW = const(0x0010)  # Window comparator

	ADS1015_REG_CONFIG_CPOL_MASK = const(0x0008)
	ADS1015_REG_CONFIG_CPOL_ACTVLOW = const(0x0000)  # ALERT/RDY pin is low when active (default)
	ADS1015_REG_CONFIG_CPOL_ACTVHI = const(0x0008)  # ALERT/RDY pin is high when active

	ADS1015_REG_CONFIG_CLAT_MASK = const(0x0004)  # Determines if ALERT/RDY pin latches once asserted
	ADS1015_REG_CONFIG_CLAT_NONLAT = const(0x0000)  # Non-latching comparator (default)
	ADS1015_REG_CONFIG_CLAT_LATCH = const(0x0004)  # Latching comparator

	ADS1015_REG_CONFIG_CQUE_MASK = const(0x0003)
	ADS1015_REG_CONFIG_CQUE_1CONV = const(0x0000)  # Assert ALERT/RDY after one conversions
	ADS1015_REG_CONFIG_CQUE_2CONV = const(0x0001)  # Assert ALERT/RDY after two conversions
	ADS1015_REG_CONFIG_CQUE_4CONV = const(0x0002)  # Assert ALERT/RDY after four conversions
	ADS1015_REG_CONFIG_CQUE_NONE = const(0x0003)  # Disable the comparator and put ALERT/RDY in high state (default)

	# CONVERSION	DELAY( in mS)
	ADS1015_CONVERSIONDELAY = const(1)

	class AdsGain:
		GAIN_TWOTHIRDS = const(0x0000)  # ADS1015_REG_CONFIG_PGA_6_144V,
		GAIN_ONE = const(0x0200)  # ADS1015_REG_CONFIG_PGA_4_096V,
		GAIN_TWO = const(0x0400)  # ADS1015_REG_CONFIG_PGA_2_048V,
		GAIN_FOUR = const(0x0600)  # ADS1015_REG_CONFIG_PGA_1_024V,
		GAIN_EIGHT = const(0x0800)  # ADS1015_REG_CONFIG_PGA_0_512V,
		GAIN_SIXTEEN = const(0x0A00)  # ADS1015_REG_CONFIG_PGA_0_256V

	def __init__(self, i2c: I2C, addr: int = ADDR):
		self._i2c = i2c
		self._addr = addr
		self._conversionDelay = self.ADS1015_CONVERSIONDELAY * 10
		self._bitShift = 4  # 12-bit ADC
		self._gain = self.AdsGain.GAIN_TWOTHIRDS  # +/- 6.144V range (limited to VDD +0.3V max!)

	def begin(self) -> bool:
		try:
			self._i2c.writeto(self._addr, bytearray([0x00]))
			self.read(0)
			return True
		except OSError:
			return False

	def read(self, channel: int) -> int:
		# print("ADS read on channel ", channel)
		if channel > 3:
			print("Invalid channel, must be 0-3")
			return 0

		config = 0 | uctypes.UINT16

		config |= (self.ADS1015_REG_CONFIG_CQUE_NONE |  # Disable the comparator (default val)
				   self.ADS1015_REG_CONFIG_CLAT_NONLAT |  # Non-latching (default val)
				   self.ADS1015_REG_CONFIG_CPOL_ACTVLOW |  # Alert / Rdy active low   (default val)
				   self.ADS1015_REG_CONFIG_CMODE_TRAD |  # Traditional comparator (default val)
				   self.ADS1015_REG_CONFIG_DR_1600SPS |  # 1600 samples per second (default)
				   self.ADS1015_REG_CONFIG_MODE_SINGLE)  # Single-shot mode (default)

		# Set PGA / voltage range
		config |= self._gain

		# Set single-ended input channel
		if channel == 0:
			config |= self.ADS1015_REG_CONFIG_MUX_SINGLE_0
		elif channel == 1:
			config |= self.ADS1015_REG_CONFIG_MUX_SINGLE_1
		elif channel == 2:
			config |= self.ADS1015_REG_CONFIG_MUX_SINGLE_2
		elif channel == 3:
			config |= self.ADS1015_REG_CONFIG_MUX_SINGLE_3

		# Set 'start single-conversion' bit
		config |= self.ADS1015_REG_CONFIG_OS_SINGLE

		buf = bytearray(2)
		buf[0] = (config >> 8) & 0xff
		buf[1] = config & 0xff
		# Write config register to the ADC
		self._i2c.writeto_mem(self._addr, self.ADS1015_REG_POINTER_CONFIG, buf)

		# Wait for the conversion to complete
		sleep_ms(self._conversionDelay)

		data = self._i2c.readfrom_mem(self._addr, self.ADS1015_REG_POINTER_CONVERT, 2)

		# Shift 12-bit results right 4 bits for the ADS1015
		return ((int)(data[0] << 8 | data[1])) >> self._bitShift

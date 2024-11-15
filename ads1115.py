# ads1115.py
# Python script to interface with ADS1115 ADC with Raspberry Pi.
# Created on 24 April 2020 by Aidan Sun

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
ADS1115_DEFAULT_ADDRESS = 0x48

# ADS1115 Register Map
ADS1115_REG_POINTER_CONVERT   = 0x00
ADS1115_REG_POINTER_CONFIG    = 0x01
ADS1115_REG_POINTER_LOWTHRESH = 0x02
ADS1115_REG_POINTER_HITHRESH  = 0x03

# ADS1115 Configuration Register
ADS1115_CONFIG_SINGLE          = 0x8000
ADS1115_REG_CONFIG_MODE_CONTIN = 0x00
ADS1115_CONFIG_COMP_WINDOW     = 0x10
ADS1115_CONFIG_COMP_ACTVHI     = 0x08
ADS1115_CONFIG_COMP_LATCH      = 0x04
ADS1115_REG_CONFIG_CQUE_NONE   = 0x03

GAIN_2_3 = 0
GAIN_1   = 1
GAIN_2   = 2
GAIN_4   = 3
GAIN_8   = 4
GAIN_16  = 5

SPS_8    = 0
SPS_16   = 1
SPS_32   = 2
SPS_64   = 3
SPS_128  = 4
SPS_250  = 5
SPS_475  = 6
SPS_860  = 7

DIFF_0_1 = 0
DIFF_0_3 = 1
DIFF_1_3 = 2
DIFF_2_3 = 3

class ADS1115:
    """Class for interfacing with ADS1115"""
    def __init__(self, device_address=ADS1115_DEFAULT_ADDRESS, gain=GAIN_1, sps=SPS_128):
        # Set up address, gain, and SPS values
        gain_vals  = [0x00, 0x02, 0x04, 0x06, 0x08, 0x0A]
        sps_vals   = [0x00, 0x20, 0x40, 0x60, 0x80, 0xA0, 0xC0, 0xE0]

        self._addr = device_address
        self._gain = gain_vals[gain]
        self._sps  = sps_vals[sps]

    def read_adc(self, ch):
        """Reads a channel from the ADC. The ch parameter must be between 0 and 3.
        Returns the value as a 16-bit integer.
        """

        # Check if ch is valid
        if not(0 <= ch <= 3):
            raise ValueError("Channel must be between 0 and 3")

        channels = [0x40, 0x50, 0x60, 0x70]
        config = [ADS1115_CONFIG_SINGLE | channels[ch] | self._gain | ADS1115_REG_CONFIG_MODE_CONTIN, self._sps | ADS1115_REG_CONFIG_CQUE_NONE]
        bus.write_i2c_block_data(self._addr, ADS1115_REG_POINTER_CONFIG, config)
        time.sleep(0.02)
        data = bus.read_i2c_block_data(self._addr, ADS1115_REG_POINTER_CONVERT, 2)

        # Convert the data
        adc_data = (data[0] * 256) + data[1]
        return adc_data if adc_data <= 32767 else adc_data - 65535

    def read_adc_differential(self, ch):
        """Reads the difference between two ADC channels.
        Returns the value as a 16-bit integer.
        """

        # Check if ch is valid
        if not(0 <= ch <= 3):
            raise ValueError("Channel must be between 0 and 3")

        channels = [0x00, 0x10, 0x20, 0x30]
        config = [ADS1115_CONFIG_SINGLE | channels[ch] | self._gain | ADS1115_REG_CONFIG_MODE_CONTIN, self._sps | ADS1115_REG_CONFIG_CQUE_NONE]
        bus.write_i2c_block_data(self._addr, ADS1115_REG_POINTER_CONFIG, config)
        time.sleep(0.02)
        data = bus.read_i2c_block_data(self._addr, ADS1115_REG_POINTER_CONVERT, 2)

        # Convert the data
        adc_data = (data[0] * 256) + data[1]
        return adc_data if adc_data <= 32767 else adc_data - 65535

    def read_adc_comparator(self, ch, low_thresh, high_thresh, active_low=True, traditional=True, latching=False, num_readings=1):
        """Read an ADC channel with comparator enabled"""

        # Check if num_readings is valid
        if num_readings not in [1, 2, 4]:
            raise ValueError("num_readings must be 1, 2, or 4")

        comp_que = [None, 0, 1, None, 2]
        bus.write_i2c_block_data(self._addr, 0x02, [low_thresh >> 8, low_thresh & 0xFF])
        bus.write_i2c_block_data(self._addr, 0x03, [high_thresh >> 8, high_thresh & 0xFF])

        config = ADS1115_CONFIG_SINGLE | ((ch + 0x04) << 12) | self._gain | 0x0100 | self._sps

        if not traditional:
            config |= ADS1115_CONFIG_COMP_WINDOW

        if not active_low:
            config |= ADS1115_CONFIG_COMP_ACTVHI

        if latching:
            config |= ADS1115_CONFIG_COMP_LATCH
        config |= comp_que[num_readings]

        bus.write_i2c_block_data(self._addr, ADS1115_REG_POINTER_CONFIG, [config >> 8, config & 0xFF])
        time.sleep(0.02)
        data = bus.read_i2c_block_data(self._addr, ADS1115_REG_POINTER_CONVERT, 2)

        # Convert the data
        adc_data = (data[0] * 256) + data[1]
        return adc_data if adc_data <= 32767 else adc_data - 65535

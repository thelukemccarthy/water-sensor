import smbus
import time
from sensor_dto import *

import pickle
import os.path
class PhSensorSettings:

    def __init__(self):
        # default settings
        self.ph4_calibration = 1
        self.ph7_calibration = 1800
        self.ph_step = 60

        self.load()

    def save(self):
        with open('ph_settings.config', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def load(self):
        if(os.path.exists('ph_settings.config')):
            with open('ph_settings.config', 'rb') as input:
                temp = pickle.load(input)
                self.ph4_calibration = temp.ph4_calibration
                self.ph7_calibration = temp.ph7_calibration
                self.ph_step = temp.ph_step

class PhSensor:

    def __init__(self):
        self.bus = smbus.SMBus(0)
        self.address = 0x4d
        self.VREF = 3.3
        self.OP_AMP_GAIN = 5.25
        self.settings = PhSensorSettings()

    def read(self):
        raw = self._read_raw()
        ph = self._calulate_ph(raw)
        print("pH {0}, raw {1}".format(ph, raw))

        return SensorWithRawDto(ph, raw)

    def _read_raw(self):
        raw1 = self.bus.read_byte_data(self.address, 2)
        raw2 = self.bus.read_byte_data(self.address, 3)
        raw = (raw1 << 8) + raw2
        return raw

    # Now that we know our probe "age" we can calucalate the proper pH Its really a matter of applying the math
    # We will find our milivolts based on ADV vref and reading, then we use the 7 calibration
    # to find out how many steps that is away from 7, then apply our calibrated slope to calcualte real pH
    def _calulate_ph(self, raw):
        miliVolts = raw / 4096.0 * self.VREF * 1000.0
        temp = (self.VREF * self.settings.ph7_calibration / 4096.0 * 1000.0 - miliVolts) / self.OP_AMP_GAIN #5.25 is the gain of our amp stage we need to remove it
        pH = 7 - (temp / self.settings.ph_step)
        return pH 

    # Read raw reading while in pH4 calibration fluid and store it
    # Temperature compensation can be added by providing the temp offset per degree
    # IIRC .009 per degree off 25c (temperature-25*.009 added pH@4calc)
    def calibrate_ph_4(self, water_temperate):
        raw = self._read_raw()
        self.settings.ph4_calibration = raw + (water_temperate - 25) * 0.009
        self._calculate_ph_slope()

        ph = self.read()
        return (ph, self.settings.ph_step)
  
    # Lets read our raw reading while in pH7 calibration fluid and store it
    # We will store in raw format as this math works the same on pH step calcs
    # No need to temperature adjust for PH 7 as the temperature has no effect
    def calibrate_ph_7(self):
        raw = self._read_raw()
        self.settings.ph7_calibration = raw
        self._calculate_ph_slope()

        ph = self.read()
        return (ph, self.settings.ph_step)

    # This is really the heart of the calibration proccess, we want to capture the
    # probes "age" and compare it to the Ideal Probe, the easiest way to capture two readings,
    # at known point(4 and 7 for example) and calculate the slope.
    # If your slope is drifting too much from Ideal(59.16) its time to clean or replace!
    def _calculate_ph_slope(self):
        # RefVoltage * our deltaRawpH / 12bit steps *mV in V / OP-Amp gain /pH step difference 7-4
        self.settings.ph_step = ((((self.VREF*(self.settings.ph7_calibration - self.settings.ph4_calibration))/4096.0)*1000.0)/self.OP_AMP_GAIN)/3.0;
        self.settings.save()

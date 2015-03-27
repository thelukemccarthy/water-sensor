import smbus
from sensor_dto import *

class EcSensorSettings:
    def __init__(self):
        # default settings
        self.write_check = 1
        self.low_ec_calibration = 200
        self.high_ec_calibration = 1380
        self.ec_step = 60

    def save(self):
        print("Save not implemented.")

class EcSensor:
    def __init__(self):
        self.bus = smbus.SMBus(0)
        self.address = 0x4c
        self.VREF = 3300
        self.MCP3221_MAX_VALUE = 4095.0
        # voltage of oscillator output after voltage divider in millivolts i.e 120mV (measured AC RMS) ideal output is about 180-230mV range   
        self.oscillator_voltage = 185.0;
        # set our Kcell constant basically our microsiemesn conversion 10-6 for 1 10-7 for 10 and 10-5 for .1
        self.k_cell = 1.0; 
        # this is the measured value of the R9 resistor in ohms
        self.gain = 3000.0; 
        self.settings = EcSensorSettings()
        self._calculate_slope()

    def __read_raw(self):
        #raw = self.bus.read_word_data(self.address, 1)
        #raw1 = self.bus.read_word_data(self.address, 2)
        #raw2 = self.bus.read_word_data(self.address, 3)
        #raw3 = self.bus.read_word_data(self.address, 4)
        #raw = (raw1 << 8) + raw2
        #raw3 = self.bus.read_byte_data(self.address, 1)
        #print("{0}, {1}, {2}, {3}".format(result, raw1, raw2, raw3))
        raw1 = self.bus.read_byte_data(self.address, 2)
        raw2 = self.bus.read_byte_data(self.address, 3)
        raw = (raw1 << 8) + raw2
        return raw

    def read(self):
        raw = self.__read_raw()
        eC = self._calculate_ec(raw)

        print("eC {0}, raw {1}\n".format(eC, raw))

        return SensorWithRawDto(eC, raw)

    def _calculate_ec(self, raw):
        milivolts = self._calculate_millivolts(raw)

        # what is our overall gain again so we can cal our probe leg portion
        tempgain = milivolts / self.oscillator_voltage - 1.0

        # this is our actually Resistivity
        r_probe = self.gain / tempgain

        # this is where we convert to uS inversing so removed neg exponant
        uS = 1000000 * self.k_cell / r_probe 

        # convert to uS to eC
        eC = uS / 1000.0;
        return eC

    def _calculate_millivolts(self, raw):
        # MCP3221 is 12bit datasheet reports a full range of 4095
        return raw / self.MCP3221_MAX_VALUE * self.VREF 

    def calibrate_low_ec(self):
        self.settings.low_ec_calibration = self._read_raw()
        self._calculate_slope()
        ec = self.read()
        return (ec, self.settings.ec_step)
  
    def calibrate_high_ec(self):
        self.settings.high_ec_calibration = self._read_raw()
        self._calculate_slope()
        ec = self.read()
        return (ec, self.settings.ec_step)

    def _calculate_slope(self):
        self.settings.ec_step = self.VREF * (self.settings.low_ec_calibration - self.settings.high_ec_calibration) / 4095.0 * 1000.0;
        self.settings.save()
                                

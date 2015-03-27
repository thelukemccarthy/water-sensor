# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
# Refactored by: Luke McCarthy

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
sys.path.append('/home/pi/water_sensor/Adafruit_Python_DHT')
import Adafruit_DHT

class AirTemperatureAndHumidity:

    def __init__(self, sensor, gpio_pin):
        supported_sensors = { 11: Adafruit_DHT.DHT11,
                              22: Adafruit_DHT.DHT22,
                              2302: Adafruit_DHT.AM2302 }

        if  sensor in supported_sensors:
            self.sensor = supported_sensors[sensor]
            self.pin = gpio_pin
        else:
            print 'usage: sudo ./Adafruit_DHT.py [11|22|2302] GPIOpin#'
            print 'example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO #4'
            sys.exit(1)

    def read(self):
        # Try to grab a sensor reading.  Use the read_retry method 
        # which will retry up to 15 times to get a sensor reading 
        # (waiting 2 seconds between each retry).
        return  Adafruit_DHT.read_retry(self.sensor, self.pin)

#from air_temperature_and_humidity import AirTemperatureAndHumidity
#air = AirTemperatureAndHumidity(22, 17)
#air.read()

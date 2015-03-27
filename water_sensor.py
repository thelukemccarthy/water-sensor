import RPi.GPIO as GPIO
import time
from display import LcdDisplay
from display import TextJustification
from air_temperature_and_humidity import AirTemperatureAndHumidity
from water_temperature import WaterTemperature
from ph_sensor import PhSensor
from ec_sensor import EcSensor
from menu_buttons import MenuButtons
from calibrate_ph_menu import CalibratePhMenu

class WaterSensor:

    def __init__(self):
        self.display = LcdDisplay()
        self.air_temperature = AirTemperatureAndHumidity(22, 17)
        self.water_temperature = WaterTemperature()
        self.ph_sensor = PhSensor()
        self.ec_sensor = EcSensor()
        self.menu_buttons = MenuButtons()

    def start(self):
        while True:
            if(self.menu_buttons.is_next_pressed()):
                ph_menu = CalibratePhMenu(self.ph_sensor)
                ph_menu.start()
            self.__get_water_temperature()
            self.__get_air_temperature_and_humidity()
            self.__get_ph()
            self.__get_ec()
            self.__update_display()
            time.sleep(3)

    def __get_air_temperature_and_humidity(self):
        self.humidity, self.air_temp = self.air_temperature.read()
        self.humidity = round(self.humidity, 2)
        self.air_temp = round(self.air_temp, 2)

    def __get_water_temperature(self):
        self.water_temp = self.water_temperature.read()
        
    def __get_ph(self):
        self.__ph = self.ph_sensor.read()

    def __get_ec(self):
        self.__ec = self.ec_sensor.read()

    def __update_display(self):
        self.display.write_line(self.display.LINE_1, 
                           "Air {:05.2f}  Wtr {:05.2f}".format(self.air_temp, self.water_temp))
        self.display.write_line(self.display.LINE_2, 
                           "Humidity   {}%".format(self.humidity))
        self.display.write_line(self.display.LINE_3, 
                           "pH  {:05.2f}  Raw {}"
                                .format(self.__ph.get_value(), 
                                        self.__ph.get_raw_value()))
        self.display.write_line(self.display.LINE_4, 
                           "EC  {:05.2f}  Raw {}".format(self.__ec.get_value(), 
                                                         self.__ec.get_raw_value()))

    def __print_debug(self):
        print("Air {:05.2f}  Wtr {:05.2f}".format(self.air_temp, self.water_temp))
        print("Humidity   {}%".format(self.humidity))
        print("pH  {:05.2f}  Raw {}".format(self.__ph.get_value(), 
                                        self.__ph.get_raw_value()))
        print("EC  {:05.2f}  Raw {}".format(self.ec, self.ec_raw))

    def __del__(self):
        GPIO.cleanup()

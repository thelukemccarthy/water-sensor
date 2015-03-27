import RPi.GPIO as GPIO
import time
from display import LcdDisplay
from display import TextJustification
from ph_sensor import PhSensor
from water_temperature import WaterTemperature
from menu_buttons import MenuButtons
from sensor_dto import SensorWithRawDto

class CalibratePhMenu:

    def __init__(self, ph_sensor):
        self.display = LcdDisplay()
        self.ph_sensor = ph_sensor
        self.water_sensor = WaterTemperature()
        self.menu_buttons = MenuButtons()
        self.selected_ph = 4

    def start(self):
        while self.menu_buttons.is_menu_pressed() == False:
            self.__update_display()
            if(self.menu_buttons.is_select_pressed()):
                ph = SensorWithRawDto(0,0)
                step = 0

                while self.menu_buttons.is_next_pressed() == False:
                    self.__update_read_ph_display(ph, step)
                    if(self.selected_ph == 4):
                        ph, step = self.ph_sensor.calibrate_ph_4(self.water_sensor.read())
                    else:
                        ph, step = self.ph_sensor.calibrate_ph_7()
                    time.sleep(0.05)
            if(self.menu_buttons.is_next_pressed()):
                if(self.selected_ph == 4):
                    self.selected_ph = 7
                else:
                    self.selected_ph = 4
            time.sleep(0.05)

    def __update_display(self):
        self.display.write_line(self.display.LINE_1, 
                           "Calibrate pH", TextJustification.CENTRE)
        self.display.write_line(self.display.LINE_2, "Green button 2 start")
        self.display.write_line(self.display.LINE_3, 
                           self.__update_selected_line("Place probe in pH 4", 4))
        self.display.write_line(self.display.LINE_4, 
                           self.__update_selected_line("Place probe in pH 7", 7))

    def __update_read_ph_display(self, ph, step):
        self.display.write_line(self.display.LINE_1, 
                           "Reading pH{}".format(self.selected_ph), 
                                TextJustification.CENTRE)
        self.display.write_line(self.display.LINE_2, "Yellow button 2 stop")
        self.display.write_line(self.display.LINE_3, 
                                "ph  {:05.2f}  raw {}"
                                .format(ph.get_value(), ph.get_raw_value()))
        self.display.write_line(self.display.LINE_4, "Step {:2.2f} Ideal 59.16".format(step))
        
    def __update_selected_line(self, line_text, selected_ph):
        if self.selected_ph == selected_ph:
            return ">" + line_text
        else:
            return line_text

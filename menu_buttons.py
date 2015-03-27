import RPi.GPIO as GPIO
import time

class MenuButtons:

    def __init__(self):
        self.MENU_PIN = 10
        self.SELECT_PIN = 9
        self.NEXT_PIN = 11
        self.HIGH = 1

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.MENU_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.SELECT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.NEXT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def is_menu_pressed(self): # White button
        return GPIO.input(self.MENU_PIN) == self.HIGH

    def is_select_pressed(self): # Green button
        return GPIO.input(self.SELECT_PIN) == self.HIGH

    def is_next_pressed(self): # Yellow button
        return GPIO.input(self.NEXT_PIN) == self.HIGH


#mb = MenuButtons()

#while True:
#    if(mb.is_menu_pressed()):
#        print("The Menu button was pressed")
#    if(mb.is_select_pressed()):
#        print("The Select button was pressed")
#    if(mb.is_next_pressed()):
#        print("The Next button was pressed")

# HD44780 20x4 LCD Test Script for
# Raspberry Pi
#
# Author      : Matt Hawkins
# Site        : http://www.raspberrypi-spy.co.uk/ 
# Date        : 09/08/2012
#
# Refacted by : Luke McCarthy

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V) via 10k variable resistor to adjust the contrast
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V via 560 ohm
# 16: LCD Backlight GND

import RPi.GPIO as GPIO
import time

class TextJustification:
  LEFT = 1
  CENTRE = 2
  RIGHT = 3

class LcdDisplay:

  def __init__(self):
    self.__define_gpio_lcd_mapping()
    self.__define_constains()
    self.__define_gpio_pins()
    self.__lcd_init()
  
  def __define_gpio_lcd_mapping(self):
    self.LCD_RS = 7
    self.LCD_E  = 8
    self.LCD_D4 = 25
    self.LCD_D5 = 24
    self.LCD_D6 = 23
    self.LCD_D7 = 18
    self.LED_ON = 15

  def __define_constains(self):
    self.LCD_WIDTH = 20    # Maximum characters per line
    self.LCD_CHR = True
    self.LCD_CMD = False

    self.LINE_1 = 0x80 # LCD RAM address for the 1st line
    self.LINE_2 = 0xC0 # LCD RAM address for the 2nd line
    self.LINE_3 = 0x94 # LCD RAM address for the 3rd lin
    self.LINE_4 = 0xD4 # LCD RAM address for the 4th line

    # Timing constants
    self.E_PULSE = 0.00005
    self.E_DELAY = 0.00005

  def __define_gpio_pins(self):
    GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
    GPIO.setup(self.LCD_E, GPIO.OUT)  # E
    GPIO.setup(self.LCD_RS, GPIO.OUT) # RS
    GPIO.setup(self.LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(self.LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(self.LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(self.LCD_D7, GPIO.OUT) # DB7
    GPIO.setup(self.LED_ON, GPIO.OUT) # Backlight enable

  def write_line(self, lcd_line, text, justification = TextJustification.LEFT):
    self.__lcd_byte(lcd_line, self.LCD_CMD)
    self.__lcd_string(text, justification)

  def __lcd_init(self):
    # Initialise display
    self.__lcd_byte(0x33, self.LCD_CMD)
    self.__lcd_byte(0x32, self.LCD_CMD)
    self.__lcd_byte(0x28, self.LCD_CMD)
    self.__lcd_byte(0x0C, self.LCD_CMD)
    self.__lcd_byte(0x06, self.LCD_CMD)
    self.__lcd_byte(0x01, self.LCD_CMD)

  def __lcd_string(self, message, justification):
    if justification==TextJustification.LEFT:
      message = message.ljust(self.LCD_WIDTH, " ")
    elif justification==TextJustification.CENTRE:
      message = message.center(self.LCD_WIDTH, " ")
    elif justification==TextJustification.RIGHT:
      message = message.rjust(self.LCD_WIDTH, " ")

    for i in range(self.LCD_WIDTH):
      self.__lcd_byte(ord(message[i]), self.LCD_CHR)

  def __lcd_byte(self, bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command

    GPIO.output(self.LCD_RS, mode) # RS

    # High bits
    GPIO.output(self.LCD_D4, False)
    GPIO.output(self.LCD_D5, False)
    GPIO.output(self.LCD_D6, False)
    GPIO.output(self.LCD_D7, False)
    if bits&0x10==0x10:
      GPIO.output(self.LCD_D4, True)
    if bits&0x20==0x20:
      GPIO.output(self.LCD_D5, True)
    if bits&0x40==0x40:
      GPIO.output(self.LCD_D6, True)
    if bits&0x80==0x80:
      GPIO.output(self.LCD_D7, True)

    # Toggle 'Enable' pin
    time.sleep(self.E_DELAY)
    GPIO.output(self.LCD_E, True)
    time.sleep(self.E_PULSE)
    GPIO.output(self.LCD_E, False)
    time.sleep(self.E_DELAY)

    # Low bits
    GPIO.output(self.LCD_D4, False)
    GPIO.output(self.LCD_D5, False)
    GPIO.output(self.LCD_D6, False)
    GPIO.output(self.LCD_D7, False)
    if bits&0x01==0x01:
      GPIO.output(self.LCD_D4, True)
    if bits&0x02==0x02:
      GPIO.output(self.LCD_D5, True)
    if bits&0x04==0x04:
      GPIO.output(self.LCD_D6, True)
    if bits&0x08==0x08:
      GPIO.output(self.LCD_D7, True)

    # Toggle 'Enable' pin
    time.sleep(self.E_DELAY)
    GPIO.output(self.LCD_E, True)
    time.sleep(self.E_PULSE)
    GPIO.output(self.LCD_E, False)
    time.sleep(self.E_DELAY)

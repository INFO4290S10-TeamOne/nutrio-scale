# This code is designed as a backend for a functional scale apparatus.
# It has borrowed some blocks of code from publically available tutorials and resources.
# Authors include tatobari and their hx711py code available off github.
import sys
import RPi.GPIO as GPIO

from time import *
from datetime import datetime
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
from hx711 import HX711

# VARIABLES
REFERENCEUNIT = 1
BUTTON_GPIO = 16       # Button pin

# BUTTON SETUP
GPIO.setmode(GPIO.BCM) # Sets GPIO numbering mode
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# FUNCTIONS
def cleanAndExit():    
    print("\nCleaning...")
    GPIO.cleanup()       
    print("Bye!")
    sys.exit()

def button_callback(channel): # Tare function activated via button
    print("Scale tare'd")
    hx.reset()
    hx.tare()

GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_callback) #falling edge detection for button     
    
def loop():
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    while(True):
                 
        lcd.clear()
        lcd.setCursor(0,0)  # set cursor position
        val = hx.get_weight() #gets weight reading from sensor
        lcd.message("{0}g".format(round(val))) 

        hx.power_down()
        hx.power_up()
        
        sleep(2)
    
PCF8574_address = 0x27      # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F     # I2C address of the PCF8574A chip.


# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)


# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
hx = HX711(5, 6)

# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# Have the reference unit set to 1 on initialization
# Know the exact weight of an object and place it on the sensor
# Run scale.py and wait for values close to 0 to appear (negative is ok)
# Remove the object and note the value now displayed
# Divide this value by the weight of the value in grams
hx.set_reference_unit(855)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")

while True:
    try:
        loop()

    except (KeyboardInterrupt, SystemExit): #Exits on ctrl+c entry
        lcd.clear()
        cleanAndExit()
        

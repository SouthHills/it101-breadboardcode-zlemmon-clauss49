# Description : Control RGBLED with Potentiometers
from pathlib import Path
import sys
from gpiozero import RGBLED
import time

HERE = Path(__file__).parent.parent
sys.path.append(str(HERE / 'Common'))
from ADCDevice import * 

USING_GRAVITECH_ADC = False # Only modify this if you are using a Gravitech ADC

ledRedPin = 22      # define 3 pins for RGBLED
ledGreenPin = 27
ledBluePin = 17
rgb_led = RGBLED(red=ledRedPin, green=ledGreenPin, blue=ledBluePin, pwm=True)
adc = ADCDevice() # Define an ADCDevice class object

def setup():
    global adc
    if(adc.detectI2C(0x48) and USING_GRAVITECH_ADC): 
        adc = GravitechADC()
    elif(adc.detectI2C(0x48)): # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
            "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
            "Program Exit. \n")
        exit(-1)
    
def loop():
    global adc, red_value, green_value, blue_value, rgb_led
    while True:     
        red_value = adc.analogRead(0)       # read ADC value of 3 potentiometers
        green_value = adc.analogRead(1)
        blue_value = adc.analogRead(2)
        
        # map the read value of potentiometers into normalized values (0-1) and set the RGBLED color
        rgb_led.value = (red_value / 255.0, green_value / 255.0, blue_value / 255.0)
        
        # print read ADC value
        print(f'ADC Value value_Red: {red_value}, value_Green: {green_value}, value_Blue: {blue_value}')
        time.sleep(0.01)

def destroy():
    global adc, rgb_led
    adc.close()
    rgb_led.close()
    
if __name__ == '__main__': # Program entrance
    print ('Program is starting ... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()

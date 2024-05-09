# Description : Control LED with Photoresistor
from pathlib import Path
import sys
from gpiozero import PWMLED
import time
import RPi.GPIO as GPIO



#barlight pins
ledPins = [12,16,18,22,32,36,38,40,37,35]

HERE = Path(__file__).parent.parent
sys.path.append(str(HERE / 'Common'))
from ADCDevice import * 

USING_GRAVITECH_ADC = False # Only modify this if you are using a Gravitech ADC

LED = PWMLED(17)
ADC = ADCDevice() # Define an ADCDevice class object

def setup():
    global ADC
    if(ADC.detectI2C(0x48) and USING_GRAVITECH_ADC): 
        ADC = GravitechADC()
    elif(ADC.detectI2C(0x48)): # Detect the pcf8591.
        ADC = PCF8591()
    elif(ADC.detectI2C(0x4b)): # Detect the ads7830
        ADC = ADS7830()
    else:
        print("No correct I2C address found, \n"
            "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
            "Program Exit. \n")
        exit(-1)
        
    #enable barlight
    GPIO.setmode(GPIO.BOARD)        # use PHYSICAL GPIO Numbering
    GPIO.setup(ledPins, GPIO.OUT)   # set all ledPins to OUTPUT mode
    GPIO.output(ledPins, GPIO.HIGH) # make all ledPins output HIGH level, turn off all led
    
def loop():
    global ADC, LED
    while True:
        value = ADC.analogRead(0)   # read the ADC value of channel 0
        LED.value = value / 255.0   # Mapping to PWM duty cycle        
        voltage = value / 255.0 * 3.3
        print (f'ADC Value: {value}\tVoltage: {voltage:.2f}\tLED Value: {LED.value:.2f}')
        time.sleep(0.01)
        
        # barlight thing
        #while True:
        #    for pin in ledPins:     # make led(on) move from left to right
        #        GPIO.output(pin, GPIO.LOW)  
        #        time.sleep(0.1)
        #        GPIO.output(pin, GPIO.HIGH)
        #    for pin in ledPins[::-1]:       # make led(on) move from right to left
        #        GPIO.output(pin, GPIO.LOW)  
        #        time.sleep(0.1)
        #        GPIO.output(pin, GPIO.HIGH)

def destroy():
    global ADC, LED
    ADC.close()
    LED.close()
    GPIO.cleanup()
    
if __name__ == '__main__':   # Program entrance
    print ('Program is starting ... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
        
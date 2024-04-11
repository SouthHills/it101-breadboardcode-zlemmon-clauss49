# Description : Use ADC module to read the voltage value of potentiometer.
from pathlib import Path
import sys
from gpiozero import PWMLED
import time

HERE = Path(__file__).parent.parent
sys.path.append(str(HERE / 'Common'))
from ADCDevice import * 

USING_GRAVITECH_ADC = False # Only modify this if you are using a Gravitech ADC

led = PWMLED(17) #17 is the pin
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
    while True:
        # read the ADC value of channel 0
        value = adc.analogRead(0)  # Gets a value between 0 and 255
        # Set LED brightness directly with value from ADC
        led.value = value / 255.0  # Value of PWM LED must be between 0 and 1
        # calculate the voltage value
        voltage = value / 255.0 * 3.3  # 3.3 because we are using the 3.3V lead
        print(f'ADC Value : {value}, Voltage : {voltage:.2f}')
        time.sleep(0.03)

def destroy():
    led.close()
    adc.close()
    
if __name__ == '__main__':   # Program entrance
    print ('Program is starting ... ')
    try:
        setup()
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()
        
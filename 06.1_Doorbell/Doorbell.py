import RPi.GPIO as GPIO
from gpiozero import Buzzer, Button

buzzer = Buzzer(17)
button = Button(18)

def loop():
    while True:
        if button.is_pressed: # if button is pressed
            buzzer.on() # turn on buzzer
            print ('buzzer turned on >>>')
        else: # if button is relessed
            buzzer.off() # turn off buzzer
            print ('buzzer turned off <<<')

def destroy():
    buzzer.close()
    button.close()

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()


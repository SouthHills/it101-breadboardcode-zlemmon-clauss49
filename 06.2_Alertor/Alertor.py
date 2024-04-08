from gpiozero import TonalBuzzer, Button
import time
from signal import pause

buzzer = TonalBuzzer(17)
button = Button(18)
HIGH_TONE = 600 # The max is 880 but that hurts my ears
LOW_TONE = 220
    
def setup():
    # Setup events for when the button is pressed and released
    button.when_pressed = alertor
    button.when_released = stop_alertor

def alertor():
    print ('alertor turned on >>> ')
    
    while True:  
        # Linear
        for x in range(LOW_TONE, HIGH_TONE):
            buzzer.play(x)
            time.sleep(0.002)
            
            if not button.is_pressed:
                return  
            
        for x in range(HIGH_TONE, LOW_TONE, -1):
            buzzer.play(x)
            time.sleep(0.002)
            
            if not button.is_pressed:
                return 
        
def stop_alertor():
    buzzer.stop()
    print ('alertor turned off <<<')

def destroy():
    buzzer.close()
    button.close()

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        pause()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()

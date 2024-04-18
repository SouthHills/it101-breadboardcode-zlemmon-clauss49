from gpiozero import LED as LEDClass, Button
from signal import pause
from time import sleep

LED = LEDClass(17)  # define ledPin
BUTTON = Button(18)  # define buttonPin

def changeLedState():
    global LED
    global pushed
    LED.toggle()
    if LED.is_lit:
        print ("led turned on strobe>>>")
        
        
    else:
        print ("led turned off strobe <<<")
        
        
def destroy():
    global LED, BUTTON
    # Release resources
    LED.close()
    BUTTON.close()

if __name__ == "__main__":     # Program entrance
    print ("Program is starting...")
    try:
        # If the button gets pressed, call the function
        # This is an event
        pushed = True
        BUTTON.when_pressed = changeLedState
        
        while pushed == True:
            LED.on
            sleep(1)
            LED.off
            sleep(1)
        
          
          
        pause()
        
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()

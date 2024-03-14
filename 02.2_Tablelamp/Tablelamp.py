from gpiozero import LED, Button
from signal import pause

led = LED(17)  # define ledPin
button = Button(18)  # define buttonPin
ledState : bool = False

def changeLedState():
    global ledState
    ledState = not ledState
    if(ledState == True):
        led.on()
        print ("led turned on >>>")
    else:
        led.off()
        print ("led turned off <<<")

def destroy():
    # Release resources
    led.close()
    button.close()

if __name__ == "__main__":     # Program entrance
    print ("Program is starting...")
    try:
        # If the button gets pressed, call the function
        # This is an event
        button.when_pressed = changeLedState
        pause()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()


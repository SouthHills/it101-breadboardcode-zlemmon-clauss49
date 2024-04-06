from gpiozero import LED, Button
from signal import pause

led = LED(17)  # define ledPin
button = Button(18)  # define buttonPin

def changeLedState():
    led.toggle()
    if led.is_lit:
        print ("led turned on >>>")
    else:
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


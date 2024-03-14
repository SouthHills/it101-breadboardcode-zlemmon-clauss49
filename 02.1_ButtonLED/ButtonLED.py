from gpiozero import LED, Button

led = LED(17)  # define ledPin
button = Button(18)  # define buttonPin

def loop():
    while True:
        if button.is_pressed:  # if button is pressed
            led.on()  # turn on led
            print ("led turned on >>>")  # print information on terminal
        else:  # if button is released
            led.off()  # turn off led 
            print ("led turned off <<<")    

def destroy():
    # Release resources
    led.close()
    button.close()

if __name__ == "__main__":     # Program entrance
    print ("Program is starting...")
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()


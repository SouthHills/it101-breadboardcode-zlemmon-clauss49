from gpiozero import LED
import time

led = LED(17)  # define led

def loop():
    while True:
        led.on() 
        print ("led turned on >>>") # print information on terminal
        time.sleep(1)
        led.off()
        print ("led turned off <<<")
        time.sleep(1)
        
def destroy():
    # Release resources
    led.close()

if __name__ == "__main__":    # Program start point
    print("Program is starting ... \n")
    print(f"Using pin {led.pin}")
    try:
        loop()
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()

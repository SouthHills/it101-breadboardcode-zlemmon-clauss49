# Description : Control 4_Digit_7_Segment_Display with 74HC595
from gpiozero import OutputDevice
import time

LSBFIRST = 1
MSBFIRST = 2
# define the pins for 74HC595
DATA_PIN = OutputDevice(24)      # DS Pin of 74HC595(Pin14)
LATCH_PIN = OutputDevice(23)     # ST_CP Pin of 74HC595(Pin12)
CLOCK_PIN = OutputDevice(18)     # CH_CP Pin of 74HC595(Pin11)

# Define the patterns for the characters "0"-"9".
# Due to common anode, 0 means LED on and 1 means LED off.
# Note that the MSB is the decimal point.
NUM_PATTERNS = (
    0b1100_0000, # 0
    0b1111_1001, # 1
    0b1010_0100, # 2
    0b1011_0000, # 3
    0b1001_1001, # 4
    0b1001_0010, # 5
    0b1000_0010, # 6
    0b1111_1000, # 7
    0b1000_0000, # 8
    0b1001_0000  # 9
)

digitPin = (17, 22, 27,10) # If your digits are out of order, rearrange this tuple
outputs = list(map(lambda pin: OutputDevice(pin), digitPin))
counter = 0         # Variable counter, the number will be dislayed by 7-segment display

def shift_out(order,val):
    """
    Sends data to the 74HC595 chip using serial communication.
    Serial communication is a method of transmitting data one bit at a time, sequentially.

    Args:
        order (int): The order of bits to be sent. Use LSBFIRST or MSBFIRST.
        val (int): The data to be sent as a sequence of bits.
    """
    global LSBFIRST, MSBFIRST, CLOCK_PIN, DATA_PIN
    for i in range(0, 8):
        CLOCK_PIN.off()  # Turning off the clock to prepare for sending a bit
        if order == LSBFIRST:
            # If we're sending LSB first, we check each bit of the value from right to left
            #   and send it out accordingly
            if (0x01 & (val >> i) == 0x01):
                DATA_PIN.on()   # If the bit is 1, we turn on the data pin
            else:
                DATA_PIN.off()  # If the bit is 0, we turn off the data pin
        elif order == MSBFIRST:
            # If we're sending MSB first, we check each bit of the value from left to right
            #   and send it out accordingly
            if (0x80 & (val << i) == 0x80):
                DATA_PIN.on()   # If the bit is 1, we turn on the data pin
            else:
                DATA_PIN.off()  # If the bit is 0, we turn off the data pin
        CLOCK_PIN.on()  # Turning on the clock to send the bit
            
def outData(data):      # function used to output data for 74HC595
    global LATCH_PIN, MSBFIRST
    LATCH_PIN.off()
    shift_out(MSBFIRST, data)
    LATCH_PIN.on()
    
def selectDigit(digit): # Open one of the 7-segment display and close the remaining three
    outputs[0].off() if ((digit&0x08) == 0x08) else outputs[0].on()
    outputs[1].off() if ((digit&0x04) == 0x04) else outputs[1].on()
    outputs[2].off() if ((digit&0x02) == 0x02) else outputs[2].on()
    outputs[3].off() if ((digit&0x01) == 0x01) else outputs[3].on()
    
def display(dec):   # display function for 7-segment display
    global NUM_PATTERNS
    outData(0xff)   # eliminate residual display
    selectDigit(0x01)   # Select the first, and display the single digit
    outData(NUM_PATTERNS[dec%10])
    
    time.sleep(0.003)   # display duration
    outData(0xff)
    selectDigit(0x02)   # Select the second, and display the tens digit
    outData(NUM_PATTERNS[dec%100//10])
    
    time.sleep(0.003)
    outData(0xff)
    selectDigit(0x04)   # Select the third, and display the hundreds digit
    outData(NUM_PATTERNS[dec%1000//100])
    
    time.sleep(0.003)
    outData(0xff)
    selectDigit(0x08)   # Select the fourth, and display the thousands digit
    outData(NUM_PATTERNS[dec%10000//1000])
    
def initial_test():
    print("Printing 1234 to the LED display...")
    start_time = time.time()
    while time.time() - start_time < 2:  # Display 1234 for 2 seconds
        display(1234)
    print("Printing 8888 to the LED display...")
    start_time = time.time()
    while time.time() - start_time < 2:  # Display 8888 for 2 seconds
        display(8888)
          
def loop():
    global counter
    while True:
        start_time = time.time()
        while time.time() - start_time < 1:  # Keep number on for one second
            display(counter)
        counter += 1
        print(counter)
        
def destroy():  
    global DATA_PIN, LATCH_PIN, CLOCK_PIN
    DATA_PIN.close()
    LATCH_PIN.close()
    CLOCK_PIN.close()        

if __name__ == '__main__': # Program entrance
    print ('Program is starting...')
    try:
        initial_test()
        loop()  
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()
 
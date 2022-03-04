import spidev
import time

LDR_CHANNEL = 0
POT_CHANNEL = 7

LDR_MIN = 2 # Lowest ADC reading seen (High light level)
LDR_MAX = 1024 # Highest ADC reading seen (Lowest light level)

POT_MIN = 0 # Turned CCW all the way
POT_MAX = 546 # Turned CW all the way

class ADC:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz=1000000

    def read(self, channel):
        adc = self.spi.xfer2([1,(8+channel)<<4,0])
        value = ((adc[1]&3) << 8) + adc[2]
        return value

# Reads from the LDR channel and scales it from 0-1
def readLDR(adc):
    return (adc.read(LDR_CHANNEL) - LDR_MIN) / (LDR_MAX - LDR_MIN)

# Reads from the POT channel and scales it from 0-1
def readPOT(adc):
    return (adc.read(POT_CHANNEL) - POT_MIN) / (POT_MAX - POT_MIN)

####################### Test Functions Below #######################

# Function to read raw values from a channel, tracking the min and max values
def minMaxReader(channel):
    adc = ADC()
    mymax = adc.read(channel)
    mymin = mymax
    print("Starting MIN/MAX:", mymax)
    try:
        while True:
            newval = adc.read(channel)
            if newval > mymax:
                mymax = newval
                print("MAX: ", mymax)
            elif newval < mymin:
                mymin = newval
                print("MIN: ", mymin)
            else:
                print(newval)
            time.sleep(1)
    except KeyboardInterrupt:
        print()
        print("MIN: ", mymin)
        print("MAX: ", mymax)
        pass


# Test function to read the raw values from ADC channels
def testRawRead(channels):
    adc = ADC()
    try:
        while True:
            print("LDR: ", adc.read(LDR_CHANNEL))
            print("POT: ", adc.read(POT_CHANNEL))
            time.sleep(1)
    except KeyboardInterrupt:
        pass

# Test function to read the scaled values from ADC channels
def testScaledRead():
    adc = ADC()
    try:
        while True:
            print("LDR: ", readLDR(adc))
            print("POT: ", readPOT(adc))
            time.sleep(1)
    except KeyboardInterrupt:
        pass


def main():
    #testRawRead([LDR_CHANNEL, POT_CHANNEL])
    minMaxReader(POT_CHANNEL)
    #testScaledRead()


if __name__ == "__main__":
    main()
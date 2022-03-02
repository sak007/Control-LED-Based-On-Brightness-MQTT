import spidev

class ADC:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz=1000000

    def read(self, channel):
        adc = self.spi.xfer2([1,(8+channel)<<4,0])
        value = ((adc[1]&3) << 8) + adc[2]
        return value

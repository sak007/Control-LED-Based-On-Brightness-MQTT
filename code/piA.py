from client import Client
import json
import time
import RPi.GPIO as GPIO
import mygpio
from adc import *
import wifi

PERCENT_DELTA = .05 # Publish changes of this %
SAMPLE_TIME = .1 # Sample ADC every x seconds

class PiAClient(Client):
    def mysetup(self):
        self.setStatusWill("status/RaspberryPiA")
        self.setOnConnectMessage('status/RaspberryPiA', 'online')
        self.setOnGracefulDisconnectMessage('status/RaspberryPiA', 'offline')

        self.connect()

        self.publishedLightSensor = None
        self.publishedThreshold = None

        self.subscribe("lightSensor")
        self.subscribe("threshold")

    def on_message(self, client, userdata, msg):
        topic = str(msg.topic)
        payload = str(msg.payload.decode("utf-8"))

        if topic == 'lightSensor':
            self.publishedLightSensor = payload
        elif topic == 'threshold':
            self.publishedThreshold = payload

        print("Received Topic: " + topic + ", Value: " + payload)


    def updateLightSensor(self, newValue, deltaThreshold):
        # First Reading/Publish ?
        if self.publishedLightSensor == None:
            self.publish("lightSensor", payload=str(newValue))
            self.publishedLightSensor = newValue
        # Is % diff of old and new value > the deltaThreshold %
        elif abs(newValue - float(self.publishedLightSensor)) > deltaThreshold:
            self.publish("lightSensor", payload=str(newValue))
            self.publishedLightSensor = newValue

    def updateThreshold(self, newValue, deltaThreshold):
        # First Reading/Publish ?
        if self.publishedThreshold == None:
            self.publish("threshold", payload=str(newValue))
            self.publishedThreshold = newValue
        # Is % diff of old and new value > the deltaThreshold % ?
        elif abs(newValue - float(self.publishedThreshold)) > deltaThreshold:
            self.publish("threshold", payload=str(newValue))
            self.publishedThreshold = newValue

# Sets up ADC, buttons, optional LEDs, and MQTT client
# In a loop, reads from ADC every .1 s, if the client is running, then
# an update to the last published values will be made if the PercentDelta is 
# great enough, then the wifi and connection button are checked to see if they are
# pressed and are handled
# Note, after wifi is reconnected, if the client was not explicitly disconnected,
# then it can be used without needed to reconnect/press the conn button
def main():
    # Load Connection Properties
    f = open('../properties.json')
    properties = json.load(f)
    BROKER_ADDR = properties['BROKER_ADDR']
    BROKER_PORT = properties['BROKER_PORT']
    # Connect ADC
    myadc = ADC()
    # Setup GPIO
    mygpio.setup()
    wifiBtn = mygpio.Button(mygpio.WIFI_PIN)
    connBtn = mygpio.Button(mygpio.CONN_PIN)
    try:
        # Setup MQTT Client
        client = PiAClient(BROKER_ADDR, BROKER_PORT, 'RaspberryPiA')
        client.mysetup()
        clientRunning = True # Protects client from publishing when it doesnt have a connection
        mygpio.turnOn(mygpio.CONN_LIGHT_PIN) # Optional Conn LED
        mygpio.turnOn(mygpio.WIFI_LIGHT_PIN) # Optional Wifi LED
        lastReadTime = time.time()

        while True:
            # Read from the ADC
            if (time.time() - lastReadTime) >= SAMPLE_TIME:
                ls = readLDR(myadc)
                th = readPOT(myadc)
                #print("Last Read Time %f seconds" % (time.time() - lastReadTime))
                lastReadTime = time.time()

                # Update values if client is running safely
                if clientRunning:
                    client.updateLightSensor(ls, PERCENT_DELTA)
                    client.updateThreshold(th, PERCENT_DELTA)

            # Handle Wifi button
            clientRunning = mygpio.handleWifiButton(wifiBtn, client, clientRunning)
            # Handle Conn button
            clientRunning = mygpio.handleConnBtn(connBtn, client, clientRunning)

            time.sleep(.005) # Needed to catch the Keyboard Interrupt
        
    except KeyboardInterrupt as e:
        print("Detected Keyboard Interrupt")
        GPIO.cleanup()
        client.disconnect()
        quit()



if __name__ == "__main__":
    main()


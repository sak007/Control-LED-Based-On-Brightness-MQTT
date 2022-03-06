from client import Client
import json
import time
import RPi.GPIO as GPIO
import mygpio
import wifi

class PiCClient(Client):
    def mysetup(self):
        self.setStatusWill("status/RaspberryPiC")
        self.setOnConnectMessage('status/RaspberryPiC', 'online')
        self.setOnGracefulDisconnectMessage('status/RaspberryPiC', 'offline')

        self.connect()
        
        self.lightSensor = None
        self.threshold = None
        self.lightStatus = None

        client.subscribe("lightStatus")
        client.subscribe("lightSensor")
        client.subscribe("threshold")

        time.sleep(1)

    def on_message(self, client, userdata, msg):
        topic = str(msg.topic)
        payload = str(msg.payload.decode("utf-8"))

        if topic == 'lightSensor':
            self.lightSensor = float(payload)
        elif topic == 'threshold':
            self.threshold = float(payload)
        elif topic == 'lightStatus':
            self.lightStatus = payload

        print ("Received Topic: " + topic + ", Value: " + payload)

    def updateLightStatus(self):
        if self.lightSensor != None and self.threshold != None:
            if (self.lightSensor > self.threshold) and self.lightStatus != 'TurnOn':
                self.lightStatus = 'TurnOn'
                self.publish("lightStatus", payload=self.lightStatus)
            elif (self.lightSensor <= self.threshold) and self.lightStatus != 'TurnOff':
                self.lightStatus = 'TurnOff'
                self.publish("lightStatus", payload=self.lightStatus)

if __name__ == "__main__":

    f = open('../properties.json')
    properties = json.load(f)
    BROKER_ADDR = properties['BROKER_ADDR']
    BROKER_PORT = properties['BROKER_PORT']
    try:
        client = PiCClient(BROKER_ADDR, BROKER_PORT, 'RaspberryPiC')
        client.mysetup()

        # Setup GPIO
        mygpio.setup()
        wifiBtn = mygpio.Button(mygpio.WIFI_PIN)
        connBtn = mygpio.Button(mygpio.CONN_PIN)

        mygpio.turnOn(mygpio.CONN_LIGHT_PIN) # Optional Conn LED
        mygpio.turnOn(mygpio.WIFI_LIGHT_PIN) # Optional Wifi LED
        clientRunning = True # Protects client from publishing when it doesnt have a connection
        # Give some time for any retained messages to show
        time.sleep(1)

        while True:
            
            client.updateLightStatus()
            # Handle clientConnection Discrepencies
            clientRunning = mygpio.handleConnDiscrepencies(client, clientRunning)
            # Handle Wifi button
            clientRunning = mygpio.handleWifiButton(wifiBtn, client, clientRunning)
            # Handle Conn button
            clientRunning = mygpio.handleConnBtn(connBtn, client, clientRunning)

            time.sleep(.005) # Needed to catch the Keyboard Interrupt
    except KeyboardInterrupt:
        GPIO.cleanup()
        client.disconnect()
        quit()

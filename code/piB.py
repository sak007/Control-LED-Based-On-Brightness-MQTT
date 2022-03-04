from client import Client
import time
import RPi.GPIO as GPIO
import json
import mygpio
import wifi

LIGHT_STATUS_PIN = 11
PI_A_PIN = 13
PI_C_PIN = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LIGHT_STATUS_PIN, GPIO.OUT)
GPIO.setup(PI_A_PIN, GPIO.OUT)
GPIO.setup(PI_C_PIN, GPIO.OUT)

class PiBClient(Client):
    def mysetup(self):
        client.connect()

        client.brokerLightStatus = False
        client.lightStatus = False
        client.piA = False
        client.piC = False

        client.subscribe("lightStatus")
        client.subscribe("status/RaspberryPiA")
        client.subscribe("status/RaspberryPiC")

    def on_message(self, client, userdata, msg):
        topic = str(msg.topic)
        payload = str(msg.payload.decode("utf-8"))

        if topic == 'lightStatus':
            # Store value of light status received from broker
            # but don't assign it to the final light status
            # output. It must first be arbitrated with the state
            # of PiC
            if payload == 'TurnOn':
                self.brokerLightStatus = True
            else:
                self.brokerLightStatus = False
        elif topic == 'status/RaspberryPiA':
            if payload == 'online':
                self.piA = True
            else:
                self.piA = False
        elif topic == 'status/RaspberryPiC':
            if payload == 'online':
                self.piC = True
            else:
                self.piC = False

        # Determine state of PiC and set final value of
        # light status as appropriate
        if self.piC == True:
            self.lightStatus = self.brokerLightStatus
        else:
            self.lightStatus = False

        print ("Received Topic: " + topic + ", Value: " + payload)
        print("Updated Outputs:\n   PiA Online (" + str(self.piA) + ")\n   PiC Online (" + str(self.piC) + ")\n   Light Status On (" + str(self.lightStatus)+ ")")

if __name__ == "__main__":

    f = open('../properties.json')
    properties = json.load(f)
    BROKER_ADDR = properties['BROKER_ADDR']
    BROKER_PORT = properties['BROKER_PORT']

    # Setup GPIO
    mygpio.setup()
    wifiBtn = mygpio.Button(mygpio.WIFI_PIN)
    connBtn = mygpio.Button(mygpio.CONN_PIN)

    try:
        client = PiBClient(BROKER_ADDR, BROKER_PORT, 'RaspberryPiB')
        client.mysetup()

        mygpio.turnOn(mygpio.CONN_LIGHT_PIN) # Optional Conn LED
        mygpio.turnOn(mygpio.WIFI_LIGHT_PIN) # Optional Wifi LED

        prevLightStatus = None
        prevPiA = None
        prevPiC = None

        # Give some time for any retained messages to show up
        time.sleep(1)

        while True:
            if prevLightStatus != client.lightStatus or prevPiA != client.piA or prevPiC != client.piC:
                GPIO.output(LIGHT_STATUS_PIN, client.lightStatus)
                GPIO.output(PI_A_PIN, client.piA)
                GPIO.output(PI_C_PIN, client.piC)


            # Check if the button was pressed
            if wifiBtn.checkState() == mygpio.BTN_PRESS:
                if wifi.isWifiEnabled(): # Disable Wifi
                    wifi.disableWifi()
                    mygpio.turnOff(mygpio.WIFI_LIGHT_PIN) # Optional Wifi LED
                    mygpio.turnOff(mygpio.CONN_LIGHT_PIN) # Optional Conn LED
                    clientRunning = False
                else: # Enable Wifi
                    wifi.enableWifi() 
                    mygpio.turnOn(mygpio.WIFI_LIGHT_PIN) # Optional Wifi LED    
                    if client.isConnected(): # Was the client connected before Wifi was shutdown
                        mygpio.turnOn(mygpio.CONN_LIGHT_PIN) # Optional Wifi LED
                        clientRunning = True      

            # If wifi is enabled, check the state of the conn button
            if wifi.isWifiEnabled():
                # Check if the conn button was pressed
                if connBtn.checkState() == mygpio.BTN_PRESS:
                    if client.isConnected(): # Disconnect
                        client.disconnect()
                        mygpio.turnOff(mygpio.CONN_LIGHT_PIN) # Optional Conn LED
                        clientRunning = False
                    else: # Connect
                        client.connect()
                        mygpio.turnOn(mygpio.CONN_LIGHT_PIN) # Optional Conn LED
                        clientRunning = True

            time.sleep(.005) # Needed to catch the Keyboard Interrupt

    except KeyboardInterrupt:
        GPIO.cleanup()
        client.disconnect()    
        quit()

from client import Client
import json
import time
import RPi.GPIO as GPIO
import PiStatus

class PiAClient(Client):
    def on_message(self, client, userdata, msg):
        topic = str(msg.topic)
        payload = str(msg.payload.decode("utf-8"))

        if topic == 'lightSensor':
            self.publishedLightSensor = payload
        elif topic == 'threshold':
            self.publishedThreshold = payload

        print ("Received Topic: " + topic + ", Value: " + payload)

def updateLightSensor(client, newValue, deltaThreshold):
    if client.publishedLightSensor == None:
        client.publish("lightSensor", payload=str(newValue))
        client.publishedLightSensor = str(newValue)
    elif abs(float(newValue) - float(client.publishedLightSensor)) > deltaThreshold:
        client.publish("lightSensor", payload=str(newValue))
        client.publishedLightSensor = str(newValue)

def updateThreshold(client, newValue, deltaThreshold):
    if client.publishedThreshold == None:
        client.publish("threshold", payload=str(newValue))
        client.publishedThreshold = str(newValue)
    elif abs(float(newValue) - float(client.publishedThreshold)) > deltaThreshold:
        client.publish("threshold", payload=str(newValue))
        client.publishedThreshold = str(newValue)


if __name__ == "__main__":

    f = open('../properties.json')
    properties = json.load(f)
    BROKER_ADDR = properties['BROKER_ADDR']
    BROKER_PORT = properties['BROKER_PORT']

    try:
        client = PiAClient(BROKER_ADDR, BROKER_PORT, 'RaspberryPiA')
        client.setStatusWill("status/RaspberryPiA")
        client.connect()
        client.publishedLightSensor = None
        client.publishedThreshold = None

        client.publish("status/RaspberryPiA", payload='online')
        client.subscribe("lightSensor")
        client.subscribe("threshold")

        # Give some time for any retained messages to show up
        time.sleep(1)

        while True:
            # ls = input("Please enter a light sensor value [0,1]:\n")
            # updateLightSensor(client, ls, 0.01)
            # th = input("Please enter a threshold value [0,1]:\n")
            # updateThreshold(client, th, 0.01)
            
            PiStatus.setupWifiButton(client)
            PiStatus.setupConnButton(client)
            
            # light = getLightValue()
            # client.publish("lightSensor", payload='1')
            # client.publish("threshold", payload='1')
    except KeyboardInterrupt as e:
        print("Graceful Disconnect.")
        client.disconnect()
        GPIO.cleanup()
        quit()           

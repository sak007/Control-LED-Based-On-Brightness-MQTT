from client import Client
import json
import time
import RPi.GPIO as GPIO
import PiStatus
from adc import ADC

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
    adc = ADC()
    try:
        client = PiAClient(BROKER_ADDR, BROKER_PORT, 'RaspberryPiA')
        client.setStatusWill("status/RaspberryPiA")
        client.setOnConnectMessage('status/RaspberryPiA', 'online')
        client.setOnGracefulDisconnectMessage('status/RaspberryPiA', 'offline')
        client.connect()
        client.publishedLightSensor = None
        client.publishedThreshold = None

        client.subscribe("lightSensor")
        client.subscribe("threshold")

        while True:
            ls = adc.read(0)
            updateLightSensor(client, ls, 100)
            th = adc.read(1)
            updateThreshold(client, th, 100)

            PiStatus.setupWifiButton(client)
            PiStatus.setupConnButton(client)

            # light = getLightValue()
            # client.publish("lightSensor", payload='1')
            # client.publish("threshold", payload='1')
    except KeyboardInterrupt as e:
        client.disconnect()
        GPIO.cleanup()
        quit()

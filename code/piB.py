from client import Client
import time
import RPi.GPIO as GPIO
import json

LIGHT_STATUS_PIN = 11
PI_A_PIN = 13
PI_C_PIN = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LIGHT_STATUS_PIN, GPIO.OUT)
GPIO.setup(PI_A_PIN, GPIO.OUT)
GPIO.setup(PI_C_PIN, GPIO.OUT)



class PiBClient(Client):

    def on_message(self, client, userdata, msg):
        topic = str(msg.topic)
        payload = str(msg.payload.decode("utf-8"))
        if topic == 'lightStatus':
            if payload == 'TurnOn':
                self.lightStatus = True
            else:
                self.lightStatus = False
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
        else:
            print("Topic:" + topic)
            print("Received:" + payload)


if __name__ == "__main__":

    f = open('../properties.json')
    properties = json.load(f)
    BROKER_ADDR = properties['BROKER_ADDR']
    BROKER_PORT = properties['BROKER_PORT']
    client = PiBClient(BROKER_ADDR, BROKER_PORT)
    client.lightStatus = 0
    client.piA = 0
    client.piC = 0
    client.connect()


    client.subscribe("lightStatus")
    client.subscribe("status/RaspberryPiA")
    client.subscribe("status/RaspberryPiC")

    while True:
        try:
            print(client.lightStatus, client.piA, client.piC)
            GPIO.output(LIGHT_STATUS_PIN, client.lightStatus)
            GPIO.output(PI_A_PIN, client.piA)
            GPIO.output(PI_C_PIN, client.piC)
        except KeyboardInterrupt:
            GPIO.cleanup()

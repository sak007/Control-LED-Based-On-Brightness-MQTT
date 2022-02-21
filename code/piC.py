from client import Client
import json

class PiCClient(Client):
    def on_message(self, client, userdata, msg):
        if str(msg.topic) == 'lightSensor':
            self.lightSensor = msg.payload.decode("utf-8")
        elif str(msg.topic) == 'threshold':
            self.threshold = mdg.payload.decode("utf-8")
        elif str(msg.topic) == 'lightStatus':
            self.oldLightStatus = str(msg.payload.decode("utf-8"))
        else:
            print("Topic:" + str(msg.topic))
            print("Received:" + str(msg.payload))

def updateLightStatus(client):
    if client.lightSensor >= client.threshold:
        if client.oldLightStatus != 'TurnOn':
            client.publish("lightStatus", payload='TurnOn')
    else:
        if client.oldLightStatus != 'TurnOff':
            client.publish("lightStatus", payload='TurnOff')
    client.lightSensor = None
    client.threshold = None

if __name__ == "__main__":

    f = open('../properties.json')
    properties = json.load(f)
    BROKER_ADDR = properties['BROKER_ADDR']
    BROKER_PORT = properties['BROKER_PORT']
    client = PiCClient(BROKER_ADDR, BROKER_PORT)
    # client.on_message = on_message
    client.setStatusWill("status/RaspberryPiC")
    client.connect()
    client.publish("status/RaspberryPiC", payload='online')
    client.subscribe("lightSensor")
    client.subscribe("threshold")
    client.subscribe("lightStatus")

    client.lightSensor = None
    client.threshold = None
    client.lightStatus = None
    client.oldLightStatus = None


    while True:
        if client.lightSensor != None and client.threshold != None:
            updateLightStatus(client)

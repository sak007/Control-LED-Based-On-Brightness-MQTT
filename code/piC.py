from client import Client
import json
import time

class PiCClient(Client):
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

def updateLightStatus(client):
    if client.lightSensor != None and client.threshold != None:
        if (client.lightSensor >= client.threshold) and client.lightStatus != 'TurnOn':
            client.lightStatus = 'TurnOn'
            client.publish("lightStatus", payload=client.lightStatus)
        elif (client.lightSensor < client.threshold) and client.lightStatus != 'TurnOff':
            client.lightStatus = 'TurnOff'
            client.publish("lightStatus", payload=client.lightStatus)

if __name__ == "__main__":

    f = open('../properties.json')
    properties = json.load(f)
    BROKER_ADDR = properties['BROKER_ADDR']
    BROKER_PORT = properties['BROKER_PORT']

    client = PiCClient(BROKER_ADDR, BROKER_PORT, 'RaspberryPiC')
    client.setStatusWill("status/RaspberryPiC")
    client.connect()

    client.lightSensor = None
    client.threshold = None
    client.lightStatus = None

    client.publish("status/RaspberryPiC", payload='online')
    client.subscribe("lightStatus")
    client.subscribe("lightSensor")
    client.subscribe("threshold")

    # Give some time for any retained messages to show
    time.sleep(1)

    while True:
        try:
            updateLightStatus(client)
        except KeyboardInterrupt:
            print("Graceful Disconnect.")
            client.disconnect()
            quit()

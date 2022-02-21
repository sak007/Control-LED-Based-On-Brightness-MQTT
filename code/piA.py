from client import Client
import json

class PiAClient(Client):
    def on_message(self, client, userdata, msg):
        topic = str(msg.topic)
        payload = str(msg.payload.decode("utf-8"))
        if topic == 'lightSensor':
            self.oldLightSensor = payload
        elif topic == 'threshold':
            self.oldThreshold = threshold
        else:
            print("Topic:" + topic)
            print("Received:" + payload)

if __name__ == "__main__":

    f = open('../properties.json')
    properties = json.load(f)
    BROKER_ADDR = properties['BROKER_ADDR']
    BROKER_PORT = properties['BROKER_PORT']
    client = PiAClient(BROKER_ADDR, BROKER_PORT)
    # client.on_message = on_message
    client.setStatusWill("status/RaspberryPiA")
    client.connect()
    client.publish("status/RaspberryPiA", payload='online')

    client.subscribe("lightSensor")
    client.subscribe("threshold")

    while True:
        # light = getLightValue()
        # client.publish("lightSensor", payload='1')
        # client.publish("threshold", payload='1')
        pass

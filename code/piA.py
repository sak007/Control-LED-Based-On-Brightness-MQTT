from client import Client

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

    client = PiAClient('localhost', 1883)
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

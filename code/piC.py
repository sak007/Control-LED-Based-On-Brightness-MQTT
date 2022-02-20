from client import Client

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

def updateLightStatus():
    if lightSensor >= threshold:
        if oldLightStatus != 'TurnOn':
            client.publish("lightStatus", payload='TurnOn')
    else:
        if oldLightStatus != 'TurnOff':
            client.publish("lightStatus", payload='TurnOff')
    lightSensor = None
    threshold = None

if __name__ == "__main__":

    client = PiCClient('localhost', 1883)
    # client.on_message = on_message
    client.setStatusWill("status/RaspberryPiC")
    client.connect()
    client.publish("status/RaspberryPiC", payload='online')
    client.subscribe("lightSensor")
    client.subscribe("threshold")
    client.subscribe("lightStatus")

    global lightSensor
    lightSensor = None
    global threshold
    threshold = None
    global lightStatus
    lightStatus = None
    global oldLightStatus
    oldLightStatus = None


    while True:
        if lightSensor != None and threshold != None:
            updateLightStatus()

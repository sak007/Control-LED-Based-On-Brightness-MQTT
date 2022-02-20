from client import Client

class LoggerClient(Client):
    def on_message(self, client, userdata, msg):
        print("Topic:" + str(msg.topic))
        print("Received:" + str(msg.payload.decode("utf-8")))

if __name__ == "__main__":

    client = LoggerClient('localhost', 1883)
    # client.on_message = on_message
    client.connect()

    client.subscribe("lightSensor")
    client.subscribe("threshold")
    client.subscribe("lightStatus")
    client.subscribe("status/RaspberryPiA")
    client.subscribe("status/RaspberryPiC")

    while True:
        pass

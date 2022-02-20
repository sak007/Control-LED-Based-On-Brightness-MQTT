from client import Client
import time
# import RPi.GPIO as GPIO

# LIGHT_STATUS_PIN = 11
# PI_A_PIN = 13
# PI_B_PIN = 15

# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(LIGHT_STATUS_PIN, GPIO.OUT)
# GPIO.setup(13, GPIO.OUT)
# GPIO.setup(15, GPIO.OUT)



class PiBClient(Client):

    def on_message(self, client, userdata, msg):
        topic = str(msg.topic)
        payload = str(msg.payload.decode("utf-8"))
        if topic == 'lightStatus':
            if payload == 'TurnOn':
                self.lightStatus = 1
            else:
                self.lightStatus = 0
        elif topic == 'status/RaspberryPiA':
            if payload == 'online':
                self.piA = 1
            else:
                # print(payload)
                # time.sleep(5)
                self.piA = 0
        elif topic == 'status/RaspberryPiC':
            if payload == 'online':
                self.piB = 1
            else:
                self.piB = 0
        else:
            print("Topic:" + topic)
            print("Received:" + payload)

        # print(self.lightStatus, self.piA, self.piB)
        # time.sleep(5)

if __name__ == "__main__":

    client = PiBClient('localhost', 1883)
    # client.on_message = on_message
    client.lightStatus = 0
    client.piA = 0
    client.piB = 0
    client.connect()


    client.subscribe("lightStatus")
    client.subscribe("status/RaspberryPiA")
    client.subscribe("status/RaspberryPiC")

    while True:
        # try:
            print(client.lightStatus, client.piA, client.piB)
            # GPIO.output(LIGHT_STATUS_PIN, lightStatus)
            # GPIO.output(PI_A_PIN, piA)
            # GPIO.output(PI_B_PIN, piB)
        # except KeyboardInterrupt:
        #         # GPIO.cleanup()

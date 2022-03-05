from client import Client
import json
import os
import datetime
from os.path import exists as file_exists

class LoggerClient(Client):
    def on_message(self, client, userdata, msg):
        check_if_exists = file_exists('logs.csv' )
        if(check_if_exists):
            f = open("logs.csv", "a")
        
        else:
            f = open("logs.csv", "w")
            f.write('Timestamp, Topic, Payload \n')
        
        f.write(str(datetime.datetime.now()) + "," + str(msg.topic) + "," + str(msg.payload.decode("utf-8")) + "\n")
        print("Topic:" + str(msg.topic))
        print("Received:" + str(msg.payload.decode("utf-8")))
        f.close()

if __name__ == "__main__":
    f = open('../properties.json')
    properties = json.load(f)
    BROKER_ADDR = properties['BROKER_ADDR']
    BROKER_PORT = properties['BROKER_PORT']
    client = LoggerClient(BROKER_ADDR, BROKER_PORT)
    # client.on_message = on_message
    client.connect()

    client.subscribe("lightSensor")
    client.subscribe("threshold")
    client.subscribe("lightStatus")
    client.subscribe("status/RaspberryPiA")
    client.subscribe("status/RaspberryPiC")

    while True:
        pass

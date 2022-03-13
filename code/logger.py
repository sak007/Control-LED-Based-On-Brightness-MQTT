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
        
        check_if_new_exists = file_exists('logs1.csv' )
        if(check_if_new_exists):
            f1 = open("logs1.csv", "a")

        else:
            f1 = open("logs1.csv", "w")
            f1.write('Timestamp, Topic, Payload \n')

        if(str(msg.topic) == 'lightStatus'):
            f1.write(str(datetime.datetime.now()) + "," + str(msg.topic) + "," + str(msg.payload.decode("utf-8")) + "\n")
       
        f.write(str(datetime.datetime.now()) + "," + str(msg.topic) + "," + str(msg.payload.decode("utf-8")) + "\n")
            
        print("Topic:" + str(msg.topic))
        print("Received:" + str(msg.payload.decode("utf-8")))
        f.close()
        f1.close()

if __name__ == "__main__":
    f = open('../properties.json')
    properties = json.load(f)
    BROKER_ADDR = properties['BROKER_ADDR']
    BROKER_PORT = properties['BROKER_PORT']
    BROKER_USERNAME = properties['BROKER_USERNAME']
    BROKER_PASSWORD = properties['BROKER_PASSWORD']
    client = LoggerClient(BROKER_ADDR, BROKER_PORT, 'Logger', BROKER_USERNAME, BROKER_PASSWORD)
    client = LoggerClient(BROKER_ADDR, BROKER_PORT, 'Logger', BROKER_USERNAME, BROKER_PASSWORD)
    # client.on_message = on_message
    client.connect()

    client.subscribe("lightSensor")
    client.subscribe("threshold")
    client.subscribe("lightStatus")
    client.subscribe("status/RaspberryPiA")
    client.subscribe("status/RaspberryPiC")

    while True:
        pass

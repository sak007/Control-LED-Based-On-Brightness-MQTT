import paho.mqtt.client as mqtt #pip3 install paho-mqtt
import argparse
import os
import sys
import math
import time
import ntplib #pip3 install ntplib
from queue import Queue

class Client:

    def __init__(self, bkr_addr, bkr_port):
        self.bkr_addr = bkr_addr
        self.bkr_port = bkr_port
        self.client = mqtt.Client()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.is_connected_flag = True

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed with QOS: " + str(granted_qos[0]))
        self.client.is_subscribed_flag = True

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print("Topic:" + str(msg.topic))
        print("Received:" + str(msg.payload))

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        # client.on_publish = on_publish


        try:
            self.client.is_connected_flag = False
            self.client.connect(self.bkr_addr, self.bkr_port)
            self.client.loop_start()
            while not self.client.is_connected_flag:
                continue
        except:
            print("Could not connect to MQTT broker: " + self.bkr_addr + ":" + str(self.bkr_port))
            sys.exit()

    def setStatusWill(self, topic):
        self.client.will_set(topic, payload='offline', qos=2, retain=True)

    def publish(self, topic, payload):
        self.client.publish(topic, payload=payload, qos=2, retain=True)

    def subscribe(self, topic):
        self.client.is_subscribed_flag = False
        self.client.subscribe(topic, 2)
        while not self.client.is_subscribed_flag:
            continue

if __name__ == "__main__":

    client = Client('localhost', 1883)

    client.setStatusWill("status/RaspberryPiA")
    client.connect()
    client.publish("status/RaspberryPiA", payload='online')

    client.subscribe("lightSensor")

    while True:
        # light = getLightValue()
        client.publish("lightSensor", payload='1')

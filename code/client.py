import paho.mqtt.client as mqtt #pip3 install paho-mqtt
import os
import time

class Client:

    def __init__(self, bkr_addr, bkr_port, client_id=None):
        self.bkr_addr = bkr_addr
        self.bkr_port = bkr_port
        self.on_connect_topic = None
        self.on_connect_payload = None
        self.on_disconnect_topic = None
        self.on_disconnect_payload = None
        self.publish_in_proc = 0

        if client_id == None:
            self.client = mqtt.Client()
        else:
            self.client = mqtt.Client(client_id = client_id,clean_session=False)
        self.status = False
        self.wifiStatus = self.getWifiStatus()

    def on_connect(self, client, userdata, flags, rc):
        self.status = True
        print("Connected with result code "+str(rc))
        self.client.is_connected_flag = True

        # If a connect message has been set, publish it
        if self.on_connect_topic != None and self.on_connect_payload != None:
            self.publish(self.on_connect_topic, self.on_connect_payload)

    def on_disconnect(self, client, userdata, rc):
        self.status = False
        print("Disconnected with result code "+str(rc))
        self.client.loop_stop()

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed with QOS: " + str(granted_qos[0]))
        self.client.is_subscribed_flag = True

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print("Topic:" + str(msg.topic))
        print("Received:" + str(msg.payload))

    def on_publish(self, client, userdata, msg):
        if self.publish_in_proc > 0:
            self.publish_in_proc -= 1

    def disconnect(self):
        self.client.disconnect()

    def gracefulDisconnect(self):
        # If a disconnect message has been set, publish it
        if self.on_disconnect_topic != None and self.on_disconnect_payload != None:
            self.publish(self.on_disconnect_topic, self.on_disconnect_payload)

        # Before finishing disconnect, we need to ensure all in process publish
        # messages have been sent successfully. For example, the offline status
        # message.
        if self.publish_in_proc > 0:
            start_time = time.time()
            seconds = 5
            print("Waiting for in process publishes to complete (5 sec max)...")
            while self.publish_in_proc > 0:
                current_time = time.time()
                elapsed_time = current_time - start_time
                if elapsed_time > seconds:
                    print("Timer expired, forcing disconnect.")
                    break
            if self.publish_in_proc == 0:
                print("All in process publishes completed successfully.")
        self.disconnect()

    def forceLastWillDisconnect(self):
        # Do something different here if we don't really want to terminate the script
        quit()

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.publish_in_proc = 0
        
        try:
            self.client.is_connected_flag = False
            self.client.connect(self.bkr_addr, self.bkr_port)
            self.client.loop_start()
            while not self.client.is_connected_flag:
                continue
        except Exception as e:
            print(e)
            print("Could not connect to MQTT broker: " + self.bkr_addr + ":" + str(self.bkr_port))
            raise e

    def setOnConnectMessage(self, topic, payload):
        self.on_connect_topic = topic
        self.on_connect_payload = payload

    def setOnGracefulDisconnectMessage(self, topic, payload):
        self.on_disconnect_topic = topic
        self.on_disconnect_payload = payload

    def setStatusWill(self, topic):
        self.client.will_set(topic, payload='offline', qos=2, retain=True)

    def publish(self, topic, payload):
        print ("Published Topic: " + topic + ", Value: " + payload)
        self.publish_in_proc += 1
        self.client.publish(topic, payload=payload, qos=2, retain=True)

    def subscribe(self, topic):
        print("Subscribed to topic:" + topic)
        self.client.is_subscribed_flag = False
        self.client.subscribe(topic, 2)
        while not self.client.is_subscribed_flag:
            continue
        
    def getWifiStatus(self):
        self.wifiStatus = 1 if (os.system('iwgetid > /dev/null') == 0) else 0
        return self.wifiStatus

    def toggleWifi(self):
        option = not self.wifiStatus
        state = 'up' if option else 'down'
        cmd = 'sudo ifconfig wlan0 ' + state
        os.system(cmd)
        while(option != self.getWifiStatus()):
            continue
        
    def getStatus(self):
        return 1 if self.status else 0
        
    def toggleConnection(self):
        s = self.status
        if self.status:
            self.disconnect()
        else:
            self.connect()
        time.sleep(1)        
        while s == self.status:
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

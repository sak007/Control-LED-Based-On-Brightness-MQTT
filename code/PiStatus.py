import RPi.GPIO as GPIO

CONN_PIN = 37
WIFI_PIN = 35
CONN_LIGHT_PIN = 33
WIFI_LIGHT_PIN = 31

GPIO.setmode(GPIO.BOARD)
GPIO.setup(CONN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(WIFI_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(CONN_LIGHT_PIN, GPIO.OUT)
GPIO.setup(WIFI_LIGHT_PIN, GPIO.OUT)


def setupWifiButton(client):
    if GPIO.input(WIFI_PIN):
        print("WIFI Toggle")
        client.toggleWifi()
    GPIO.output(WIFI_LIGHT_PIN, client.wifiStatus)


def setupConnButton(client):
    if GPIO.input(CONN_PIN):
        print("Connection Toggle")
        client.toggleConnection()
    GPIO.output(CONN_LIGHT_PIN, client.status and client.wifiStatus)

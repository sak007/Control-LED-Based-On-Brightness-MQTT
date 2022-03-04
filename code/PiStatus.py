import RPi.GPIO as GPIO

CONN_PIN = 37
WIFI_PIN = 35
CRASH_PIN = 29
CONN_LIGHT_PIN = 33
WIFI_LIGHT_PIN = 31

GPIO.setmode(GPIO.BOARD)
GPIO.setup(CONN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(WIFI_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(CRASH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(CONN_LIGHT_PIN, GPIO.OUT)
GPIO.setup(WIFI_LIGHT_PIN, GPIO.OUT)

prevWifiButtonState = 0
prevConnButtonState = 0
prevCrashButtonState = 0

def setupWifiButton(client):
    global prevWifiButtonState
    if GPIO.input(WIFI_PIN) and not prevWifiButtonState:
        print("WIFI Toggle")
        client.toggleWifi()
    GPIO.output(WIFI_LIGHT_PIN, client.wifiStatus)
    prevWifiButtonState = GPIO.input(WIFI_PIN)


def setupConnButton(client):
    global prevConnButtonState
    if GPIO.input(CONN_PIN) and not prevConnButtonState:
        print("Connection Toggle")
        client.toggleConnection()
    GPIO.output(CONN_LIGHT_PIN, client.status and client.wifiStatus)
    prevConnButtonState = GPIO.input(CONN_PIN)


def setupCrashButton(client):
    global prevCrashButtonState
    if GPIO.input(CRASH_PIN) and not prevCrashButtonState:
        print("Crash!")
        GPIO.cleanup()
        client.forceLastWillDisconnect()
    prevCrashButtonState = GPIO.input(CRASH_PIN)

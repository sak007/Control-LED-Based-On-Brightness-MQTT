import RPi.GPIO as GPIO
import os
import time
import wifi

CONN_PIN = 37
WIFI_PIN = 35
CONN_LIGHT_PIN = 33
WIFI_LIGHT_PIN = 31

BTN_NO_CHANGE = 0
BTN_RELEASE = 1
BTN_PRESS = 2

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(CONN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(WIFI_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(CONN_LIGHT_PIN, GPIO.OUT) # Optional
    GPIO.setup(WIFI_LIGHT_PIN, GPIO.OUT) # Optional


class Button:
    # debounceTime is the time to sleep after a button release is detected, this prevents
    # the debounce effect, where the reading switches between low and high before finally settling
    # at low, only occurs on for button release using Radek's buttons
    def __init__(self, pin, debounceTime=.2):
        self.pin = pin
        self.lastState = GPIO.input(pin) # Track the last state of the button
        self.debounceTime = .2
    
    # Checks the state of the button and compares it to the last checked state
    # If the state has not changed, then we are waiting for button release or press,
    # If the state goes from high to low, then the button was released, 
    # If the state goes from low to high, then the button was pressed
    # Return True if button was pressed, False if the state has not changed or reset back to low
    def checkState(self):
        curState = GPIO.input(self.pin) # No change since last check
        if curState == self.lastState: 
            return BTN_NO_CHANGE
        elif curState == GPIO.LOW: # Hi -> Low, button release
            self.lastState = curState
            time.sleep(self.debounceTime)
            return BTN_RELEASE
        else: # Low -> Hi, btn press
            self.lastState = curState
            return BTN_PRESS

def turnOn(pin):
    GPIO.output(pin, GPIO.HIGH)
def turnOff(pin):
    GPIO.output(pin, GPIO.LOW)

def handleWifiButton(wifiBtn, client, lastState):
    # Check if the button was pressed
    if wifiBtn.checkState() == BTN_PRESS:
        if wifi.isWifiEnabled(): # Disable Wifi
            wifi.disableWifi()
            turnOff(WIFI_LIGHT_PIN) # Optional Wifi LED
            turnOff(CONN_LIGHT_PIN) # Optional Conn LED
            return False
        else: # Enable Wifi
            wifi.enableWifi() 
            turnOn(WIFI_LIGHT_PIN) # Optional Wifi LED    
            if client.isConnected(): # Was the client connected before Wifi was shutdown
                turnOn(CONN_LIGHT_PIN) # Optional Wifi LED
                return True
    return lastState # no change

def handleConnBtn(connBtn, client, lastState):
    # If wifi is enabled, check the state of the conn button
    if wifi.isWifiEnabled():
        # Check if the conn button was pressed
        if connBtn.checkState() == BTN_PRESS:
            if client.isConnected(): # Disconnect
                client.disconnect()
                turnOff(CONN_LIGHT_PIN) # Optional Conn LED
                clientRunning = False
                return False
            else: # Connect
                client.connect()
                turnOn(CONN_LIGHT_PIN) # Optional Conn LED
                clientRunning = True
                return True
    return lastState # no change

# Upon reconnecting wifi, sometimes the client will also reconnect, but seconds
# later, this will catch that and adjust the state and fix the light
# Also detects if mqtt connection drops in cases other than intentionall
# button presses
def handleConnDiscrepencies(client, lastState):
    # Fires after delayed mqtt client reconnection after wifi reconnects
    if lastState == False and wifi.isWifiEnabled() and client.isConnected():
        turnOn(CONN_LIGHT_PIN) # Optional Conn LED
        return True
    # Might fire in the case of broker disconnect?
    elif lastState == True and not client.isConnected():
        turnOff(CONN_LIGHT_PIN) # Optional Conn LED
        return False
    else:
        return lastState

####################### Test Functions Below #######################

# def setupWifiButton(client):
#     state = False
#     if GPIO.input(WIFI_PIN):
#         print("WIFI Toggle")
#         state = True
#         #client.toggleWifi()
#     #GPIO.output(WIFI_LIGHT_PIN, client.wifiStatus)
#     return state


# def setupConnButton(client):
#     if GPIO.input(CONN_PIN):
#         print("Connection Toggle")
#         #client.toggleConnection()
#     GPIO.output(CONN_LIGHT_PIN, client.status and client.wifiStatus)

# Tests button functionality
def main():
    setup()
    i = 0
    #btn = Button(WIFI_PIN)
    btn = Button(CONN_PIN)
    try:
        while True:
            btnCode = btn.checkState()
            if btnCode == BTN_RELEASE:
                print(i, "Btn released")
            if btnCode == BTN_PRESS:
                print(i, "Btn pressed")
                i+=1
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()



    


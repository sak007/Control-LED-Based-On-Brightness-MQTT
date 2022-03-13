import os
import time


def isWifiEnabled():
    if (os.system('iwgetid > /dev/null') == 0):
        return True
    return False

# Blocks until wifi is enabed by default, ~10 seconds
def enableWifi(block=True):
    cmd = 'sudo ifconfig wlan0 up' 
    os.system(cmd)
    if block: # Block until wifi is enabled
        while isWifiEnabled() != True:
            time.sleep(.01)

# Blocks until wifi is disabled by default, ~1 seconds
def disableWifi(block=True):
    cmd = 'sudo ifconfig wlan0 down' 
    os.system(cmd)
    if block: # Block until wifi is disabled
        while isWifiEnabled() != False:
            time.sleep(.01)

####################### Test Functions Below #######################

# Tests the wifi enabled and disable command
# Wifi connected -> disable -> sleep -> enable -> end
def main():
    # Wait for Wifi to be connected
    while isWifiEnabled() != True:
        time.sleep(1)
    print("Wifi is connected")
    time.sleep(3)

    # Disable Wifi
    print("Disabling Wifi")
    runtime = time.time()
    disableWifi()
    runtime = time.time() - runtime
    print("Wifi disabled after %f seconds" % runtime)

    time.sleep(3)
    
    # Enable wifi
    print("Enabling Wifi")
    runtime = time.time()
    enableWifi()
    runtime = time.time() - runtime
    print("Wifi Enabled afted %f seconds" % runtime)

    print("End")

if __name__ == "__main__":
    main()
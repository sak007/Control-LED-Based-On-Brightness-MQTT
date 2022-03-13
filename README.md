# IOT_HW3

## Content

|Title|Hyperlink|
|-|-|
|Layout| [Click here](#layout)|
|Functionalities| [Click here](#functionalities)|
|Setup Instructions| [Click here](#setup-instructions)|


## Layout
  - [TODO]

## Functionalities

### Broker
  - [TODO]
  
### RaspberryPiA

### RaspberryPiB
  - [TODO]

### RaspberryPiC
  - [TODO]

### Laptop 2 [Logger]
  - [TODO]

## Setup Instructions

### Broker

 - Start the broker in Laptop 1 (mosquitto mqtt)
 - Note the IP address of the broker
 - Update the broker address field in properties.json in all the devices.
 - **Note: Do not push the broker ip in the repo if you are using NAT**

### RaspberryPiA
 - Connect LDR, Potentiometer and ADC to RaspberryPi as per the following circuit diagram.
 - Test all subfunctions:
   - Confirm ADC is functioning via `python3 code/adc.py`
     - `testRawRead()` to test raw readings for the LDR and POT
     - `minMaxReader(channel)` to find min and max ADC vals for connected channels for scaling and set the scale vals
     - `testScaledRead()` to test scaled ADC readings
   - Confirm wifi and connection buttons are functioning via `python3 code/mygpio.py`
     - set button in `main()`
   - Confirm wifi can be enabled/disabled via `python3 code/wifi.py`
   - Confirm MQTT client works via `python3 client.py`
 - Run piA code via `python3 piA.py`
 
 ### RaspberryPiC
 - Checkout the repo in RaspberryPiC
 - From repo home run,
 [use 'python3' if python points to python2]
 ```
 python code/piC.py
 ```
 
 ### RaspberryPiB
 - Connect LEDs, and Resistors to RaspberryPi as per the following circuit diagram.
 - [TODO]
 - Checkout the repo in RaspberryPiB
 - From repo home run,
 [use 'python3' if python points to python2]
 ```
 python code/piB.py
 ```
 ### Laptop 2 [Logger]
  - Checkout the repo in Laptop
  - From repo home run,
  [use 'python3' if python points to python2]
  ```
  python code/logger.py
  ```

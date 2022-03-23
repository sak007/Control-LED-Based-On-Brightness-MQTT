# IOT_HW3

## Setup Instructions

### Laptop 1 [MQTT Broker]

 - Create the username and password hash file by executing the following command in the mqtt_broker_conf/ folder `sh gen_password.sh`. You should see a file called client_password.txt has been created
 - From the mqtt_broker_conf/ folder, start the broker on Laptop 1 referencing the supplied .conf file ex: `/usr/local/sbin/mosquitto -c mosquitto.conf`
 - Note the IP address of the broker
 - Update the BROKER_ADDR field in properties.json on all the other devices (i.e. piA, piB, piC and logger).
 - **Note: Do not push the broker ip in the repo if you are using NAT**

### Laptop 2 [Logger]

 - From the /code folder, run logger code via `python3 logger.py`
 - The full log file with all required results will be written to: logs.csv
 - A log file showing only lightStatus changes will be written to: logs1.csv

### RaspberryPiA

 - Connect the required components (Buttons, LED's, Resistors, LDR, Potentiometer and ADC) to RaspberryPi as per the schematics submitted with the assignment.
 - If not already installed, installed the paho-mqtt package, ex: `pip install paho-mqtt`
 - Test all subfunctions:
   - Confirm ADC is functioning via `python3 code/adc.py`
     - `testRawRead()` to test raw readings for the LDR and POT
     - `minMaxReader(channel)` to find min and max ADC vals for connected channels for scaling and set the scale vals
     - `testScaledRead()` to test scaled ADC readings
   - Confirm wifi and connection buttons are functioning via `python3 code/mygpio.py`
     - set button in `main()`
   - Confirm wifi can be enabled/disabled via `python3 code/wifi.py`
   - Confirm MQTT client works via `python3 client.py`
 - From the code/ folder, run piA code via `python3 piA.py`
 
### RaspberryPiB

 - Connect the required components (Resistors and  LED's) to RaspberryPi as per the schematics submitted with the assignment.
 - If not already installed, installed the paho-mqtt package, ex: `pip install paho-mqtt`
 - From the code/ folder, run piB code via `python3 piB.py`

### RaspberryPiC

 - Connect the required components (Buttons, Resistors and LED's) to RaspberryPi as per the schematics submitted with the assignment.
 - If not already installed, installed the paho-mqtt package, ex: `pip install paho-mqtt`
 - From the code/ folder, run piC code via `python3 piC.py`
 
# IOT_HW3

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![version](https://img.shields.io/badge/version-3.0-blue)](https://github.com/sak007/Control-LED-Based-On-Brightness-MQTT/releases/tag/v3.0)
[![DOI](https://zenodo.org/badge/461343040.svg)](https://zenodo.org/badge/latestdoi/461343040)
[![GitHub issues](https://img.shields.io/github/issues/sak007/Control-LED-Based-On-Brightness-MQTT)](https://github.com/sak007/Control-LED-Based-On-Brightness-MQTT/issues?q=is%3Aopen+is%3Aissue)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/sak007/Control-LED-Based-On-Brightness-MQTT)](https://github.com/sak007/Control-LED-Based-On-Brightness-MQTT/issues?q=is%3Aissue+is%3Aclosed)
[![Github pull requests](https://img.shields.io/github/issues-pr/sak007/Control-LED-Based-On-Brightness-MQTT)](https://github.com/sak007/Control-LED-Based-On-Brightness-MQTT/pulls)
[![Github closed pull requests](https://img.shields.io/github/issues-pr-closed/sak007/Control-LED-Based-On-Brightness-MQTT)](https://github.com/sak007/Control-LED-Based-On-Brightness-MQTT/pulls?q=is%3Apr+is%3Aclosed)

## Setup Instructions

### Laptop 1 [MQTT Broker]

 - Create the username and password hash file by executing the following command in the mqtt_broker_conf/ folder `sh gen_password.sh`. You should see a file called client_password.txt has been created.
 - From the mqtt_broker_conf/ folder, start the broker on Laptop 1 referencing the supplied .conf file ex: `/usr/local/sbin/mosquitto -c mosquitto.conf`
 - Note the IP address of the broker
 - Update the BROKER_ADDR field in properties.json on all the other devices (i.e. piA, piB, piC and logger).
 - **Note: Do not push the broker ip in the repo if you are using NAT**

### Laptop 2 [Logger]

 - From the code/ folder, run logger software via `python3 logger.py`
 - The full log file with all required results will be written to: logs.csv
 - A log file showing only lightStatus changes will be written to: lightStatus.csv

### RaspberryPiA

 - Connect the required components (Buttons, LED's, Resistors, LDR, Potentiometer and ADC) to RaspberryPi as per the schematics submitted with the assignment.
 - Enable SPI and install the paho-mqtt package by executing the following command `sh setup.sh`
 
### RaspberryPiB

 - Connect the required components (Resistors and  LED's) to RaspberryPi as per the schematics submitted with the assignment.
 - If not already installed, install the required packages using requirements.txt, ex: `pip install -r requirements.txt`
 - From the code/ folder, run piB software via `python3 piB.py`

### RaspberryPiC

 - Connect the required components (Buttons, Resistors and LED's) to RaspberryPi as per the schematics submitted with the assignment.
 - If not already installed, install the required packages using requirements.txt, ex: `pip install -r requirements.txt`
 - From the code/ folder, run piC software via `python3 piC.py`

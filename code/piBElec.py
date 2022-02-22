import RPi.GPIO as GPIO
import time

LED1 = 16
LED2 = 20
LED3 = 21

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LED1, GPIO.OUT)
	GPIO.setup(LED2, GPIO.OUT)
	GPIO.setup(LED3, GPIO.OUT)

def turnOff(led):
	GPIO.output(led, 0)

def turnOn(led):
	GPIO.output(led, 1)

def main():
	setup()
	state=0
	try:
		while True:
			if state == 0:
				print("Turning off")
				turnOn(LED1)
				turnOn(LED2)
				turnOn(LED3)
				state = 1
			else:
				print("Turning on")
				turnOff(LED1)
				turnOff(LED2)
				turnOff(LED3)
				state = 0
			time.sleep(3)
	except KeyboardInterrupt:
		GPIO.cleanup()

if __name__ == "__main__":
	main()

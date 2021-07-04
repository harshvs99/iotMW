import RPi.GPIO as GPIO
import configuration as config
import redis

cache=redis.Redis()
cache.set("Magnetron","0")


def mag_door_configure():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(config.DOOR_PIN,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(config.Magnetron_PIN,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
	isDoorOpen = 0
	isMagnetronON = 0

def magnetron_input():
	if GPIO.input(config.Magnetron_PIN) == GPIO.HIGH:
		isMagnetronON = 1
		#print("MagnetronON")
		cache.set("Magnetron","1")
	else:
		isMagnetronON = 0
		#print("MagnetronOFF")
		cache.set("Magnetron","0")

	return isMagnetronON

def door_input():
	if GPIO.input(config.DOOR_PIN) == GPIO.HIGH:
		isDoorOpen = 1
		#print("DOOR OPEN")
	else:
		isDoorOpen = 0
		#print("DOOR CLOSED")

	return isDoorOpen	
	

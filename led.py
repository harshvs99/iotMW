import RPi.GPIO as GPIO
import time
import configuration as config
import redis

cache=redis.Redis()

class indication():
    def __init__(self):
        pass

    def configure(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

    def stop(self):
        pass

    def idle(self):   
        pass

    def heating_on(self):
        pass

    def door_open(self):   
        pass

    def self_check(self):
        pass

    def heating_completed(self):
        pass
    
    def internet_error(self):
        pass

    def sensor_error(self):
        pass

    def emergency(self):
        pass

class led(indication):

    def __init__(self):
        self.timestampatredstart=0
        self.timestampatredstop=0
        self.timestampatgreenstart=0
        self.timestampatgreenstop=0
        self.timestampatledstop=0
        self.timestampatledstart=0

    
    def configure(self):
        indication.configure(self)
        GPIO.setup(config.RED_PIN,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(config.GREEN_PIN,GPIO.OUT,initial=GPIO.LOW)

    def stop(self):
        GPIO.output(config.RED_PIN, GPIO.LOW)
        GPIO.output(config.GREEN_PIN, GPIO.LOW)
    
    def idle(self):
        GPIO.output(config.GREEN_PIN, GPIO.HIGH)
        GPIO.output(config.RED_PIN, GPIO.LOW)

    def heating_paused(self):
        GPIO.output(config.GREEN_PIN, GPIO.HIGH)
        GPIO.output(config.RED_PIN, GPIO.LOW)

    def heating_on(self):
        GPIO.output(config.RED_PIN, GPIO.HIGH)
        GPIO.output(config.GREEN_PIN, GPIO.LOW)

    def door_open(self):   
        GPIO.output(config.RED_PIN, GPIO.HIGH)
        GPIO.output(config.GREEN_PIN, GPIO.LOW)

    def self_check(self):
        GPIO.output(config.RED_PIN, GPIO.HIGH)
        GPIO.output(config.GREEN_PIN, GPIO.HIGH)

    def heating_completed(self):
        GPIO.output(config.GREEN_PIN, GPIO.HIGH)
        GPIO.output(config.RED_PIN, GPIO.LOW)
    
    def internet_error(self):
        #print("HELLO WORLD")
        while(cache.get('CurrentState').decode()=="InternetError" and cache.get("LedOn").decode()=='1'):
            #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            GPIO.output(config.GREEN_PIN, GPIO.LOW)
            self.timestampatredstart=time.time()

            GPIO.output(config.RED_PIN, GPIO.HIGH)
            while(time.time()-self.timestampatredstart<0.5):
                pass

            GPIO.output(config.RED_PIN, GPIO.LOW)
            self.timestampatredstop =time.time()

            while(time.time()-self.timestampatredstop<0.5):
                pass

    def sensor_error(self):
        while(cache.get('CurrentState').decode()=="SensorError" and cache.get("LedOn").decode()=='1'):
            GPIO.output(config.GREEN_PIN, GPIO.LOW) #needs to be red pin being shutdown, instead of green
            self.timestampatgreenstart=time.time()

            GPIO.output(config.GREEN_PIN, GPIO.HIGH)
            while(time.time()-self.timestampatgreenstart<0.5):
                pass

            GPIO.output(config.GREEN_PIN, GPIO.LOW)
            self.timestampatgreenstop =time.time()

            while(time.time()-self.timestampatgreenstop<0.5):
                pass

    def manual_override(self):
        while(cache.get('CurrentState').decode()=="ManualOverride" and cache.get("LedOn").decode()=='1'):
            GPIO.output(config.RED_PIN, GPIO.HIGH)
            GPIO.output(config.GREEN_PIN, GPIO.HIGH)
            self.timestampatledstart=time.time()
            while(time.time()-self.timestampatledstart<0.5):
                pass

            GPIO.output(config.RED_PIN, GPIO.LOW)
            GPIO.output(config.GREEN_PIN, GPIO.LOW)
            self.timestampatledstop =time.time()

            while(time.time()-self.timestampatledstart<0.5):
                pass







    

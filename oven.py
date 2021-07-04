import RPi.GPIO as GPIO
import configuration as config
import time

# Parent Microwave class 
class Microwave():
	def __init__(self):
		pass
	def configure(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(config.START_PIN,GPIO.OUT,initial=GPIO.LOW)
		GPIO.setup(config.TIME_PIN,GPIO.OUT,initial=GPIO.LOW)
		GPIO.setup(config.STOP_PIN,GPIO.OUT,initial=GPIO.LOW)

	def start():
		pass
	def pause():
		pass
	def stop():
		pass
	def isStarted():
		pass
	def isStopped():
		pass

# Butler Class and its implementation
class Butler(Microwave):
	def __init__(self):
		self.isstarted = 0
		self.isstopped = 0
		self.isPaused  = 0
		self.timestampatFirstStartPulse =0
		self.timestampatFirstStopPulse = 0
		self.timestampatFirstStopPulse_1 = 0
		self.timestampatSecondStopPulse =0
		self.timestampafterFirstStopPulse=0
		self.timestampatSecondStopPulse=0
		self.timestampafterpausePulse=0

# Butler Microwave Gpio Configuration
	def configure(self):
		Microwave.configure(self)

# Butler Start 
	def start(self):
		
		if (self.isPaused):     # check before start 
			self.pause()
			self.timestampafterpausePulse=time.time()
			while(True): 
				if(time.time()-self.timestampafterpausePulse>0.25): 
					break
			self.isPaused = 0
			self.timestampafterpausePulse=0

		GPIO.output(config.TIME_PIN,GPIO.HIGH)
		self.timestampatFirstStartPulse=time.time()
		while(True): 
			if(time.time()-self.timestampatFirstStartPulse>0.25): 
				break
		GPIO.output(config.TIME_PIN,GPIO.LOW)
		print("Oven_Started..........")
		self.timestampatFirstStartPulse = 0

		self.isstopped = 0
		self.isstarted = 1
		
	def stop(self):
		
		if (self.isPaused):
		
			GPIO.output(config.STOP_PIN,GPIO.HIGH)
			self.timestampatSecondStopPulse_1=time.time()
		
			while(True): 
				if(time.time()-self.timestampatSecondStopPulse_1>0.25): 
					break
			
			GPIO.output(config.STOP_PIN,GPIO.LOW)

			self.timestampatSecondStopPulse_1 = 0
		
		else:
			GPIO.output(config.STOP_PIN,GPIO.HIGH)
			self.timestampatFirstStopPulse=time.time()
		
			while(True): 
				if(time.time()-self.timestampatFirstStopPulse>0.25): 
					break
		
			GPIO.output(config.STOP_PIN,GPIO.LOW)
			self.timestampafterFirstStopPulse=time.time()
		
			while(True): 
				if(time.time()-self.timestampafterFirstStopPulse>0.25): 
					break
		
			GPIO.output(config.STOP_PIN,GPIO.HIGH)
			self.timestampatSecondStopPulse=time.time()
		
			while(True): 
				if(time.time()-self.timestampatSecondStopPulse>0.25): 
					break
		
		GPIO.output(config.STOP_PIN,GPIO.LOW)
		print("OVEN_Stopped......")
		timestampatFirstStopPulse=0
		timestampafterFirstStopPulse=0
		timestampatSecondStopPulse=0

		self.isPaused = 0
		self.isstopped = 1
		self.isStarted = 0
		
	def pause(self):
		GPIO.output(config.STOP_PIN,GPIO.HIGH)
		self.timestampatFirstStopPulse_1=time.time()
		
		while(True): 
			if(time.time()-self.timestampatFirstStopPulse_1>0.25): 
				break
		
		GPIO.output(config.STOP_PIN,GPIO.LOW)
		print("OVEN_Paused....")

		timestampatFirstStopPulse=0
		self.isPaused = 1
		self.isstopped = 0
		self.isstarted = 0

	def isStarted():
		return self.isstarted 
	
	def isStopped():
		return self.isstopped 


class LG(Microwave):
	def __init__(self):
		self.isstarted = 0
		self.isstopped = 0
		self.isPaused  = 0

		self.timestampatpausePulse=0
		self.timestampattimePulse=0
		self.timestampaftertimePulse=0
		self.timestampafterstartPulse=0
		self.timestampatstopPulse=0
		self.timestampatFirstStopPulse=0
		self.timestampafterFirstStopPulse=0
		self.timestampatSecondStopPulse=0

	def configure(self):
		Microwave.configure(self)

	def start(self):
		
		if (self.isPaused):
			GPIO.output(config.START_PIN,GPIO.HIGH)
			self.timestampatpausePulse=time.time()
		
			while(True): 
				if(time.time()-self.timestampatpausePulse>0.20): 
					break
			
			GPIO.output(config.START_PIN,GPIO.LOW)

		else:
			
			GPIO.output(config.TIME_PIN,GPIO.HIGH)
			self.timestampattimePulse=time.time()
		
			while(True): 
				if(time.time()-self.timestampattimePulse>0.20): 
					break
		
			GPIO.output(config.TIME_PIN,GPIO.LOW)
			self.timestampaftertimePulse=time.time()
		
			while(True): 
				if(time.time()-self.timestampaftertimePulse>0.20): 
					break
		
			GPIO.output(config.START_PIN,GPIO.HIGH)
			self.timestampafterstartPulse=time.time()
		
			while(True): 
				if(time.time()-self.timestampafterstartPulse>0.20): 
					break	

			GPIO.output(config.START_PIN,GPIO.LOW)
		
		print("OVEN_Started......")
		self.timestampatstartPulse=0
		self.timestampattimestartPulse=0
		self.timestampaftertimePulse=0
		self.timestampafterstartPulse=0
		
		self.isPaused = 0
		self.isstopped = 0
		self.isstarted = 1
		
	def stop(self):
		
		if (self.isPaused):
		
			GPIO.output(config.STOP_PIN,GPIO.HIGH)
			self.timestampatstopPulse=time.time()
		
			while(True): 
				if(time.time()-self.timestampatstopPulse>0.2): 
					break
			
			GPIO.output(config.STOP_PIN,GPIO.LOW)
		
		else:
			GPIO.output(config.STOP_PIN,GPIO.HIGH)
			self.timestampatFirstStopPulse=time.time()
		
			while(True): 
				if(time.time()-self.timestampatFirstStopPulse>0.25): 
					break
		
			GPIO.output(config.STOP_PIN,GPIO.LOW)
			self.timestampafterFirstStopPulse=time.time()
		
			while(True): 
				if(time.time()-self.timestampafterFirstStopPulse>0.25): 
					break
		
			GPIO.output(config.STOP_PIN,GPIO.HIGH)
			self.timestampatSecondStopPulse=time.time()
		
			while(True): 
				if(time.time()-self.timestampatSecondStopPulse>0.25): 
					break
		
		GPIO.output(config.STOP_PIN,GPIO.LOW)

		print("OVEN_Stopped......")

		self.timestampatstopPulse=0
		self.timestampatFirstStopPulse=0
		self.timestampafterFirstStopPulse=0
		self.timestampatSecondStopPulse=0
		
		self.isPaused = 0
		self.isstopped = 1
		self.isStarted = 0
		
	def pause(self):

		GPIO.output(config.STOP_PIN,GPIO.HIGH)
		self.timestampatpausePulse=time.time()
		
		while(True): 
			if(time.time()-self.timestampatpausePulse>0.25): 
				break
		
		GPIO.output(config.STOP_PIN,GPIO.LOW)

		print("OVEN_Paused....")

		self.timestampatpausePulse=0
		self.isPaused = 1
		self.isstopped = 0
		self.isstarted = 0

	def isStarted():
		return self.isStarted 
	
	def isStopped():
		return self.isstopped 
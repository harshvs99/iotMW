import spi as spi
import configuration as config
import time

SPI=spi.SPI()

class TemperatureSensor():
	def configure():
		pass
	def getRawTemperature():
		pass
	def updateAdress():
		pass
	def stop():
		pass
		
class TSEV0108L39(TemperatureSensor):
	def __init__(self):
		self.isSPIconfigure = False
		self.temp={"sensor_temp":None,"pixel1":None,"pixel2":None,"pixel3":None,"pixel4":None,"pixel5":None,"pixel6":None,"pixel7":None,"pixel8":None}
		self.timestampforSpiStart = 0
		self.timestampafterMSbyteStart=0
		self.MSByte=0
		self.LSByte=0
	SPI=spi.SPI()
		
	def configure(self):
		if (self.SPI.isSpiclose()== True):
			self.SPI.configure(config.SPI_CHANNEL,config.SPI_CLOCK,config.SPI_MODE,config.SPI_isCsinactive,config.SPI_isThreewireactive)
			self.isSPIconfigure = True
		else:
			self.SPI.close()
	
	def getRawTemperature(self):
		if (self.SPI.isSpiConfigured == True):
			for i in range(len(self.temp)):
				if(i == 0):	
					self.temp["sensor_temp"]=self.updateAddress(0xA0)
				elif(i == 1):
					self.temp["pixel1"]=self.updateAddress(0xA1)
				elif(i == 2):
					self.temp["pixel2"]=self.updateAddress(0xA2)
				elif(i == 3):
					self.temp["pixel3"]=self.updateAddress(0xA3)
				elif(i == 4):
					self.temp["pixel4"]=self.updateAddress(0xA4)
				elif(i == 5):
					self.temp["pixel5"]=self.updateAddress(0xA5)
				elif(i == 6):
					self.temp["pixel6"]=self.updateAddress(0xA6)
				elif(i == 7):
					self.temp["pixel7"]=self.updateAddress(0xA7)
				elif(i == 8):
					self.temp["pixel8"]=self.updateAddress(0xA8)		
			return self.temp
							
		else:
			self.configure()
			self.temp={"senor_temp":00.00,"pixel1":00.00,"pixel2":00.00,"pixel3":00.00,"pixel4":00.00,"pixel5":00.00,"pixel6":00.00,"pixel7":00.00,"pixel8":00.00}
			return self.temp
			
	def updateAddress(self,Address):
		self.timestampforSpiStart=time.time()
		self.SPI.write_data(Address)
		while(True): 
			if(time.time()-self.timestampforSpiStart>0.0025): 
				break
		self.MSByte=self.SPI.transfer(0xff)
		self.timestampafterMSbyteStart=time.time()
		
		while True: 
			if (time.time()-self.timestampafterMSbyteStart>0.0025):
				 break		 
		self.LSByte=self.SPI.transfer(0xff)
		self.timestampforSpiStart=0
		self.timestampafterMSbyteStart=0

		if(self.MSByte[0] != 255):
			self.pixel_temp=((256*self.MSByte[0]+self.LSByte[0])/10)
		else:
			self.pixel_temp=((-256+self.LSByte[0])/10)
		
		return self.pixel_temp
	
	def stop(self):
		self.SPI.close()
		self.isSPIconfigure = False

import spidev

spi=spidev.SpiDev()

class SPI():
	def __init__(self):
		self.isSpiConfigured = False
		self.channel = 0
		self.max_speed_hz=0
		self.mode=0
		self.no_cs=False
		self.isThreewireactive=False
		self.isSpiClose =False
	spi=spidev.SpiDev()	
		
	def configure(self,channel,clock,mode,isCsinactive,isThreewireactive):
		self.spi.open(channel,0)
		self.spi.max_speed_hz=clock
		self.spi.mode=mode
		self.spi.no_cs=isCsinactive
		self.spi.threewire=isThreewireactive
		self.isSpiConfigured=True
	
	def write_data(self,addressRegister):
		self.spi.writebytes([addressRegister])
	
	def transfer(self,misoByte):	
		return self.spi.xfer2([misoByte],100000,200,8)
	
	def read_data(self,no_bytes):
		return self.readbytes(no_bytes)
	
	def isSpiConfigured(self):
		return self.isSpiConfigured
		
	def close(self):
		self.spi.close()
		self.isSpiClose=True
		self.isSpiConfigured = False
	
	def isSpiclose(self):
		return self.isSpiClose
	

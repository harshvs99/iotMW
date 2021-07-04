import temperature as temp
import time
import json 
import redis

cache=redis.Redis()

def temp_configure():
	global temperatureSensor,Temperature
	temperatureSensor = temp.TSEV0108L39()
	temperatureSensor.stop()
	temperatureSensor.configure()
	Temperature={"Temp":None,"code":None}
	return "Ok"

def Temp():
	global temperatureSensor,Temperature
	try:
		#while True:
		#t1=time.time()
		temp_list=[]
		for i in range(0,10) :
			data=temperatureSensor.getRawTemperature()
		#	print(data)
			all_temp_list=list(data.values())
			del all_temp_list[0]

			if (all(i==0.0 for i in data.values())):
				#Temp sensor is completly disconneted
				Temperature["code"]=404
				return Temperature

			elif(all ( i== -0.1  for i in data.values())):
				#VCC/GND is Disconnected 
				Temperature['code']=403
				return Temperature
		
			elif (data["sensor_temp"] > 85.0 or data["sensor_temp"] < 0.0 ):
				Temperature["Temp"]=data["senor_temp"]
				Temperature["code"]=402
				return Temperature
		
			elif (all ( (i > 120.0 or i < -20.0 ) for i in all_temp_list) ):
			
				temp_max=max(all_temp_list)
				temp_min=min(all_temp_list)
				if (temp_max>120.0):
					Temperature["Temp"]=temp_max
				elif(temp_min< -20.0):
					Temperature["Temp"]=temp_min
				Temperature["code"]=401
				return Temperature
		
			else:
				#print(all_temp_list)
				input=json.loads(cache.get("InputStatusAndReading"))
				reachTemp=float(input["ReachTemp"])
				if  (reachTemp>1.0 and reachTemp<10.0):
					temp_list.append(min(all_temp_list))
				else:
					temp_list.append(max(all_temp_list))
		
		temp_list.sort()
		final_temp=(temp_list[4]+temp_list[5])/2.0
                #print(input['magnetron'])
		if float(input["Magnetron"]):
			Temperature["Temp"]=round(final_temp,0)-7
		else:
			Temperature["Temp"]=round(final_temp,0)
		Temperature["code"]=200
		return Temperature

	except Exception as e:
		print(str(e))                
		Temperature["code"]=405
		temperatureSensor.stop()
		return Temperature

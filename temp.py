import temperature as temp
import time
import json
import redis
import pandas as pd
cache=redis.Redis()
global l
l=[]
global mag_on
mag_on = False
global mag_on_time
mag_on_time = None
global temp_before_mag_on
temp_before_mag_on = 25.6
global curr_temp
curr_temp = 0.0
global temp_before_mag_on_used
temp_before_mag_on_used = False
global reach_temp
reach_temp = None
global temp_readings
temp_readings = pd.DataFrame(columns=[1,2,3,4,5,6,7,8,'_min','_2_sec_min_of_min','two_sec_max','curr_temp','mag'])
#global all_temp_list
#all_temp_list=[]

def temp_configure():
        global temperatureSensor,Temperature
        temperatureSensor = temp.TSEV0108L39()
        temperatureSensor.stop()
        temperatureSensor.configure()
        Temperature={"Temp":None,"code":None}
        return "Ok"

def Temp():
    global mag_on,Temperature,mag_on_time,temp_before_mag_on,curr_temp,temp_before_mag_on_used,reach_temp,temp_readings
    try:
        data=temperatureSensor.getRawTemperature()
        all_temp_list=list(data.values())
        del all_temp_list[0]

        if (all(i==0.0 for i in data.values())):
            temp_readings.drop(range(len(temp_readings)),inplace=True)
            temp_readings.reset_index(drop=True,inplace=True)
            #Temp sensor is completly disconneted
            Temperature["code"]=404
            return Temperature

        elif(all ( i== -0.1  for i in data.values())):
            temp_readings.drop(range(len(temp_readings)),inplace=True)
            temp_readings.reset_index(drop=True,inplace=True)
            #VCC/GND is Disconnected 
            Temperature['code']=403
            return Temperature

        elif (data["sensor_temp"] > 85.0 or data["sensor_temp"] < 0.0 ):
            temp_readings.drop(range(len(temp_readings)),inplace=True)
            temp_readings.reset_index(drop=True,inplace=True)
            Temperature["Temp"]=data["senor_temp"]
            Temperature["code"]=402
            return Temperature

        elif (all ( (i > 120.0 or i < -20.0 ) for i in all_temp_list) ):
            temp_readings.drop(range(len(temp_readings)),inplace=True)
            temp_readings.reset_index(drop=True,inplace=True)
            temp_max=max(all_temp_list)
            temp_min=min(all_temp_list)
            if (temp_max>120.0):
                Temperature["Temp"]=temp_max
            elif(temp_min< -20.0):
                Temperature["Temp"]=temp_min
            Temperature["code"]=401
            return Temperature
        t1=time.time()*1000
        if mag_on == False:
            if cache.get("Magnetron").decode()=='1':
                print("mag started")
                mag_on = True
                mag_on_time = time.time()
                reach_temp = float(cache.get("ReachTemp").decode())
        elif mag_on == True:
            if cache.get("Magnetron").decode()=='0':
                print("mag stopped")
                mag_on = False
                mag_on_time = None
                reach_temp = None
        current_time = time.time()
        if len(temp_readings)>2000:
            temp_readings.drop(range(len(temp_readings)-150),inplace=True)
            temp_readings.reset_index(drop=True,inplace=True)
        temp = all_temp_list
        _min = min(temp[3:6])
        _2_sec_min_of_min=_min
        two_sec_max=_min
        if len(temp_readings)>0:
            _2_sec_min_of_min=min(temp_readings.tail(35)['_min'])
            two_sec_max=max(temp_readings.tail(35)['_2_sec_min_of_min'])
        temp.append(_min)
        temp.append(_2_sec_min_of_min)
        temp.append(two_sec_max)
        if mag_on:
            curr_temp = two_sec_max
        else:
            curr_temp = two_sec_max
        temp.append(curr_temp)
        temp.append(mag_on)
        #print("current recorded temp = "+str(curr_temp))
        if not mag_on:
            temp_before_mag_on = curr_temp
        temp_readings.loc[len(temp_readings)] = temp
        ############ Checking if temperature is not increasing and put in error state
        if mag_on:
            time_diff = current_time-mag_on_time
            ############ case for 5 second increments
            #if time_diff>4.5 and len(temp_readings)>75 and int(current_time-mag_on_time)%5==0:
            #    _0th_read = temp_readings.iloc[len(temp_readings)-75]["curr_temp"]
            #    _curr_read = temp_readings.iloc[len(temp_readings)-1]["curr_temp"]
            #    if mag_on and (_curr_read - _0th_read)<0.25:
            #        Temperature["code"]=4005
            #        return Temperature
            ############ case for 10 second increments
            #if time_diff>9.5 and len(temp_readings)>150 and int(current_time-mag_on_time)%10==0:
            #    _0th_read = temp_readings.iloc[len(temp_readings)-150]["curr_temp"]
            #    _curr_read = temp_readings.iloc[len(temp_readings)-1]["curr_temp"]
            #    if mag_on and (_curr_read - _0th_read)<0.5:
            #        Temperature["code"]=4010
            #        return Temperature
        ############ END
        ############ Logic for reach temp handling
        Temperature["code"]=200
        if mag_on:
            if reach_temp < 10 and reach_temp-curr_temp < 0.25:
                time.sleep(5)
                Temperature["Temp"]=reach_temp
            elif reach_temp < 20 and  reach_temp-curr_temp < 2:
                time.sleep(5)
                Temperature["Temp"]=reach_temp
            elif reach_temp < 30 and  reach_temp-curr_temp < 2:
                time.sleep(5)
                Temperature["Temp"]=reach_temp
            elif reach_temp < 40 and  reach_temp-curr_temp < 2.5:
                time.sleep(4)
                Temperature["Temp"]=reach_temp
            elif reach_temp < 60 and  reach_temp-curr_temp < 3:
                time.sleep(4)
                Temperature["Temp"]=reach_temp
            elif reach_temp < 80 and  reach_temp-curr_temp < 4:
                time.sleep(5)
                Temperature["Temp"]=reach_temp
            elif reach_temp < 120 and  reach_temp-curr_temp < 4:
                time.sleep(5)
                Temperature["Temp"]=reach_temp
            else:
                Temperature["Temp"]=curr_temp
        else:
            Temperature["Temp"]=curr_temp
        ############ END
        t2=time.time()*1000
        Temperature["4"]=temp[3]
        Temperature["5"]=temp[4]
        Temperature["6"]=temp[5]
        #print(len(temp_readings))
        return Temperature

    
    except Exception as e:
        print(str(e))                
        Temperature["code"]=405
        temperatureSensor.stop()
        return Temperature


def tocsv(filename):
    temp_readings.to_csv(filename)

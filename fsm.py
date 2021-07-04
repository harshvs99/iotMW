import redis
import time
from input import *
from states import *
import requests
from multiprocessing import Process

if __name__ == "__main__":
    p=Process(target=hw_input)
    p.start()
    r = SMART_MW_Oven()
    r.FSM.ToTransition("toSelf_Check")
    r.Execute()
    GetRefreshToken()
    while not cache.exists("Token"):
        if r.FSM.curState.__class__.__name__!= "InternetError":
            r.FSM.ToTransition("toInternetError")
            r.Execute()
        server_time=time.time()
        while time.time()-server_time<1:
            pass
        GetRefreshToken()
    pt=time.time()
    while True:
        events=json.loads(cache.get("InputStatusAndReading"))
        #print(events)
        if events["Internet"]==1 and events["Door"]==0 and events["TempSensor"]==200:
            if events["Magnetron"]==0 and cache.get("CurrentState").decode()!="HeatingPaused":
                NextState="Idle"
                if events["Action"]=="Start":
                    if float(events["LiveTemp"])<float(events["ReachTemp"]):
                        NextState="HeatingOn"
                    else:   pass             
            else:
                if float(events["LiveTemp"])>=float(events["ReachTemp"]):
                    print(events)
                    if float(events["ReachTemp"])<=20.0:
                        NextState="HeatingPaused"
                        cache.set("Action","Stop")  #Q. what's the action cache word for pause
                        pass
                        if cache.get("CurrentState") == "HeatingPaused"
                            pt1 = time.time()
                            temp_record = []
                            while time.time()-pt1 <= 3.0:
                                temp_record.append(float(events["LiveTemp"]))
                            LowRecordedTemp = min(temp_record)
                            if LowRecordedTemp >= float(events["ReachTemp"]):
                                NextState="HeatingCompleted"
                                cache.set("Action","Stop")  #Q. what's the action cache word for pause
                            else:
                                NextState="HeatingOn"
                    else: 
                        NextState="HeatingCompleted"
                        cache.set("Action","Stop")
                elif events["Action"]=="Stop":
                    NextState="HeatingPaused"
                else:
                    NextState="HeatingOn"
        else:
            if events["Internet"]==0:
                NextState="InternetError"
            elif events["Door"]==1:
                NextState="DoorOpen"
            else:
                NextState="SensorError" 
       # print(NextState)
        if r.FSM.curState.__class__.__name__!=NextState:
            if cache.get("CurrentState").decode()!="ManualOverride" or NextState=="DoorOpen":
               # print(NextState)
                #print(r.FSM.curState.__class__.__name__)
                r.FSM.ToTransition("to"+NextState)
                r.Execute()
        
        else:   pass
        
        if time.time()-pt>1.0 or NextState!=r.FSM.curState.__class__.__name__:
            pt=time.time()
            SendData()

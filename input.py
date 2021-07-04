from temp import *
from mag_door import *
import redis
import json
import requests

cache=redis.Redis()
cache.flushdb()

temp_configure()
mag_door_configure()

UrlGetToken="http://13.233.240.121/server.microwave/GetToken"
url="http://13.233.240.121/server.microwave/SetTemp"
url_setLiveStatus="http://13.233.240.121/server.microwave/SetLiveStatus"
header={"Content-Type":"application/json"}

# magnetron on=1
# door close=0
# temp connected=200
#OVenStatus started=1
#internet connected=1
InputStatusAndReading={"Door":0,"Internet":1,"TempSensor":200,"Magnetron":0,"Action":"Stop","LiveTemp":0,"ReachTemp":0}
cache.set("InputStatusAndReading",json.dumps(InputStatusAndReading))
cache.set("Action","Stop")
cache.set("ReachTemp",0)
cache.set("Magnetron",0)
cache.set("Internet",1)

def hw_input():
    while True:
        try:
            magnetron=magnetron_input()
            door=door_input()
            TempValueAndStatus=Temp()
            Action=cache.get("Action").decode()
            ReachTemp=cache.get("ReachTemp").decode()
            cache.set("Magnetron",magnetron)
            cache.set("Door",door)
            Internet=int(cache.get("Internet").decode())
            InputStatusAndReading={"Door":door,"Internet":Internet,"TempSensor":TempValueAndStatus["code"],"Magnetron":magnetron,"Action":Action,"LiveTemp":TempValueAndStatus["Temp"],"ReachTemp":ReachTemp}
            cache.set("InputStatusAndReading",json.dumps(InputStatusAndReading))
        except Exception as e:
            print(str(e))

def SendData():
    InputStatusAndReading=json.loads(cache.get("InputStatusAndReading"))
    OvenStarted=0
    if InputStatusAndReading['Magnetron']==1:
        OvenStarted=1
    data={'Token':cache.get('Token').decode(),'LiveTemp':InputStatusAndReading['LiveTemp'],\
    'CurrentState':cache.get("CurrentState").decode(),'PrevState':cache.get("PrevState").decode(),'OvenStatus':OvenStarted,\
    'TempSensor':InputStatusAndReading['TempSensor']}
    try:
        print(data)
        r=requests.post(url=url_setLiveStatus,data=json.dumps(data),headers=header,timeout=(3.05,5))
        if r.status_code==200:
            print(r.json())
            cache.set("Action",r.json()['Action'])
            cache.set("ReachTemp",r.json()['ReachTemp'])
            cache.set("Internet",1)
        else:
            print("Server down")
            cache.set("Internet",0)
    except requests.ConnectionError:
        cache.set("Internet",0)
    except Exception as e:
        print(str(e))

def GetRefreshToken():
    f=open(r"../RefreshToken","r")
    f1=open("Version","r")
    Version=f1.read().rstrip()
    RefreshToken=f.read().rstrip()
    f.close()
    f1.close()
    hwaddr=open(r"../hwaddr",'r')
    mac=hwaddr.read().rstrip()
    hwaddr.close()
    data={"MachineId":mac,"AuthToken":RefreshToken,"SoftwareVersion":Version}
    try:
        print(data)
        r=requests.post(url=UrlGetToken,data=json.dumps(data),headers=header,timeout=(3.05,3))
        print(r.json())
        token=r.json()['Token']
        print (token)
        with open("../RefreshToken",'w') as RefreshTokenFile:
            RefreshTokenFile.write(str(token))
            RefreshTokenFile.close()
        cache.set('Token',token)
    except Exception as e:
        print(str(e))
        

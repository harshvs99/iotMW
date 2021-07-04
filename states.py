# SMART MICROWAVE PYTHON CODE __VERSION__2.0.0 Date-07/07/2020 Owner -  Udyogyantra Tecchnologies
# #======================================================================================================================================

import time
import redis
import json
import oven
import led
from threading import Thread

x = led.led()
x.configure()

MW = oven.Butler()
MW.configure()
cache = redis.Redis()

cache.set("PrevState", "Self_Check")
cache.set("CurrentState", "Self_Check")


#  STATES=1['Self_Check','Emergency','Idle','HeatingOn','#TempAlreadyHigh','HeatingCompleted','HeatingPaused',
# 'InternetError','DoorOpen','SensorError']

class State(object):  # The base template state which all others will inherit from
    def __init__(self, FSM):
        self.FSM = FSM
        self.stopTime = 0
        self.startTime = 0

    def Enter(self):
        self.startTime = time.time()

    def Execute(self):
        r = SMART_MW_Oven()

        for counter in range(2):
            pt = time.time()
            if cache.get('Magnetron').decode() == '0':
                break
            else:
                MW.stop()

            while time.time() - pt <= 3.0:
                if cache.get('Door').decode() == '1':
                    r.FSM.ToTransition("toDoorOpen")
                    r.Execute()
                    break

        if counter == 1 and cache.get('Magnetron').decode() == '1':
            r.FSM.ToTransition("toManualOverride")
            r.Execute()

    def Exit(self):
        pass


class Self_Check(State):
    def __init__(self, FSM):
        super().__init__(FSM)

    def Enter(self):
        super().Enter()
        cache.set("CurrentState", "Self_Check")

    def Execute(self):
        super().Execute()
        x.self_check()
        events = json.loads(cache.get("InputStatusAndReading"))
        r = SMART_MW_Oven()

        if events["Internet"] == 1 and events["TempSensor"] == 200:
            r.FSM.ToTransition("toIdle")
        elif events["Internet"] == 0:
            r.FSM.ToTransition("toInternetError")
        else:
            r.FSM.ToTransition("toSensorError")
        r.Execute()

    def Exit(self):
        cache.set("PrevState", "Self_Check")


class ManualOverride(State):
    def __init__(self, FSM):
        super().__init__(FSM)

    def Enter(self):
        super().Enter()
        cache.set("CurrentState", "ManualOverride")

    def Execute(self):
        global t
        cache.set("LedOn", '1')
        t = Thread(target=x.manual_override)
        t.start()

    def Exit(self):
        cache.set("PrevState", "ManualOverride")
        global t
        if t.isAlive():
            cache.set("LedOn", '0')
            t.join()


class Idle(State):
    def __init__(self, FSM):
        super().__init__(FSM)

    def Enter(self):
        super().Enter()
        cache.set("CurrentState", "Idle")

    def Execute(self):
        super().Execute()
        x.idle()

    def Exit(self):
        cache.set("PrevState", "Idle")


class HeatingOn(State):
    def __init__(self, FSM):
        super(HeatingOn, self).__init__(FSM)

    def Enter(self):
        super(HeatingOn, self).Enter()
        cache.set("CurrentState", "HeatingOn")

    def Execute(self):
        r = SMART_MW_Oven()
        x.heating_on()
        for counter in range(2):
            pt = time.time()
            if cache.get('Magnetron').decode() == '1':
                break
            else:
                MW.start()

            while time.time() - pt <= 3.0:
                if cache.get('Door').decode() == '1':
                    r.FSM.ToTransition("toDoorOpen")
                    r.Execute()
                    break

        if counter == 1 and cache.get('Magnetron').decode() == '0':
            r.FSM.ToTransition("toManualOverride")
            r.Execute()

    def Exit(self):
        cache.set("PrevState", "HeatingOn")


class HeatingCompleted(State):
    def __init__(self, FSM):
        super(HeatingCompleted, self).__init__(FSM)

    def Enter(self):
        super(HeatingCompleted, self).Enter()
        x.heating_completed()
        cache.set("CurrentState", "HeatingCompleted")
        cache.set("Action", "Stop")
        MW.stop()

    def Execute(self):
        super().Execute()

    def Exit(self):
        cache.set("PrevState", "HeatingCompleted")


class HeatingPaused(State):
    def __init__(self, FSM):
        super(HeatingPaused, self).__init__(FSM)

    def Enter(self):
        super(HeatingPaused, self).Enter()
        cache.set("CurrentState", "HeatingPaused")

    def Execute(self):
        r = SMART_MW_Oven()
        x.heating_paused()
        for counter in range(2):
            pt = time.time()
            if cache.get('Magnetron').decode() == '0':
                break
            else:
                MW.pause()

            while time.time() - pt <= 3.0:
                if cache.get('Door').decode() == '1':
                    r.FSM.ToTransition("toDoorOpen")
                    r.Execute()
                    break
        if (counter == 1 and cache.get('Magnetron').decode() == '1'):
            r.FSM.ToTransition("toManualOverride")
            r.Execute()

    def Exit(self):
        cache.set("PrevState", "HeatingPaused")


class InternetError(State):
    def __init__(self, FSM):
        super(InternetError, self).__init__(FSM)

    def Enter(self):
        super(InternetError, self).Enter()
        cache.set("CurrentState", "InternetError")
        if cache.get("Magnetron").decode() == 1:
            MW.stop()

    def Execute(self):
        super().Execute()
        global t
        cache.set("LedOn", '1')
        t = Thread(target=x.internet_error)
        # print("THREAD  ENTER")
        t.start()
        # print(t.isAlive())

    def Exit(self):
        cache.set("PrevState", "InternetError")
        global t
        if t.isAlive():
            cache.set("LedOn", '0')
            t.join()


class DoorOpen(State):
    def __init__(self, FSM):
        super(DoorOpen, self).__init__(FSM)

    def Enter(self):
        super(DoorOpen, self).Enter()
        cache.set("CurrentState", "DoorOpen")
        if (cache.get("PrevState").decode() == "HeatingOn" or cache.get("PrevState").decode() == "HeatingPaused"):
            MW.pause()

    def Execute(self):
        super().Execute()
        x.door_open()

    def Exit(self):
        cache.set("PrevState", "DoorOpen")


class SensorError(State):
    def __init__(self, FSM):
        super(SensorError, self).__init__(FSM)

    def Enter(self):
        super(SensorError, self).Enter()
        cache.set("CurrentState", "SensorError")
        if cache.get("Magnetron").decode() == 1:
            MW.stop()

    def Execute(self):
        super().Execute()
        global t
        cache.set("LedOn", '1')
        t = Thread(target=x.sensor_error)
        t.start()

    def Exit(self):
        cache.set("PrevState", "SensorError")
        global t
        if t.isAlive():
            cache.set("LedOn", '0')
            t.join()


class Transition(object):  # Class called when any transition occurs from one state to another
    def __init__(self, toState):
        self.toState = toState

    def Execute(self):  pass


# ==================================================================================================================
# FINITE STATE MACHINES

class FSM(object):  # Holds the states and transitions available executes current states main functions and transitions
    def __init__(self, character):
        self.char = character
        self.states = {}
        self.transitions = {}
        self.curState = None
        self.prevState = None  # USE TO PREVENT LOOPING 2 STATES FOREVER
        self.trans = None

    def AddTransition(self, transName, transition):
        self.transitions[transName] = transition

    def AddState(self, stateName, state):
        self.states[stateName] = state

    def SetState(self, stateName):
        self.prevState = self.curState
        self.curState = self.states[stateName]

    def ToTransition(self, toTrans):
        self.trans = self.transitions[toTrans]
        print(toTrans)

    def Execute(self):
        if self.trans:
            self.curState.Exit()
            self.trans.Execute()
            self.SetState(self.trans.toState)
            self.curState.Enter()
            self.trans = None
        self.curState.Execute()
        # print(Transition("Self_Check"))#self.curState.Enter()


##=================================================================================================================================================
## IMPLEMENTATION

Char = type("Char", (object,), {})


class SMART_MW_Oven(Char):  # #Base character which will be holding the Finite State Machine, which will hold the
    # states and
    # transitions. '''
    def __init__(self):
        self.FSM = FSM(self)

        ## STATES
        self.FSM.AddState("Idle", Idle(self.FSM))
        self.FSM.AddState("HeatingOn", HeatingOn(self.FSM))
        self.FSM.AddState("Self_Check", Self_Check(self.FSM))
        self.FSM.AddState("HeatingCompleted", HeatingCompleted(self.FSM))
        self.FSM.AddState("HeatingPaused", HeatingPaused(self.FSM))
        self.FSM.AddState("InternetError", InternetError(self.FSM))
        self.FSM.AddState("DoorOpen", DoorOpen(self.FSM))
        self.FSM.AddState("SensorError", SensorError(self.FSM))
        self.FSM.AddState("ManualOverride", ManualOverride(self.FSM))

        ## TRANSITIONS
        self.FSM.AddTransition("toIdle", Transition("Idle"))
        self.FSM.AddTransition("toHeatingOn", Transition("HeatingOn"))
        self.FSM.AddTransition("toSelf_Check", Transition("Self_Check"))
        self.FSM.AddTransition("toHeatingCompleted", Transition("HeatingCompleted"))
        self.FSM.AddTransition("toHeatingPaused", Transition("HeatingPaused"))
        self.FSM.AddTransition("toInternetError", Transition("InternetError"))
        self.FSM.AddTransition("toDoorOpen", Transition("DoorOpen"))
        self.FSM.AddTransition("toSensorError", Transition("SensorError"))
        self.FSM.AddTransition("toManualOverride", Transition("ManualOverride"))
        self.FSM.SetState("Idle")

    def Execute(self):
        self.FSM.Execute()

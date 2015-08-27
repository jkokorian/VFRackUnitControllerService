from tinyrpc.dispatch import public

class VFRackUnitController(object):

    valveNames = ["pureArgon", 
                  "bubblerInlet", 
                  "bubblerOutlet", 
                  "chamberInlet",
                  "chamberOutlet",
                  "exhaust",
                  "purgeInlet"]

    stateNames = {0: "stopped",
                  1: "flowing",
                  2: "pumping",
                  3: "purging",
                  4: "venting"}

    def __init__(self, serial):
        """
        Creates a new instance of the VFRackUnitController
        class.
        
        parameters
        ----------
        
        serial: an instance of serial.Serial to communicate with the sensor over RS-232.
        """
        
        self.serial = serial
        
    def _query(self,command,replyConverter=str):
        commandString = "%s\n".encode() % (command)
        print commandString
        self.serial.write(commandString)
        self.serial.flush()
        
        reply = self.serial.readall()
        
        if reply.startswith("E:"):
            #an error has occured
            raise Exception("The device threw an error: %s" % reply)
        if replyConverter is not None:
            value = replyConverter(reply.strip())
            return value
    
    def _valueQuery(self,command,valueConverter=str):
        reply = self._query(command)
        return valueConverter(reply[len(command):])
    
    @public
    def getValveStates(self):
        command = "VALVES?"
        valveStates = self._query(command,lambda reply: [bool(int(v)) for v in list(reply[7:])])
        valveStatesDict = {valveName: valveState for valveName,valveState in zip(self.valveNames, valveStates)}
        return valveStatesDict
        
    @public
    def getState(self):
        command = "STATE?"
        stateInt = self._valueQuery(command, int)        
        state = self.stateNames[stateInt]
        return state
        
    @public
    def getActualPureArgonFlow(self):
        value = self._valueQuery("PAFLOW?",float)
        return value

    @public
    def getActualBubblerFlow(self):
        value = self._valueQuery("BBFLOW?", float)
        return value

    @public    
    def getVacuumPumpIsActive(self):
        value = self._valueQuery("PUMP?", lambda v: bool(int(v)))
        return value

    @public    
    def getFirmwareVersion(self):
        value = self._valueQuery("VERSION?", str)
        return value

    @public        
    def getPureArgonFlowStateSetpoint(self):
        value = self._valueQuery("PAFLOWSP?", float)
        return value

    @public        
    def getPureArgonVentStateSetpoint(self):
        value = self._valueQuery("PAVENTSP?", float)
        return value

    @public        
    def getPureArgonPurgeStateSetpoint(self):
        value = self._valueQuery("PAPURGESP?", float)
        return value

    @public        
    def getPureArgonWorkingSetpoint(self):
        value = self._valueQuery("PAWSP?", float)
        return value

    @public        
    def getBubblerWorkingSetpoint(self):
        value = self._valueQuery("BBWSP?", float)
        return value
        
        
 
    @public       
    def gotoStopState(self):
        self._query("STOP!")

    @public        
    def gotoFlowState(self):
        self._query("FLOW!")

    @public            
    def gotoPumpState(self):
        self._query("PUMP!")

    @public                
    def gotoPurgeState(self):
        self._query("PURGE!")

    @public            
    def gotoVentState(self):
        self._query("VENT!")

    @public            
    def test(self):
        return "hello!"
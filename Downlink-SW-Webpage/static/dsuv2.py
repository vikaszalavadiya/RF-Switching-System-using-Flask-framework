#Ku-Band RF Downlink Switching Unit - CSW23Ku
#Version: V 1.2.0
#Last Update: 18-01-22

from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import encoder, decoder
from pysnmp.proto import api
import time, bisect
import RPi.GPIO as GPIO
import time
import threading
from pysnmp.hlapi.asyncore import *
import fileinput
import os
from flask import Flask
from flask import jsonify, request
from flask import render_template
from flask import send_file
from flask import render_template, request, url_for, redirect, escape
import logging
import subprocess



class SysDescr:
    name = (1,3,6,1,2,1,1,1,0)
    def __eq__(self, other): return self.name == other
    def __ne__(self, other): return self.name != other
    def __lt__(self, other): return self.name < other
    def __le__(self, other): return self.name <= other
    def __gt__(self, other): return self.name > other
    def __ge__(self, other): return self.name >= other
    def __call__(self, protoVer):
        return api.protoModules[protoVer].OctetString('Ku-Band RF Downlink Switching Unit - CSW23Ku')

class SysObjectID:
    name = (1,3,6,1,2,1,1,2,0)
    def __eq__(self, other): return self.name == other
    def __ne__(self, other): return self.name != other
    def __lt__(self, other): return self.name < other
    def __le__(self, other): return self.name <= other
    def __gt__(self, other): return self.name > other
    def __ge__(self, other): return self.name >= other
    def __call__(self, protoVer):
        return api.protoModules[protoVer].OctetString('Praniskom Solutions Pvt Ltd - Downlink SW CSW23Ku')

class Uptime:
    name = (1,3,6,1,2,1,1,3,0)
    birthday = time.time()
    def __eq__(self, other): return self.name == other
    def __ne__(self, other): return self.name != other
    def __lt__(self, other): return self.name < other
    def __le__(self, other): return self.name <= other
    def __gt__(self, other): return self.name > other
    def __ge__(self, other): return self.name >= other    
    def __call__(self, protoVer):
        return api.protoModules[protoVer].TimeTicks((time.time()-self.birthday)*100)

class sysContact:
    name = (1,3,6,1,2,1,1,4,0)
    birthday = time.time()
    def __eq__(self, other): return self.name == other
    def __ne__(self, other): return self.name != other
    def __lt__(self, other): return self.name < other
    def __le__(self, other): return self.name <= other
    def __gt__(self, other): return self.name > other
    def __ge__(self, other): return self.name >= other    
    def __call__(self, protoVer):
        return api.protoModules[protoVer].OctetString(
            'Contact: +91-265-2985335  '
            'Email: sales@praniskom.com  '
            'Website: www.praniskom.com '
            'Postal Address: B-315, Monalisa Business Center, '
            'Near More Mega Store, Manjalpur, '
            'Vadodara, Gujarat. - 390011'  
            )

class SysName:
    name = (1,3,6,1,2,1,1,5,0)
    def __eq__(self, other): return self.name == other
    def __ne__(self, other): return self.name != other
    def __lt__(self, other): return self.name < other
    def __le__(self, other): return self.name <= other
    def __gt__(self, other): return self.name > other
    def __ge__(self, other): return self.name >= other
    def __call__(self, protoVer):
        return api.protoModules[protoVer].OctetString('Ku-Band RF Downlink Switching Unit')

class SysLocation:
    name = (1,3,6,1,2,1,1,6,0)
    def __eq__(self, other): return self.name == other
    def __ne__(self, other): return self.name != other
    def __lt__(self, other): return self.name < other
    def __le__(self, other): return self.name <= other
    def __gt__(self, other): return self.name > other
    def __ge__(self, other): return self.name >= other
    def __call__(self, protoVer):
        return api.protoModules[protoVer].OctetString('Under development')

class sysServices:
    name = (1,3,6,1,2,1,1,7,0)
    def __eq__(self, other): return self.name == other
    def __ne__(self, other): return self.name != other
    def __lt__(self, other): return self.name < other
    def __le__(self, other): return self.name <= other
    def __gt__(self, other): return self.name > other
    def __ge__(self, other): return self.name >= other
    def __call__(self, protoVer):
        return api.protoModules[protoVer].OctetString('0')

class localremote:
    
    name = (1,3,6,1,4,1,49289,902,1,0)
    def __eq__(self, other): return self.name == other
    def __ne__(self, other): return self.name != other
    def __lt__(self, other): return self.name < other
    def __le__(self, other): return self.name <= other
    def __gt__(self, other): return self.name > other
    def __ge__(self, other): return self.name >= other
    def __call__(self, protoVer):
        global loc_rem_var
        if(loc_rem_var==False):
            lclremsnmp=1
        else:
            lclremsnmp=0
        return api.protoModules[protoVer].Integer(lclremsnmp)

class converter1:
    name = (1,3,6,1,4,1,49289,902,2,0)
    def __eq__(self, other): return self.name == other
    def __ne__(self, other): return self.name != other
    def __lt__(self, other): return self.name < other
    def __le__(self, other): return self.name <= other
    def __gt__(self, other): return self.name > other
    def __ge__(self, other): return self.name >= other
    def __call__(self, protoVer):
        global sw1pos1
        return api.protoModules[protoVer].Integer(sw1pos1)

class converter2:
    name = (1,3,6,1,4,1,49289,902,3,0)
    def __eq__(self, other): return self.name == other
    def __ne__(self, other): return self.name != other
    def __lt__(self, other): return self.name < other
    def __le__(self, other): return self.name <= other
    def __gt__(self, other): return self.name > other
    def __ge__(self, other): return self.name >= other
    def __call__(self, protoVer):
        global sw2pos1
        return api.protoModules[protoVer].Integer(sw2pos1)

class servo_tracking:
    name = (1,3,6,1,4,1,49289,902,4,0)
    def __eq__(self, other): return self.name == other
    def __ne__(self, other): return self.name != other
    def __lt__(self, other): return self.name < other
    def __le__(self, other): return self.name <= other
    def __gt__(self, other): return self.name > other
    def __ge__(self, other): return self.name >= other
    def __call__(self, protoVer):
        global sw3pos1
        return api.protoModules[protoVer].Integer(sw3pos1)

class lineamplifire:
    name = (1,3,6,1,4,1,49289,901,5,0)
    def __eq__(self, other): return self.name == other
    def __ne__(self, other): return self.name != other
    def __lt__(self, other): return self.name < other
    def __le__(self, other): return self.name <= other
    def __gt__(self, other): return self.name > other
    def __ge__(self, other): return self.name >= other
    def __call__(self, protoVer):
        global sw4pos1
        return api.protoModules[protoVer].Integer(sw4pos1)

class aupc:
    name = (1,3,6,1,4,1,49289,901,6,0)
    def __eq__(self, other): return self.name == other
    def __ne__(self, other): return self.name != other
    def __lt__(self, other): return self.name < other
    def __le__(self, other): return self.name <= other
    def __gt__(self, other): return self.name > other
    def __ge__(self, other): return self.name >= other
    def __call__(self, protoVer):
        global sw5pos1
        return api.protoModules[protoVer].Integer(sw5pos1)


mibInstr = ( SysDescr(), SysObjectID(), Uptime() ,sysContact(),SysName(),
    SysLocation(), sysServices(),localremote(), converter1(), converter2(),servo_tracking())

mibInstrIdx = {}
for mibVar in mibInstr:
    mibInstrIdx[mibVar.name] = mibVar



def cbFun(transportDispatcher, transportDomain, transportAddress, wholeMsg):
    global sw1pos1,sw2pos1,sw3pos1,sw1pos2,sw2pos2,sw3pos2,loc_rem_var
    
    while wholeMsg:
        msgVer = api.decodeMessageVersion(wholeMsg)
        if msgVer in api.protoModules:
            pMod = api.protoModules[msgVer]
        else:
            print('Unsupported SNMP version %s' % msgVer)
            return
        reqMsg, wholeMsg = decoder.decode(
            wholeMsg, asn1Spec=pMod.Message(),
            )
        rspMsg = pMod.apiMessage.getResponse(reqMsg)
        rspPDU = pMod.apiMessage.getPDU(rspMsg)        
        reqPDU = pMod.apiMessage.getPDU(reqMsg)
        varBinds = []; pendingErrors = []
        errorIndex = 0
        # GETNEXT PDU
        if reqPDU.isSameTypeWith(pMod.GetNextRequestPDU()):
            # Produce response var-binds
            for oid, val in pMod.apiPDU.getVarBinds(reqPDU):
                errorIndex = errorIndex + 1
                # Search next OID to report
                nextIdx = bisect.bisect(mibInstr, oid)
                if nextIdx == len(mibInstr):
                    # Out of MIB
                    varBinds.append((oid, val))
                    pendingErrors.append(
                        (pMod.apiPDU.setEndOfMibError, errorIndex)
                        )
                else:
                    # Report value if OID is found
                    varBinds.append(
                        (mibInstr[nextIdx].name, mibInstr[nextIdx](msgVer))
                        )
        elif reqPDU.isSameTypeWith(pMod.GetRequestPDU()):
            for oid, val in pMod.apiPDU.getVarBinds(reqPDU):
                if oid in mibInstrIdx:
                    varBinds.append((oid, mibInstrIdx[oid](msgVer)))
                else:
                    # No such instance
                    varBinds.append((oid, val))
                    pendingErrors.append(
                        (pMod.apiPDU.setNoSuchInstanceError, errorIndex)
                        )
                    break
        elif reqPDU.isSameTypeWith(pMod.SetRequestPDU):
            for oid, val in pMod.apiPDU.getVarBinds(reqPDU):
                
                if str(oid) == "1.3.6.1.4.1.49289.902.2.0":
                    if(int(val) == 0 or int(val) == 1):
                        if(loc_rem_var == False):
                            sw1pos2 = bool(int(val))
                            sw1pos1 = not(sw1pos2)
                            execute_sw1function()
                      
                if str(oid) == "1.3.6.1.4.1.49289.902.3.0":
                    if(int(val) == 0 or int(val)==1):
                        if(loc_rem_var == False):
                            sw2pos2 = bool(int(val))
                            sw2pos1 = not(sw2pos2)
                            execute_sw2function()
                       
                if str(oid) == "1.3.6.1.4.1.49289.902.4.0":
                    if(int(val) == 0 or int(val)==1):
                        if(loc_rem_var == False):
                            sw3pos2 = bool(int(val))
                            sw3pos1 = not(sw3pos2)
                            execute_sw3function()
        else:
            # Report unsupported request type
            pMod.apiPDU.setErrorStatus(rspPDU, 'genErr')
        pMod.apiPDU.setVarBinds(rspPDU, varBinds)
        # Commit possible error indices to response PDU
        for f, i in pendingErrors:
            f(rspPDU, i)
        transportDispatcher.sendMessage(
            encoder.encode(rspMsg), transportDomain, transportAddress
            )
    return wholeMsg
 

#---------------  For IP Address  -----------------------------------------
def setipfunc():
    global ipaddress,trapip,gateway,subnetmask
    global set_ipaddress,set_gateway,set_subnetmask, set_trapipval
    try:
        os.system("sudo ifconfig eth0 down")
        os.system("sudo ifconfig eth0 down")
        time.sleep(0.05)
        os.system("sudo ifconfig eth0 " + ipaddress + " netmask " + subnetmask)
        os.system("sudo route add default gw " + gateway + " eth0")
        #time.sleep(0.2)
        #os.system("sudo ifconfig eth0 up")
        #os.system("sudo ifconfig eth0 up")
        print("Set IP Config:",ipaddress, gateway, subnetmask)

    except Exception as e:
        print("setipfunc:",e)
        pass

def readipfunc():
    global ipaddress,trapip,gateway,subnetmask
    global set_ipaddress,set_gateway,set_subnetmask, set_trapipval
    try:
        fo = open("/home/user/ipconfig","r")
        allines = fo.readlines()
        fo.close()

        ipaddress1 = (allines[0]).rstrip()
        ipaddress = ".".join([str(int(i)) for i in ipaddress1.split(".")])
        gateway1 = (allines[1]).rstrip() 
        gateway = ".".join([str(int(i)) for i in gateway1.split(".")])
        subnetmask1 = (allines[2]).rstrip()
        subnetmask = ".".join([str(int(i)) for i in subnetmask1.split(".")])
        print("Read IP Config:",ipaddress, gateway, subnetmask)
        
    except Exception as e:
        print("readipfunc:",e)
        #global ipaddress,trapip,gateway,subnetmask
        ipaddress = "192.168.1.100"
        gateway = "192.168.1.1"
        subnetmask = "255.255.255.0"
        writeipfunc() 
        pass

def checkipfunc():
    global ipaddress,trapip,gateway,subnetmask
    global set_ipaddress,set_gateway,set_subnetmask, set_trapipval
    try:
        set_ipaddress = ".".join([str(int(i)) for i in set_ipaddress.split(".")])
        set_gateway = ".".join([str(int(i)) for i in set_gateway.split(".")])
        set_subnetmask = ".".join([str(int(i)) for i in set_subnetmask.split(".")])
        
        if (set_ipaddress != ipaddress or set_gateway != gateway or set_subnetmask != subnetmask):
            ipaddress = str(set_ipaddress)
            gateway = str(set_gateway)
            subnetmask = str(set_subnetmask)
            writeipfunc()
            command = "/usr/bin/sudo /sbin/shutdown -r now"
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            output = process.communicate()[0]
            
    except Exception as e:
        print("checkipfunc:",e)
        pass
        

def writeipfunc():
    global ipaddress,trapip,gateway,subnetmask
    global set_ipaddress,set_gateway,set_subnetmask, set_trapipval
    try:
        fo = open("/home/user/ipconfig","w")
        fo.write(str((ipaddress).rstrip() + "\n"))
        fo.write(str((gateway).rstrip() + "\n"))
        fo.write(str(subnetmask).rstrip())
        fo.close()
        print("Write ifconfig:", ipaddress, gateway, subnetmask)
        setipfunc()

    except Exception as e:
        print("write ipfunc:",e)
        pass


#------------------  RF Switch Position Read Function  --------------------------------
def read_sw_pos_sw1():
    global sw1pos1, sw1pos2
    try:
        GPIO.output(mux_s0, GPIO.HIGH) #Y1
        GPIO.output(mux_s1, GPIO.LOW)
        GPIO.output(mux_s2, GPIO.LOW)
        GPIO.output(mux_s3, GPIO.LOW)
        GPIO.output(mux_enable, GPIO.LOW)
        
        if(GPIO.input(mux_read) == GPIO.LOW):
                sw1pos1 = True
        else:
                sw1pos1 = False
        GPIO.output(mux_enable, GPIO.HIGH)
        
        GPIO.output(mux_s0, GPIO.LOW) #Y2
        GPIO.output(mux_s1, GPIO.HIGH)
        GPIO.output(mux_s2, GPIO.LOW)
        GPIO.output(mux_s3, GPIO.LOW)
        GPIO.output(mux_enable, GPIO.LOW)
        
        if(GPIO.input(mux_read)== GPIO.LOW):
                sw1pos2=True
        else:
                sw1pos2 = False
        GPIO.output(mux_enable, GPIO.HIGH)
        
        print(sw1pos1,sw1pos2)
    except Exception as e:
        print("read_sw_pos_sw1:",e)
        pass
    
def read_sw_pos_sw2():
    global sw2pos1, sw2pos2
    try:
        GPIO.output(mux_s0, GPIO.HIGH) #Y3
        GPIO.output(mux_s1, GPIO.HIGH)
        GPIO.output(mux_s2, GPIO.LOW)
        GPIO.output(mux_s3, GPIO.LOW)
        GPIO.output(mux_enable, GPIO.LOW)
        if(GPIO.input(mux_read) == GPIO.LOW):
            sw2pos1 = True
        else:
            sw2pos1 = False

        GPIO.output(mux_enable, GPIO.HIGH)
        
        GPIO.output(mux_s0, GPIO.LOW) #Y4
        GPIO.output(mux_s1, GPIO.LOW)
        GPIO.output(mux_s2, GPIO.HIGH)
        GPIO.output(mux_s3, GPIO.LOW)
        GPIO.output(mux_enable, GPIO.LOW)
        
        if(GPIO.input(mux_read) == GPIO.LOW):
            sw2pos2 = True
        else:
            sw2pos2 = False
        GPIO.output(mux_enable, GPIO.HIGH)
        
        print(sw2pos1,sw2pos2)
    except Exception as e:
        print("read_sw_pos_sw2:",e)
        pass


def read_sw_pos_sw3():
    global sw3pos1, sw3pos2
    try:
        GPIO.output(mux_s0, GPIO.HIGH) #Y5
        GPIO.output(mux_s1, GPIO.LOW)
        GPIO.output(mux_s2, GPIO.HIGH)
        GPIO.output(mux_s3, GPIO.LOW)
        GPIO.output(mux_enable, GPIO.LOW)
        
        if(GPIO.input(mux_read) == GPIO.LOW):
            sw3pos1 = True
        else:
            sw3pos1 = False
        GPIO.output(mux_enable, GPIO.HIGH)
        
        GPIO.output(mux_s0, GPIO.LOW) #Y6
        GPIO.output(mux_s1, GPIO.HIGH)
        GPIO.output(mux_s2, GPIO.HIGH)
        GPIO.output(mux_s3, GPIO.LOW)
        GPIO.output(mux_enable, GPIO.LOW)
        
        if(GPIO.input(mux_read) == GPIO.LOW):
            sw3pos2 = True
        else:
            sw3pos2 = False
        GPIO.output(mux_enable, GPIO.HIGH)
        
        print(sw3pos1,sw3pos2)
    except Exception as e:
        print("read_sw_pos_sw3:",e)
        pass

# -----------------  Front Panel LED Indicaton Function  ----------------------------
 
def check_latch1_enable_on(): 
    GPIO.output(latch1_enable, GPIO.HIGH)
    
    while(GPIO.input(latch1_enable) == GPIO.LOW): 
        GPIO.output(latch1_enable,GPIO.HIGH)
        
def check_latch1_enable_off(): 
    GPIO.output(latch1_enable, GPIO.LOW)
    
    while(GPIO.input(latch1_enable) == GPIO.HIGH): 
        GPIO.output(latch1_enable,GPIO.LOW)

def check_latch2_enable_on():
    GPIO.output(latch2_enable, GPIO.HIGH)
    
    while(GPIO.input(latch2_enable) == GPIO.LOW): 
        GPIO.output(latch2_enable,GPIO.HIGH)

def check_latch2_enable_off(): 
    GPIO.output(latch2_enable, GPIO.LOW)
    
    while(GPIO.input(latch2_enable) == GPIO.HIGH): 
        GPIO.output(latch2_enable,GPIO.LOW)
        
def check_latch3_enable_on():
    GPIO.output(latch3_enable, GPIO.HIGH)
    
    while(GPIO.input(latch3_enable) == GPIO.LOW): 
        GPIO.output(latch3_enable,GPIO.HIGH)

def check_latch3_enable_off(): 
    GPIO.output(latch3_enable, GPIO.LOW)
    
    while(GPIO.input(latch3_enable) == GPIO.HIGH): 
        GPIO.output(latch3_enable,GPIO.LOW)

def latch_led_func():
    global sw1pos1,sw2pos1,sw3pos1,sw1pos2,sw2pos2,sw3pos2,loc_rem_var

    try:
# ------------ Latch 1 - sw1 pos1&2  &  Sw2 pos1&2 -------------
 
        if(sw1pos1 == False):
            GPIO.output(d0_led, GPIO.LOW)        
        else:
            GPIO.output(d0_led, GPIO.HIGH) 

        
        if(sw1pos2 == False):
            GPIO.output(d1_led, GPIO.LOW)
        else:
            GPIO.output(d1_led, GPIO.HIGH)

        
        if(sw2pos1 == False):
            GPIO.output(d2_led, GPIO.LOW)
        else:
            GPIO.output(d2_led, GPIO.HIGH)
        
        if(sw2pos2 == False):
            GPIO.output(d3_led, GPIO.LOW)
        else:
            GPIO.output(d3_led, GPIO.HIGH)

        GPIO.output(latch1_enable, GPIO.HIGH)
        check_latch1_enable_on()
        
        GPIO.output(latch1_enable, GPIO.LOW)
        check_latch1_enable_off()

# ------------ Latch 2 - sw3 pos1&2  &  Sw4 pos1&2 -------------

        if(sw3pos1 == False):
            GPIO.output(d0_led, GPIO.LOW)        
        else:
            GPIO.output(d0_led, GPIO.HIGH) 

        
        if(sw3pos2 == False):
            GPIO.output(d1_led, GPIO.LOW)
        else:
            GPIO.output(d1_led, GPIO.HIGH)

        GPIO.output(latch2_enable, GPIO.HIGH)
        check_latch2_enable_on()
        
        GPIO.output(latch2_enable, GPIO.LOW)
        check_latch2_enable_off()

# ------------ Latch 3 - sw5 pos1&2  &  local remote leds -------------

        if(loc_rem_var == True):
            
            GPIO.output(d2_led, GPIO.LOW) # Local Mode
            GPIO.output(d3_led, GPIO.HIGH)
        else:
            GPIO.output(d2_led, GPIO.HIGH) #remote mode
            GPIO.output(d3_led, GPIO.LOW)

        GPIO.output(latch3_enable, GPIO.HIGH)
        check_latch3_enable_on()

        GPIO.output(latch3_enable, GPIO.LOW)
        check_latch3_enable_off()
        
    except Exception as e:
        print("latch_led_func:",e)
        pass

# -------------  Switch Press Functions  ---------------------------

def execute_sw1function():
    global sw1pos1,sw2pos1,sw3pos1,sw1pos2,sw2pos2,sw3pos2,loc_rem_var
    
    if(sw1pos1 == False):
        
        GPIO.output(decod_a0, GPIO.HIGH) # out - Y1 
        GPIO.output(decod_a1, GPIO.LOW)
        GPIO.output(decod_a2, GPIO.LOW)
        GPIO.output(decod_a3, GPIO.LOW)
        GPIO.output(decod_enable1, GPIO.LOW)
        GPIO.output(decod_enable2, GPIO.LOW)

    if(sw1pos2 == False ):
        GPIO.output(decod_a0, GPIO.LOW) # out - Y2
        GPIO.output(decod_a1, GPIO.HIGH)
        GPIO.output(decod_a2, GPIO.LOW)
        GPIO.output(decod_a3, GPIO.LOW)
        GPIO.output(decod_enable1, GPIO.LOW)
        GPIO.output(decod_enable2, GPIO.LOW)
    time.sleep(0.1)
    read_sw_pos_sw1()
    latch_led_func()


def execute_sw2function():
    global sw1pos1,sw2pos1,sw3pos1,sw1pos2,sw2pos2,sw3pos2,loc_rem_var
            
    if(sw2pos1 == False):
        GPIO.output(decod_a0, GPIO.HIGH)
        GPIO.output(decod_a1, GPIO.HIGH)
        GPIO.output(decod_a2, GPIO.LOW)
        GPIO.output(decod_a3, GPIO.LOW)
        GPIO.output(decod_enable1, GPIO.LOW)
        GPIO.output(decod_enable2, GPIO.LOW)
    if(sw2pos2 == False):
        GPIO.output(decod_a0, GPIO.LOW)
        GPIO.output(decod_a1, GPIO.LOW)
        GPIO.output(decod_a2, GPIO.HIGH)
        GPIO.output(decod_a3, GPIO.LOW)
        GPIO.output(decod_enable1, GPIO.LOW)
        GPIO.output(decod_enable2, GPIO.LOW)
    time.sleep(0.1)
    read_sw_pos_sw2()
    latch_led_func()


def execute_sw3function():
    global sw1pos1,sw2pos1,sw3pos1,sw1pos2,sw2pos2,sw3pos2,loc_rem_var
    if(sw3pos1 == False):
        GPIO.output(decod_a0, GPIO.HIGH)
        GPIO.output(decod_a1, GPIO.LOW)
        GPIO.output(decod_a2, GPIO.HIGH)
        GPIO.output(decod_a3, GPIO.LOW)
        GPIO.output(decod_enable1, GPIO.LOW)
        GPIO.output(decod_enable2, GPIO.LOW)

    if(sw3pos2 == False):
        GPIO.output(decod_a0, GPIO.LOW)
        GPIO.output(decod_a1, GPIO.HIGH)
        GPIO.output(decod_a2, GPIO.HIGH)
        GPIO.output(decod_a3, GPIO.LOW)
        GPIO.output(decod_enable1, GPIO.LOW)
        GPIO.output(decod_enable2, GPIO.LOW)
    time.sleep(0.1)
    read_sw_pos_sw3()
    latch_led_func()



def execute_lclrem_sw_func():
    global loc_rem_var
    if((GPIO.input(lclrem_sw) == GPIO.HIGH)):
        if (loc_rem_var == True):
            pass
        else:
            loc_rem_var = True #Local mode
            latch_led_func()
    else:
        if (loc_rem_var == False):
            pass
        else:
            loc_rem_var = False  #Remote mode
            latch_led_func()

def lclrem_sw_func(channel):
    execute_lclrem_sw_func()

def conv1_sw_func(channel):
    print("SW1 Low")
    if (loc_rem_var == True):
        execute_sw1function()

def conv2_sw_func(channel):
    print("SW2 Low")
    if (loc_rem_var == True):
        execute_sw2function()

def servo_sw_func(channel):
    print("SW3 Low")
    if (loc_rem_var == True):
        execute_sw3function()

def lineamp_sw_func(channel):
    print("SW4 Low")

def aupc_sw_func(channel):
    print("SW5 Low")

# -------------------  SNMP Get & Set Functions  -------------------------


transportDispatcher = AsynsockDispatcher()
transportDispatcher.registerRecvCbFun(cbFun)


# UDP/IPv4
transportDispatcher.registerTransport(
    udp.domainName, udp.UdpSocketTransport().openServerMode(('localhost', 161))
)

# UDP/IPv6
transportDispatcher.registerTransport(
    udp6.domainName, udp6.Udp6SocketTransport().openServerMode(('::', 161))
)

transportDispatcher.jobStarted(1)

class runsnmp(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            transportDispatcher.runDispatcher()
        except:
            transportDispatcher.closeDispatcher()
            raise


class runfunc(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            execute_lclrem_sw_func()
            time.sleep(0.1)

class setsnmp(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        def cbFun(transportDispatcher, transportDomain, transportAddress, wholeMsg):
            while wholeMsg:
                msgVer = int(api.decodeMessageVersion(wholeMsg))
                if msgVer in api.protoModules:
                    pMod = api.protoModules[msgVer]
                else:
                    print('Unsupported SNMP version %s' % msgVer)
                    return 
            reqMsg, wholeMsg = decoder.decode( wholeMsg, asn1Spec=pMod.Message(),)
            ipadressrecd =  (str(transportAddress).split(',')[0].replace('(',''))

            reqPDU = pMod.apiMessage.getPDU(reqMsg)

            if reqPDU.isSameTypeWith(pMod.setPDU()):
                print("set command received")
                if msgVer == api.protoVersion1:
                    print('Enterprise: %s' % (pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()))
                    print('Agent Address: %s' % (pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()))
                    print('Generic Trap: %s' % (pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()))
                    print('Specific Trap: %s' % (pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()))
                    print('Uptime: %s' % (pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()))
                    varBinds = pMod.apiTrapPDU.getVarBindList(reqPDU)
                else:
                    varBinds = pMod.apiPDU.getVarBindList(reqPDU)

                for name in varBinds:
                    strin = name.prettyPrint()
                    st = strin.splitlines()
                    for row in st:
                        if "1.3.6.1.6.3.1.1.4.1.0" in row:
                            for nrow in st:
                                if "-value" in nrow:
                                    trpid = nrow
                                    #print(trpid.split('=',1)[-1])
                                    trpid = (trpid.split('=',1)[-1])
                                    #sendsos(ipadressrecd,trpid)

            return wholeMsg

            transportDispatcher = AsynsockDispatcher()

            transportDispatcher.registerRecvCbFun(cbFun)
            ipv4 = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]
            # UDP/IPv4
            transportDispatcher.registerTransport(udp.domainName, udp.UdpSocketTransport().openServerMode((ipv4, 162)))
            # UDP/IPv6
            transportDispatcher.registerTransport(udp6.domainName, udp6.Udp6SocketTransport().openServerMode(('::1', 162)))

            transportDispatcher.jobStarted(1)

# --------------------- START PROGRAM ---------------------

# ------------------  RPi Pins Configurations  -----------------
# ---------------   PCB 1   -------------------

''' RF Input Pins'''
mux_enable = 23
mux_s0 = 15
mux_s1 = 14
mux_s2 = 2
mux_s3 = 3
mux_read = 4

''' RF Output Pins'''
decod_a0 = 7
decod_a1 = 1
decod_a2 = 12
decod_a3 = 16
decod_enable1 = 20
decod_enable2 = 22

''' local remote sw '''
lclrem_sw = 24

# ---------------   PCB 2   -------------------
''' Input Switch Pins'''
conv1_sw = 17
conv2_sw = 27
servo_sw = 10
lineamp_sw = 9
aupc_sw = 11

''' Output LEDs Pins'''
latch1_enable = 19
latch2_enable = 26
latch3_enable = 21

d0_led = 0 # conv1 port 1 & servo port 1 & aupc port 1
d1_led = 5 # conv1 port 2 & servo port 2 & aupc port 2
d2_led = 6 # conv2 port 1 & lineamp port 1 & local led
d3_led = 13 # conv2 port 2 & lineamp port 2 & remote led

#------------------   Variable   -----------------------

loc_rem_var = False #True- local, False- remote

ipaddress =""
trapip = ""
gateway =""
subnetmask= ""

# ----------------------------------------------------------


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(decod_a0 , GPIO.OUT)
GPIO.setup(decod_a1 , GPIO.OUT)
GPIO.setup(decod_a2 , GPIO.OUT)
GPIO.setup(decod_a3 , GPIO.OUT)
GPIO.setup(decod_enable1 , GPIO.OUT)
GPIO.setup(decod_enable2 , GPIO.OUT)
GPIO.setup(latch1_enable, GPIO.OUT)
GPIO.setup(latch2_enable, GPIO.OUT)
GPIO.setup(latch3_enable, GPIO.OUT)

GPIO.setup(d0_led, GPIO.OUT)
GPIO.setup(d1_led, GPIO.OUT)
GPIO.setup(d2_led, GPIO.OUT)
GPIO.setup(d3_led, GPIO.OUT)

GPIO.setup(mux_enable, GPIO.OUT)
GPIO.setup(mux_s0, GPIO.OUT)
GPIO.setup(mux_s1, GPIO.OUT)
GPIO.setup(mux_s2, GPIO.OUT)
GPIO.setup(mux_s3, GPIO.OUT)
GPIO.setup(mux_read, GPIO.IN)

GPIO.setup(conv1_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(conv2_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(servo_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(lineamp_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(aupc_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(lclrem_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(conv1_sw, GPIO.FALLING, callback = conv1_sw_func,bouncetime=500)
GPIO.add_event_detect(conv2_sw, GPIO.FALLING, callback = conv2_sw_func,bouncetime=500)
GPIO.add_event_detect(servo_sw, GPIO.FALLING, callback = servo_sw_func,bouncetime=500)
GPIO.add_event_detect(lineamp_sw, GPIO.RISING, callback = lineamp_sw_func,bouncetime=500)
GPIO.add_event_detect(aupc_sw, GPIO.RISING, callback=aupc_sw_func,bouncetime=500)
#lclrem_sw
#GPIO.add_event_detect(lclrem_sw, GPIO.RISING, callback=lclrem_sw_func,bouncetime=500)
# ----------------------------------------------------------


readipfunc()
setipfunc()

read_sw_pos_sw1() # Read all SW1 position read
read_sw_pos_sw2() # Read all SW2 position read
read_sw_pos_sw3() # Read all SW3 position read
 
latch_led_func() #Set all LEDs
execute_lclrem_sw_func() # read local remote Sw

a = runsnmp()
a.start()
b = runfunc()
b.start()


# ---------------------  Web Page Code  -------------------------------------

def getcurrentstat():
    global sw1pos1,sw2pos1,sw3pos1,sw1pos2,sw2pos2,sw3pos2,loc_rem_var
    global ipaddress,trapip,gateway,subnetmask

    try:

        resp = ["0","0","0", "0", "0", "0", "0"]
        if(sw1pos1 == False):
            resp[0] = "Position 1"
        else:
            resp[0] = "Position 2"
        if(sw2pos1 == False):
            resp[1] = "Position 1"
        else:
            resp[1] = "Position 2"
        if(sw3pos1 == False):
            resp[2]="Position 1"
        else:
            resp[2]="Position 2"
        if(loc_rem_var == True):
            resp[3]="Local mode"
        else:
            resp[3] ="Remote mode"

        resp[4] = ipaddress
        resp[5] = gateway
        resp[6] = subnetmask

        return resp

    except Exception as e:
        print("getcurrentstat:",e)
        resp = ["0","0","0", "0", "0", "0", "0"]
        return resp
        pass

app = Flask(__name__, template_folder='/home/pi/Templates')
log = logging.getLogger('werkzeug')
log.disabled = True

@app.route('/_load1', methods=['GET', 'POST'])
def load1():
    st = getcurrentstat()

    return jsonify(converter1=st[0],converter2=st[1], tracking=st[2], lclrem_web = st[3], webipaddress = st[4], webgatewayadd = st[5], websubnetmask = st[6])


@app.route('/', methods=['GET', 'POST'])
def index():
    global set_ipaddress,set_gateway,set_subnetmask, set_trapipval
    try:

        if (request.method == "POST"):
            btnval = request.form['btnval']

            if (btnval == "Converter1"):
                if (loc_rem_var == False):
                    if (sw1pos1 == False):
                        sw1pos2 = False
                        sw1pos2 = True
                    else:
                        sw1pos2 = True
                        sw1pos2 = False
                    execute_sw1function()
            elif (btnval == "Converter2"):
                if (loc_rem_var == False):
                    if (sw2pos1 == False):
                        sw2pos2 = False
                        sw2pos2 = True
                    else:
                        sw2pos2 = True
                        sw2pos2 = False
                    execute_sw2function()

            elif (btnval == "Tracking"):
                if (loc_rem_var == False):
                    if (sw3pos1 == False):
                        sw3pos2 = False
                        sw3pos2 = True
                    else:
                        sw3pos2 = True
                        sw3pos2 = False
                    execute_sw3function()
            else:
                set_ipaddress = request.form['ipaddress']
                set_gateway = request.form['gatewayadd'] 
                set_subnetmask = request.form['subnetmask']
                checkipfunc()

            return redirect(request.url)
        st = getcurrentstat()
        return render_template('index.html',converter1=st[0],converter2=st[1],tracking=st[2], lclrem_web = st[3], webipaddress = st[4], webgatewayadd = st[5], websubnetmask = st[6])

    except Exception as e:
        print("index:",e)
        st = getcurrentstat()
        return render_template('index.html',converter1=st[0],converter2=st[1],tracking=st[2], lclrem_web = st[3], webipaddress = st[4], webgatewayadd = st[5], websubnetmask = st[6])
        pass

app.run(host='0.0.0.0', port=80, debug=False)

#--------------------------------------------------------------------------------------------



#Ku-Band RF Uplink Switching Unit - COSW33Ku
#Version: V 1.2.0
#Last Update: 14-03-22

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




# ---------------------  Web Page Code  -------------------------------------  <form action ="" method ="post" onsubmit="return validate2(this);" ></form>

def getcurrentstat():
    global sw1pos1,sw2pos1,sw3pos1,sw4pos1,sw5pos1,sw1pos2,sw2pos2,sw3pos2,sw4pos2,sw5pos2,loc_rem_var
    global ipaddress,trapip,gateway,subnetmask
    try:
        resp = ["0","0","0","0","0","0","0", "0", "0", "0"]
        if(sw1pos1!=sw1pos2):
            if(sw1pos1 == False):
                resp[0] = "Position 1"
            else:
                resp[0] = "Position 2"
        else:
            resp[0] = "Unknown"
        if(sw2pos1 != sw2pos2):
            if(sw2pos1 == False):
                resp[1] = "Position 1"
            else:
                resp[1] = "Position 2"
        else:
            resp[1] = "Unknown"
        if(sw3pos1 != sw3pos2):
            if(sw3pos1 == False):
                resp[2]="Position 1"
            else:
                resp[2]="Position 2"
        else:
            resp[2]="Unknown"

        if(sw4pos1!= sw4pos2):
            if(sw4pos1 == False):
                resp[3] = "Position 1"
            else:
                resp[3] = "Position 2"
        else:
            resp[3] = "Unknown"
            
        if(sw5pos1 != sw5pos2):
            if(sw5pos1 == False):
                resp[4] = "Position 1"
            else:
                resp[4] = "Position 2"
        else:
            resp[4] = "Unknown"
        if(sw6pos1!= sw6pos2):
            if(sw6pos1 == False):
                resp[5]="Position 1"
            else:
                resp[5]="Position 2"
        else:
            resp[5] = "Unknown"
        if(loc_rem_var == True):
            resp[6]="Local mode"
        else:
            resp[6] ="Remote mode"

        resp[7] = ipaddress
        resp[8] = gateway
        resp[9] = subnetmask

        return resp

    except Exception as e:
        print("getcurrentstat:",e)
        resp = ["0","0","0","0","0","0", "0", "0", "0", "0"]
        return resp
        pass

app = Flask(__name__, template_folder='/home/pi/Templates')
log = logging.getLogger('werkzeug')
log.disabled = True

@app.route('/_load1', methods=['GET', 'POST'])
def load1():
    st = getcurrentstat()

    return jsonify(webws1=st[0],webws2=st[1], webws3=st[2],webcs1=st[3],webcs2=st[4], webcs3=st[5], lclrem_web = st[6] ,webipaddress = st[7], webgatewayadd = st[8], websubnetmask = st[9])


@app.route('/', methods=['GET', 'POST'])
def index():
    global set_ipaddress,set_gateway,set_subnetmask, set_trapipval
    try:

        if (request.method == "POST"):
            btnval = request.form['btnval']

            if (btnval == "websw1"):
                if (loc_rem_var == False):
                    if (sw1pos1 == False):
                        #sw1pos2 = False
                        sw1pos2 = True
                        print("sw1")
                    else:
                        #sw1pos2 = True
                        sw1pos2 = False
                        print("sw2")
                    execute_sw1function()
            elif (btnval == "websw2"):
                if (loc_rem_var == False):
                    if (sw2pos1 == False):
                        sw2pos2 = False
                        sw2pos2 = True
                    else:
                        sw2pos2 = True
                        sw2pos2 = False
                    execute_sw2function()

            elif (btnval == "websw3"):
                if (loc_rem_var == False):
                    if (sw3pos1 == False):
                        sw3pos2 = False
                        sw3pos2 = True
                    else:
                        sw3pos2 = True
                        sw3pos2 = False
                    execute_sw3function()
            if (btnval == "websw4"):
                if (loc_rem_var == False):
                    if (sw4pos1 == False):                        
                        sw4pos2 = True                        
                    else:                        
                        sw4pos2 = False                        
                    execute_sw4function()
            elif (btnval == "websw5"):
                if (loc_rem_var == False):
                    if (sw5pos1 == False):                        
                        sw5pos2 = True
                    else:                        
                        sw5pos2 = False
                    execute_sw5function()

            elif (btnval == "websw6"):
                if (loc_rem_var == False):
                    if (sw6pos1 == False):                        
                        sw6pos2 = True
                    else:                        
                        sw6pos2 = False
                    execute_sw6function()                    
            else:
                set_ipaddress = request.form['ipaddress']
                set_gateway = request.form['gatewayadd'] 
                set_subnetmask = request.form['subnetmask']
                checkipfunc()

            return redirect(request.url)
        st = getcurrentstat()
        return render_template('index.html',webws1=st[0],webws2=st[1], webws3=st[2],webcs1=st[3],webcs2=st[4], webcs3=st[5], lclrem_web = st[6] ,webipaddress = st[7], webgatewayadd = st[8], websubnetmask = st[9])

    except Exception as e:
        print("index:",e)
        st = getcurrentstat()
        return render_template('index.html',webws1=st[0],webws2=st[1], webws3=st[2],webcs1=st[3],webcs2=st[4], webcs3=st[5], lclrem_web = st[6] ,webipaddress = st[7], webgatewayadd = st[8], websubnetmask = st[9])
        pass

app.run(host='0.0.0.0', port=80, debug=False)

#--------------------------------------------------------------------------------------------

#Ku-Band RF Downlink Switching Unit - Four RF
#Version: V 1.3.0
#Last Update: 10-03-22

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



# ---------------------  Web Page Code  -------------------------------------

def getcurrentstat():
    global sw1pos1,sw2pos1,sw3pos1,sw1pos2,sw2pos2,sw3pos2,loc_rem_var
    global ipaddress,trapip,gateway,subnetmask
    global sw4pos1, sw4pos2, sw5pos1, sw5pos2

    try:

        resp = ["0","0","0", "0", "0", "0", "0", "0" , "0"]
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
        
        if(sw4pos1 == False):
            resp[7] = "Position 1"
        else:
            resp[7] = "Position 2"
        if(sw5pos1 == False):
            resp[8] = "Position 1"
        else:
            resp[8] = "Position 2"
            
            
        return resp

    except Exception as e:
        print("getcurrentstat:",e)
        resp = ["0","0","0", "0", "0", "0", "0", "0", "0"]
        return resp
        pass

app = Flask(__name__, template_folder='/home/pi/Templates')
log = logging.getLogger('werkzeug')
log.disabled = True

@app.route('/_load1', methods=['GET', 'POST'])
def load1():
    st = getcurrentstat()

    return jsonify(converter1=st[0],converter2=st[1], tracking=st[2], lclrem_web = st[3], webipaddress = st[4], webgatewayadd = st[5], websubnetmask = st[6], lineamp = st[7], AUPC=st[8])


@app.route('/', methods=['GET', 'POST'])
def index():
    global set_ipaddress,set_gateway,set_subnetmask, set_trapipval
    try:

        if (request.method == "POST"):
            btnval = request.form['btnval']
            if (btnval == "Converter1"):
                if (loc_rem_var == False):
                    if (sw1pos1 == False):
                        sw1pos2 = True
                    else:
                        sw1pos2 = False
                    execute_sw1function()
            elif (btnval == "Converter2"):
                if (loc_rem_var == False):
                    if (sw2pos1 == False):
                        sw2pos2 = True
                    else:
                        sw2pos2 = False
                    execute_sw2function()

            elif (btnval == "Tracking"):
                if (loc_rem_var == False):
                    if (sw3pos1 == False):
                        sw3pos2 = True
                    else:
                        sw3pos2 = False
                    execute_sw3function()
            elif (btnval == "lineamp"):
                if (loc_rem_var == False):
                    if (sw4pos1 == False):
                        sw4pos2 = True
                    else:
                        sw4pos2 = False
                    execute_sw4function()
                    
            elif (btnval == "aupc"):
                if (loc_rem_var == False):
                    if (sw5pos1 == False):
                        sw5pos2 = True
                    else:
                        sw5pos2 = False
                    execute_sw5function()            
            else:
                set_ipaddress = request.form['ipaddress']
                set_gateway = request.form['gatewayadd'] 
                set_subnetmask = request.form['subnetmask']
                checkipfunc()

            return redirect(request.url)
        st = getcurrentstat()
        return render_template('index.html',converter1=st[0],converter2=st[1],tracking=st[2], lclrem_web = st[3], webipaddress = st[4], webgatewayadd = st[5], websubnetmask = st[6], lineamp = st[7], AUPC=st[8])

    except Exception as e:
        print("index:",e)
        st = getcurrentstat()
        return render_template('index.html',converter1=st[0],converter2=st[1],tracking=st[2], lclrem_web = st[3], webipaddress = st[4], webgatewayadd = st[5], websubnetmask = st[6], lineamp = st[7], AUPC=st[8])
        pass

app.run(host='0.0.0.0', port=80, debug=False)

#--------------------------------------------------------------------------------------------



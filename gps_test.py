import serial
import time
import sys
from submodules import *
from threading import Thread
from core import config
import logging


#EDIT THIS TO WORK WITH GPS

def on_startup():
    global bperiod, t1, ser
    bperiod = 60
    serialPort = config['aprs']['serial_port']
    ser = serial.Serial(serialPort, 19200)
    t1 = Thread(target=listen, args=())
    t1.daemon = True
    t1.start()

def send(msg):
    msg += "\n"
    ser.write(msg.encode("utf-8"))
def listen():
    while(True):
        zz = ser.inWaiting()
        rr = ser.read(size = zz)
        if zz > 0:
            time.sleep(.5)
            zz = ser.inWaiting()
            rr += ser.read(size = zz)
            print(rr)
            log('GOT: '+rr)
def keyin():
    while(True):
        #GET INPUT FROM YOUR OWN TERMINAL
        #TRY input("shihaoiscoolforcommentingstuff") IF raw_input() doesn't work
        in1 = input("Type Command: ")
        send("TJ" + in1 + chr(sum([ord(x) for x in "TJ" + in1]) % 128))
def on_startup():
    #GLOBAL VARIABLES ARE NEEDED IF YOU "CREATE" VARIABLES WITHIN THIS METHOD
    #AND ACCESS THEM ELSEWHERE
    global bperiod, t1, ser, logfile
    bperiod = 60
    #serialPort = config['aprs']['serial_port']
    #REPLACE WITH COMx IF ON WINDOWS
    #REPLACE WITH /dev/ttyUSBx if 1 DOESNT WORK
    serialPort = "/dev/ttyUSB0"
    #OPENS THE SERIAL PORT FOR ALL METHODS TO USE WITH 19200 BAUD
    ser = serial.Serial(serialPort, 19200)
    #CREATES A THREAD THAT RUNS THE LISTEN METHOD
    t1 = Thread(target=listen, args=())
    t1.daemon = True
    t1.start()
    tlt = time.localtime()
    filename = 'gps'+'-'.join([str(x) for x in tlt[0:3]])
    logfile = open('/home/pi/TJREVERB/pFS/submodules/logs/gps/'+filename+'.txt','a+')
    log('RUN@'+'-'.join([str(x) for x in tlt[3:5]]))

# I NEED TO KNOW WHAT NEEDS TO BE DONE IN NORMAL, LOW POWER, AND EMERGENCY MODES
def enter_normal_mode():
    global bperiod
    bperiod = 60


def enter_low_power_mode():
    global bperiod
    bperiod = 120

def enter_emergency_mode():
    pass

#USE THIS LOG FUNCTION
def log(msg):
    global logfile
    logfile.write(msg+'\n')
    logfile.flush()

if __name__ == '__main__':
    startup()
    serialPort = sys.argv[1]
    ser = serial.Serial(serialPort, 19200)
    t2 = Thread(target=keyin, args=())
    t2.daemon = True
    t2.start()
    while True:
        time.sleep(1)
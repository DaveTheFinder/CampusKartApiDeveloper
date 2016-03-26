#- Main code -#
#!/usr/bin/python
import math
import serial
import time
import struct
from evdev import InputDevice, categorize, ecodes, KeyEvent
import sys
from api import Api


#File to write the data
archivo = open("coordenadasTm.txt","a")
archivo.write("Inicio\n")

#Interface with the controller
gamepad = InputDevice("/dev/input/event0")
print(gamepad)

direccionFinal = 1

#Instance of the API
api = Api("carroV1")

velocity = 0
manual = True

while True:    
    event = gamepad.read_one()
    x = api.Read()
    if(x == True):
        velocity = 0
        api.POSTVel(velocity)
        print("EMERGENCIA")
    if event != None:
        #print(event)
        if event.code == 17 and event.value == -1:
           
                    
            velocity = velocity + 1
            if velocity >= 10:
                velocity = 10
                    
        if event.code == 17 and event.value == 1:
            velocity = velocity -1
            if(velocity <= 0):
                velocity = 0
        if event.code == 315 and event.value == 1:
            manual = not manual
        if event.code == 305 and event.value == 1:
            velocity = 0
        if event.code == 310 and event.value == 1:
            #compassHeading = get_KartHeading(hmc5883l)
            t = time.process_time()
            
        if event.code == 311 and event.value == 1:
            elapsed = time.process_time() - t
            print("elapsed " + str(elapsed))
            archivo.write(str(elapsed)+"\n")
        api.POSTVel(velocity)
        #print("Velocidad" + str(velocity))
        #time.sleep(.01)
        #16.54948489399999
        #Inicio
        #8.913049059000002
    if(manual):
        if(event != None):
            if (event.code == 3 or event.code == 0) and event.type == 3:
                direccionFinal = int((event.value + 32768)/256)
                #print("DireccionC2 "+ str(direccionFinal))
                api.POSTDir(int(direccionFinal/(255/50)))
                print("DireccionC2 " + str(int(direccionFinal/(255/50))))
    if(not manual):
        print("Primera")
        api.POSTDir(25)
        t1 = time.process_time()
        while(time.process_time()-t1 < 16.54948):
            event = gamepad.read_one()
            if(event != None and event.value != 0):
                manual = True
                break
        #time.sleep(16.54948489399999)
        print("Segunda")
        api.POSTDir(0)
        t2 = time.process_time()
        while(time.process_time()-t2 < 10):
            event = gamepad.read_one()
            if(event != None and event.value != 0):
                manual = True
                break
        #time.sleep(10.913049059000002)
        print("tercera")
        api.POSTDir(25)
        manual = True


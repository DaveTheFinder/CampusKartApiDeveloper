import threading
from queue import Queue
import globalVariables
import time
import serial
import struct
import os
from Velocidad import Velocidad
from Direccion import Direccion
from controller import Joystick
#import RPI.GPIO as GPIO

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(false)
#GPIO.setup(18,GPIO.OUT)

class Master:
        def __init__(self):
                puertos = (os.popen("ls /dev/ttyACM*").read()).split()
                #for x in puertos:
                        #print(x)
                        #ser = scan(x,q)
                
                #try:
                        
                thread1 = Joystick(1, "Controller")
                thread1.start()
                while 1:
                        print(globalVariables.fila.get()[0])
                        print(globalVariables.fila.get()[1])
                        
        #recibe x que es el nombre del puerto

        def printing(self):
                x =0
                while x < 10:
                        globalVariables.fila.put("main")
                        #GPIO.output(18,GPIO.HIGH)
                        #time.sleep(1)
                        #GPIO.output(18,GPIO.LOW)
                        #time.sleep(1)
                        x = x+1
                        
        def scan(self,x,q):
                ser= serial.Serial(
                        port = x,
                        baudrate = 9600,
                        parity = serial.PARITY_NONE,
                        stopbits = serial.STOPBITS_ONE,
                        bytesize = serial.EIGHTBITS,
                        timeout = 10
                )
                ser.flushInput()
                ser.flushOutput()
                buffer_out = 0
                buffer_in = bytearray(1)
                bytesToRead = 0
                print("waiting")
                while(bytesToRead <= 0):
                        bytesToRead = ser.inWaiting()
                        print(ser.inWaiting())
                buffer_in = ser.read()
                print("not waiting")
                print('{:}'.format(buffer_in))
                #x = input()
                print("Sending message: ")
                print(buffer_in)
                string = struct.pack('!B',int(buffer_in))
                if(int(buffer_in) == 1):
                        print("Arduino de Velocidad")
                        arduinoVel = Velocidad(ser)
                        arduinoVel.sendSpeed(string)
                if(int(buffer_in) == 2):
                        print("Arduino De Direccion")
                        arduinoDir = Direccion(ser)
                        arduinoDir.initialize(string)
                        while(1):
                                y = input("Grados:")
                                y = struct.pack("!B",int(y))
                                arduinoDir.sendDirection(y)
                        

master = Master()		


import socket
import os
from carroV1 import CarroV1
from carrito import Carrito

class Api:

    def __init__(self, version):
        self. arduinoList = []
        if version == "carrito":
            arduino = Carrito(os.popen("ls /dev/ttyACM*").read())
            self.arduinoList = [arduino]
        elif version == "carroV1":
            puertos = (os.popen("ls /dev/ttyACM*").read()).split()
            for puerto in puertos:
                arduino = CarroV1(puerto)
                self.arduinoList += [arduino]
        print(self.arduinoList)
        
    def POSTDir(self, number):
        msg = "Direccion, " + str(number)
        print(msg)
        for(arduino in self.arduinoList):
            arduino.sendDirection(number)
     
        #self.s.sendall()
    def POSTSentido(self):
        self.carrito.Reverse()
    
    def POSTVel(self, number):
        msg = "Velocidad, " + str(number)
        print(msg)
        for arduino in self.arduinoList):
            arduino.sendSpeed(number)
        
    def GETDir(self):
        print("Consiguiendo")

    def getVel(self):
        print("velocity")
        

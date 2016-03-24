import time
import serial
import struct

class Velocidad:

    def __init__(self,ser):
        self.ser = ser
        
    def sendSpeed(self,speed):
        print("Writing in class....")
        self.ser.write(speed)
        

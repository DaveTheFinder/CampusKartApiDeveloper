import time
import serial
import struct
from queue import Queue

class Direccion:
    #ser is an instance of the Serial Class
    def __init__(self,puerto):
        #puertos = (os.popen("ls /dev/ttyACM*").read()).split()
        ser= serial.Serial(
                        port = x,
                        baudrate = 9600,
                        parity = serial.PARITY_NONE,
                        stopbits = serial.STOPBITS_ONE,
                        bytesize = serial.EIGHTBITS,
                        timeout = 10
                )
        self.ser = ser
        
    def sendDirection(self,angle):
        print("Writing in class....")
        self.ser.write(angle)
        buffer_in = bytearray(1)
        bytesToRead = 0
        print("esperando")
        while(bytesToRead<=0):
            bytesToRead = self.ser.inWaiting()
        buffer_in=self.ser.readline()
        print("{:}".format(buffer_in))
        
    def initialize(self,angle):
        print("Writing in class init....")
        self.ser.write(angle)

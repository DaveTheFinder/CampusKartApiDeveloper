import time
import serial
import struct

class Carrito:
    #ser is an instance of the Serial Class
    def __init__(self,puerto):
        ser= serial.Serial(
                        port = puerto,
                        baudrate = 9600,
                        parity = serial.PARITY_NONE,
                        stopbits = serial.STOPBITS_ONE,
                        bytesize = serial.EIGHTBITS,
                        timeout = 10
                )
        
        self.ser = ser
        self.ser.flushOutput()
        self.ser.flushInput()
        self.vel = 0
        self.dir = 90
        self.sentido = 0
        
    def sendDirection(self,angle):
        cero = 0
        self.dir = angle
        #angle = chr(angle)
        vel = chr(self.vel)
        mylist = [self.vel,self.sentido,self.vel,self.sentido,angle]
        for byte in mylist:
            string = struct.pack('!B',int(byte))
            print(int(byte))
            self.ser.write(string)
        
    def Reverse(self):
        if self.sentido == 0:
            self.sentido = 1
        else:
            self.sentido = 0
            
    def sendSpeed(self,vel):
        self.ser.flushOutput()
        self.vel = vel
        cero = 0
        #vel = chr(vel)
        direccion = chr(self.dir)
        mylist = [vel,self.sentido,vel,self.sentido,self.dir]
        #print(vel)
        #print(self.dir)
        #mylist = bytearray([self.dir,cero,vel,cero,vel])
        #for byte in mylist:
         #   print(byte)
        #self.ser.write(mylist)
        for byte in mylist:
            string = struct.pack('!B',int(byte))
            print(bytes(string))
            #print(str(byte))
            self.ser.write(string)
        
    

import time
import serial
import struct

class CarroV1:
    #ser is an instance of the Serial Class
    def __init__(self, puerto):
        ser = serial.Serial(
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
        
    def sendDirection(self, angle):
        mylist = [100, angle]
        for byte in mylist:
            string = struct.pack('!B', int(byte))
            print(bytes(string))
            self.ser.write(string)
            
    def sendSpeed(self, vel):
        mylist = [118, vel]
        for byte in mylist:
            string = struct.pack('!B', int(byte))
            print(bytes(string))
            #print(str(byte))
            self.ser.write(string)
        
    

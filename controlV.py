import time
import serial
import struct
import os

puertos = (os.popen("ls /dev/ttyACM*").read()).split()

#recibe x que es el nombre del puerto
def scan(x):
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
		
for x in puertos:
	ser = scan(x)
		

ser = serial.Serial(
	port =puertos[0],
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

string = ''

while 1:
	x = input()
	print("Sending message: ")
	print(x)
	string = struct.pack('!B',int(x))
	ser.write(string)
	bytesToRead = 0
	while(bytesToRead <= 0):
		bytesToRead = ser.inWaiting()
	buffer_in = ser.readline()
	print('{:}'.format(buffer_in))

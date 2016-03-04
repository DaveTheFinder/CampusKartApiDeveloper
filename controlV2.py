import time
import serial
import struct

ser = serial.Serial(
	port = '/dev/ttyACM2',
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
	time.sleep(3)

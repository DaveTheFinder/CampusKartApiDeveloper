import sys
sys.path.append('/usr/local/lib/python3.5/site-packages')
from evdev import InputDevice, categorize, ecodes, KeyEvent

#args: inputdevice,event.code1,evento.code2

class Joystick():

    def __init__(self, *args):
       self.gamepad = InputDevice(args[0])
       self.callback = args[1]
       self.read()
           
           
       
       
       
    def read(self):
        
        #print(self.gamepad.capabilities())
        print(self.gamepad)
        
        
        for event in self.gamepad.read_loop():
            self.callback(event)
            """
            if event.type == ecodes.EV_ABS and event.code == self.direccion:
                if(self.valueDirection != int(event.value)):
                    self.valueDirection = int(event.value)
                    self.callback(event)
            elif event.type == ecodes.EV_ABS and event.code == 49:
                if(self.valueVel != int(event.value)):
                    self.valuesVel= int(event.value)
                    self.callback(event)
               """     

             



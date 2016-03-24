from evdev import InputDevice, categorize, ecodes, KeyEvent

#args: inputdevice,event.code1,evento.code2

class Joystick():

    def __init__(self, *args):
       self.gamepad = InputDevice(args[0])
       self.callback = args[1]
       self.valueDirection = 0
       self.valueVel = 0
       self.argumentos = args
       self.read()
       print("error: Demasiados Argumentos")
           
           
       
       
       
    def read(self):
        
        #print(self.gamepad.capabilities())
        print(self.gamepad)
        
        
        for event in self.gamepad.read_loop():
            for argumento in range (2,len(self.argumentos)):
                if event.code == self.argumentos[argumento]:
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

             


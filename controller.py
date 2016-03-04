from evdev import InputDevice, categorize, ecodes, KeyEvent
import time
from queue import Queue 
import globalVariables
import threading
class Joystick(threading.Thread):

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        gamepad = InputDevice("/dev/input/event3")
        #print(gamepad.capabilities())
        print(gamepad)
        valuesDirection, valuesSpeed = 0, 0
        constantDirection = 255/80
        constantSpeed = 255/40

        for event in gamepad.read_loop():
            if event.type == ecodes.EV_ABS and event.code == 00: 
                absevent = categorize(event)
                if(valuesDirection != int(event.value/constantDirection)):
                    valuesDirection = int(event.value/constantDirection)
                    list1 = ["girar",valuesDirection-40]
                    globalVariables.fila.put(list1)
                    #print(valuesDirection-40)
            elif event.type == ecodes.EV_ABS and event.code == 49:
                absevent = categorize(event)
                if(valuesSpeed != int(event.value/constantSpeed)):
                    valuesSpeed = int(event.value/constantSpeed)
                    list2=["velocidad",valuesSpeed/4]
                    globalVariables.fila.put(list2)

            if event.type == ecodes.EV_KEY:
                keyevent = categorize(event)
                if keyevent.keystate == KeyEvent.key_down:
                    if keyevent.keycode == 'BTN_BASE2':
                        print ("Left")
                    elif keyevent.keycode == 'BTN_PINKIE':
                        print ("Right")
                    elif keyevent.keycode == 'BTN_TOP2':
                        print ("Forward")
                    elif keyevent.keycode == 'BTN_BASE':
                        print ("Backward") 

#control = Joystick()
#control.joystickManager()

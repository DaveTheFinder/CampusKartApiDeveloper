from controllerF import Joystick
from api import Api
import time

#00 direccion 49 velovidad analoga, 294 arriba, 292 abajo
def callback(event):
    if event.code == 00 and event.type == 3:
        print(int(event.value/(255/80))-40)
        api.POSTDir(int(event.value/(255/80))+50)
        #time.sleep(1)
    elif event.code == 49:
        api.POSTVel(event.value)
        #time.sleep(1)
    elif event.code == 292 and event.value == 1:
        api.POSTSentido()  

api = Api("carrito")

joystick = Joystick("/dev/input/event0",callback)

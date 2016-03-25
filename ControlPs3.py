from controllerF import Joystick
from api import Api
import time

#00 direccion 49 velovidad analoga, 294 arriba, 292 abajo
def callback(event):
    global reversa
    if event.code == 3 and event.type == 3:
        direccionF = int((event.value + 32768)/256)
        print("DireccionC2 "+ str(direccionF))
        api.POSTDir(int(direccionF/(255/80))+50)
    elif event.code == 5 or event.code == 2:
        if event.code == 5 and reversa:
            reversa = False
            api.POSTSentido()
        if event.code == 2 and not reversa:
            reversa = True
            api.POSTSentido()
        api.POSTVel(int(event.value))
        #time.sleep(1)
        #print("Velocidad")
    elif event.code == 292 and event.value == 1:
        api.POSTSentido()  

api = Api("carrito")
reversa = False
joystick = Joystick("/dev/input/event0",callback)

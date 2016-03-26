from controllerF import Joystick
from api import Api
import time

#00 direccion 49 velovidad analoga, 294 arriba, 292 abajo
def callback(event):
    global reversa
    global velocity
    print(event)
    if (event.code == 3 or event.code == 0) and event.type == 3:
        direccionF = int((event.value + 32768)/256)
        print("DireccionC2 "+ str(direccionF))
        api.POSTDir(int(direccionF/(255/50)))
        print("DIreccionC2 " + str(int(direccionF/(255/50))))
        #time.sleep(1)
        #print("Velocidad")
    if event.code == 17 and event.value == -1:
        velocity = velocity + 1
        print(velocity)
        if velocity >= 10:
            velocity = 10
        api.POSTVel(velocity)
    if event.code == 17 and event.value == 1:
        velocity = velocity -1
        if(velocity <= 0):
            velocity = 0
        print(velocity)
        api.POSTVel(velocity)
    if event.code == 315 and event.value == 1:
        time.sleep(5)
    if event.code == 305 and event.value == 1:
        velocity = 0
        api.POSTVel(velocity)  
while True:
    try:
        api = Api("carroV1")
        reversa = False
        velocity = 0
        joystick = Joystick("/dev/input/event0",callback)
    except:
        pass
    else:
        break
    print("Reiniciando")
    time.sleep(5)

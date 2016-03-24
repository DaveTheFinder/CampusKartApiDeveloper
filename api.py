import socket

from carrito import Carrito

class Api:

    def __init__(self):
        self.s = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 12347                # Reserve a port for your service.
        #self.s.connect((host, port))
        self.carrito = Carrito("/dev/ttyACM0")

    def POSTDir(self,number):
        msg = "Direccion," + str(number)
        print(msg)
        self.carrito.sendDirection(number)
     
        #self.s.sendall()
    def POSTSentido(self):
        self.carrito.Reverse()
    
    def POSTVel(self,number):
        msg = "Velocidad," + str(number)
        print(msg)
        self.carrito.sendSpeed(number)
        
        
        

    def GETDir(self):
        print("Consiguiendo")

    def getVel(self):
        print("velocity")
        

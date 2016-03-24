
#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import threading
class Cliente(threading.Thread):
    def __init__(self,inicialMsg):
        self.inicial = inicialMsg
        self.s = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 12347                # Reserve a port for your service.

        self.s.connect((host, port))
        print self.s.recv(16)
        self.s.sendall("control,1")
        print self.s.recv(16)
        self.s.close                     # Close the socket when done

    def send(self,mensaje):
        self.s.sendall(mensaje)

    def listen(self):
        while 1:
            self.s.recv(16)
        

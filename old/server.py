#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
from objectClient import Client

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12347                # Reserve a port for your service.

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
c, addr = s.accept()     # Establish connection with client.

print 'Got connection from', addr

nombre = c.recv(1024)
comandos = nombre.split(",")

print comandos

objeto = Client(c,nombre)

lista =[objeto]
lista[0].connection.send("Muy bien")
c.close()                # Close the connection
s.close()


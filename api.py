from queue import Queue
import globalVariables
import socket
import sys

HOST = None
PORT = 50007

class api:
    
    def POST(self,name,number):
        list1 = [name,number]
        globalVariables.fila.put(list1)

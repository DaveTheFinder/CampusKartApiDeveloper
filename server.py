from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from api import Api

from config import *

import os
import signal

# Protocol for managing MovingRaspiRemote commands
class MovingRaspi(Protocol):

  def __init__(self):
    self.api = Api("carrito")
  
  def connectionMade(self):
    print("A client connected")

  def dataReceived(self, data):
    coordinates = []
    dataRec = data.decode()
    print(dataRec)
    
    coordinates = dataRec.split(',')
    
    if coordinates[1] == "Angle":
      angleVar = float(coordinates[2])
      angle = int(angleVar)
      self.api.POSTDir(angle)
    elif coordinates[1] == "Speed":
      speedVar = float(coordinates[2])
      speed = int(speedVar)
      self.api.POSTVel(speed)

   # print("Angle: ", angleVar + " Speed: ", speedVar)
 

def stop():
    print("STOP")

# Called on process interruption. Set all pins to "low level" output.
def endProcess(signalnum = None, handler = None):
    stop()
 
    reactor.stop()

# Get current pid
pid = os.getpid()

# Save current pid for later use
try:
    fhandle = open('/var/run/movingraspi.pid', 'w')
except IOError:
    print ("Unable to write /var/run/movingraspi.pid")
    exit(1)
fhandle.write(str(pid))
fhandle.close()

# Prepare handlers for process exit
signal.signal(signal.SIGTERM, endProcess)
signal.signal(signal.SIGINT, endProcess)
signal.signal(signal.SIGHUP, endProcess)

# Init and start server
factory = Factory()
factory.protocol = MovingRaspi
reactor.listenTCP(PORT, factory, 50, IFACE)
reactor.run()

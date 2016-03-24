import threading

class ServerNode(threading.Thread):
    
    def __init__(self,connection, threadID,name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.connection = connection

    def run(self):
        while 1:
            command = self.connection.connection.recv(16)
            print command
            
            

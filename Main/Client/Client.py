from Common.Utils import PacketTypes, getConfig
from threading import Thread
from time import sleep
from Common.Serialization import pack, deserialize
import socket

class ClientConnection:
    
    def __init__(self):
        self.setupVariables()
        
    def setupVariables(self):
        self.stopped = False
    
    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        config = getConfig()
        self.conn.connect((config.ServerAddress, config.Port))
        self.packetSize = config.PacketSize
        
        Thread(target=self.ping).start()
        Thread(target=self.recieve).start()

    def ping(self):
        while not self.stopped:
            self.send(PacketTypes.PING, None)
            sleep(3)
            
    def recieve(self):
        while not self.stopped and self.conn:
            try:
                data = deserialize(self.conn.recv(self.packetSize))
                self.packetHandler.handlePacket(data, self)
            except:
                self.disconnect()     
                
    def disconnect(self):
        print "Disconnect Called"
        self.stopped = True
        if self.conn:
            self.conn.close()
            self.conn = None    
            
    def send(self, message, data):
        packet = pack(message, data)
        if(self.conn):
            self.conn.send(packet)     
        
import Common.Serialization as Serialization
from Common.Utils import PacketTypes
from threading import Thread
from time import sleep

class ClientConnection:
    
    def __init__(self, packetHandler, client, ID, accountName):
        self.packetHandler = packetHandler
        self.accountName = accountName
        self.dataSize = 1024
        self.client = client
        self.ID = ID
        self.loop()
        
    def loop(self):
        print self.accountName + " has connected!"
        while self.client:
            try:
                packet = self.client.recv(self.dataSize)
                data = Serialization.deserialize(packet)
                self.packetHandler.handlePacket(data, self)
            except:
                self.client.close()
                self.client = None
            
    def send(self, message, data):
        packet = Serialization.pack(message, data)
        if self.client:
            self.client.send(packet)
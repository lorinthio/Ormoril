import Common.Serialization as Serialization
from Common.Utils import PacketTypes
from threading import Thread
from time import sleep

class ClientConnection:
    
    def __init__(self, server, packetHandler, client, ID, accountName):
        self.server = server
        self.packetHandler = packetHandler
        self.accountName = accountName
        self.dataSize = 1024
        self.client = client
        self.ID = ID
        self.loop()
        
    def notifyPlayerLoggedOn(self, username):
        self.send(PacketTypes.PLAYER_ONLINE, {"username": username})
        
    def notifyPlayerLoggedOff(self, username):
        self.send(PacketTypes.PLAYER_OFFLINE, {"username": username})          
        
    def loop(self):
        Thread(target=self.ping).start()
        print self.accountName + " has connected!"
        while self.client:
            try:
                packet = self.client.recv(self.dataSize)
                data = Serialization.deserialize(packet)
                self.packetHandler.handlePacket(data, self)
            except:
                self.close()
    
    def ping(self):
        while True:
            sleep(1.5)
            self.send(PacketTypes.PING, None)
            sleep(1.5)    
                
    def close(self):
        print self.accountName + " has disconnected! ({})".format(reason)
        if self.client:
            try:
                self.server.playerLogoff(self, self.accountName)
                self.client = None
                self.send(PacketTypes.FORCE_CLOSE, None)
                self.client.close()
            except:
                pass # Client closed connection
        
    def send(self, message, data):
        packet = Serialization.pack(message, data)
        if self.client:
            self.client.send(packet)
            
    
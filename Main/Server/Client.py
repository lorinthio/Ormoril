import Common.Serialization as Serialization
from Common.Utils import PacketTypes
from threading import Thread
from time import sleep

class ClientConnection:
    
    def __init__(self, packetHandler, client, ID):
        self.packetHandler = packetHandler
        self.dataSize = 1024
        self.client = client
        self.ID = ID
        self.loop()
        
    def loop(self):
        print "Player connected with instance ID : " + str(self.ID)
        Thread(target=self.fakeDamage).start()
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
        
    def fakeDamage(self):
        health = 200
        mana = 100
        
        while health > 0 or mana > 0:
            if(health > 0):
                health -= 1
            if(mana > 0):
                mana -= 1
            self.send(PacketTypes.CHARACTER_VITAL_TICK, {"curHealth": health, "maxHealth": 200, "curMana": mana, "maxMana": 100})
            sleep(0.25)
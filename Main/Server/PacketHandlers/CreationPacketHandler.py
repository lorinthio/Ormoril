from Common.Utils import PacketTypes, sendPacketToClient
from Common.ModLoader import ModLoader
from random import randint

class CreationPacketHandler:
    
    def __init__(self, Server, Database):
        self.server = Server
        self.database = Database
    
    def handlePacket(self, packet, client):
        msg = packet["message"]
        data = packet["data"]
        
        if msg == PacketTypes.CREATION_CLASSES:
            sendPacketToClient(client, PacketTypes.CREATION_CLASSES, ModLoader.classes)
        elif msg == PacketTypes.CREATION_RACES:
            sendPacketToClient(client, PacketTypes.CREATION_RACES, ModLoader.races)
        elif msg == PacketTypes.CREATION_RANDOMIZE:
            self.handleRandomizeStats(client)
            
    def handleRandomizeStats(self, client):
        stats = []
        for i in range(6):
            stat = 0
            for i in range(4):
                stat += randint(2, 5)
            stats.append(stat)
        
        sendPacketToClient(client, PacketTypes.CREATION_RANDOMIZE, stats)
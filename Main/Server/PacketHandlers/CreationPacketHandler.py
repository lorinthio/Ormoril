from Common.Utils import PacketTypes, sendPacketToClient
from Common.ModLoader import ModLoader
from random import randint

class CreationPacketHandler:
    
    def __init__(self, Server, Database):
        self.server = Server
        self.database = Database
        self.randomValues = {}
    
    def handlePacket(self, packet, client):
        msg = packet["message"]
        data = packet["data"]
        
        if msg == PacketTypes.CREATION_CLASSES:
            sendPacketToClient(client, PacketTypes.CREATION_CLASSES, ModLoader.classes)
        elif msg == PacketTypes.CREATION_RACES:
            sendPacketToClient(client, PacketTypes.CREATION_RACES, ModLoader.races)
        elif msg == PacketTypes.CREATION_RANDOMIZE:
            self.handleRandomizeStats(data["username"], client)
        elif msg == PacketTypes.CREATION_FINAL:
            self.handleHeroCreation(client, data)
            
    def handleRandomizeStats(self, username, client):
        stats = []
        for i in range(6):
            stat = 0
            for i in range(4):
                stat += randint(2, 5)
            stats.append(stat)
        
        self.randomValues[username] = stats
        
        sendPacketToClient(client, PacketTypes.CREATION_RANDOMIZE, stats)
        
    def handleHeroCreation(self, client, data):
        stats = self.randomValues[data["username"]]
        Race = data["race"]
        Class = data["class"]
        sentStats = data["stats"]
        difference = 0 
        for i in range(6):
            difference += sentStats[i] - stats[i]
            
        if difference > 6:
            sendPacketToClient(client, PacketTypes.CREATION_INVALID, None)
        elif difference == 6:
            sendPacketToClient(client, PacketTypes.CREATION_SUCCESS, None)
        else:
            sendPacketToClient(client, PacketTypes.CREATION_INVALID, None)
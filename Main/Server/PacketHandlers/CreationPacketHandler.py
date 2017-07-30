from Common.Utils import PacketTypes, sendPacketToClient
from Common.ModLoader import ModLoader

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
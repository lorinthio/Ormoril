class PlayerPacketHandler:
    
    def __init__(self, Server, Database):
        self.server = Server
        self.database = Database
        
    def handlePacket(self, data, client):
        return
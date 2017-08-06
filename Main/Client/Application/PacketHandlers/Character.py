from Common.Utils import PacketTypes

class CharacterPacketHandler:
    
    def __init__(self, client, window):
        self.client = client
        self.window = window
    
    def handlePacket(self, packet):
        message = packet["message"]
        data = packet["data"]
        
        if message == PacketTypes.CHARACTER_VITAL_TICK:
            self.window.changeVital("health", data["curHealth"], data["maxHealth"])
            self.window.changeVital("mana", data["curMana"], data["maxMana"])
        return
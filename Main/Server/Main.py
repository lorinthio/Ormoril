from threading import Thread
from Database.Database import DatabaseService
from PacketHandlers.AccountPacketHandler import AccountPacketHandler
from PacketHandlers.PlayerPacketHandler import PlayerPacketHandler
from PacketHandlers.CreationPacketHandler import CreationPacketHandler
from Client import ClientConnection
from Common.ModLoader import ModLoader
from Common.Utils import PacketTypes
import Common.Serialization as Serialization
import socket
import atexit

class Server:
    
    def __init__(self):
        self.players = {}
        self.modLoader = ModLoader()
        self.dbService = DatabaseService()
        self.accountPacketHandler = AccountPacketHandler(self, self.dbService)
        self.creationPacketHandler = CreationPacketHandler(self, self.dbService)
        self.playerPacketHandler = PlayerPacketHandler(self, self.dbService)
        self.currentID = 0
        self.playerCount = 0
        self.config = Config()
        self.host = ""
        self.port = self.config.port
        
        print "Server started on, {} on port {}".format("localhost", self.port)
        
    def listen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))        
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(5)
            Thread(target = self.handleClientConnection, args= (client, address)).start()
        
    def handleClientConnection(self, client, address):
        try:
            while True:
                packet = client.recv(2048)
                data = Serialization.deserialize(packet)
                msg = data["message"]
                if PacketTypes.LOGIN_PACKETS[0] <= msg and msg <= PacketTypes.ACCOUNT_PACKETS[1]:
                    self.accountPacketHandler.handlePacket(data, client)
                elif PacketTypes.CREATION_PACKETS[0] <= msg and msg <= PacketTypes.CREATION_PACKETS[1]:
                    self.creationPacketHandler.handlePacket(data, client)
        except Exception, e:
            if e.message != "":
                print e.message
            
    def close(self):
        print "Server closed"
        raw_input()
        return
            
    def playerLogin(self, client, username):
        self.currentID += 1
        self.playerCount += 1
        self.dbService.accountService.markPlayerOnline(username)
        for username, player in self.players.iteritems():
            player.notifyPlayerLoggedOn(username)
    
        oldUser = self.players.pop(username, None)
        if oldUser:
            oldUser.close()
        self.players[username] = ClientConnection(self, self.playerPacketHandler, client, self.currentID, username)
        
    def playerLogoff(self, player, username):
        self.playerCount -= 1
        self.players.pop(username, None)
        for username, player  in self.players.iteritems():
            player.notifyPlayerLoggedOff(username)

class Config:
    
    def __init__(self):
        self.port = 8123
        self.load()
        
    def load(self):
        configFile = open("config.txt", "r")
        for line in configFile.readlines():
            try:
                line = line.lower()
                if "port" in line:
                    self.port = int(line.replace("port:", "").strip())
            except:
                print "There was an issue with line,"
                print " > " + line
                print "in your config.txt"
        
if __name__ == "__main__":
    server = Server()
    atexit.register(server.close)
    server.listen()
    print "Server Closed..."
    print "Hit enter to close this window"
    raw_input()
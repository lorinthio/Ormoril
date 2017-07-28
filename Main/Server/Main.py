from threading import Thread
from Database import DatabaseService
from PacketHandlers.AccountPacketHandler import AccountPacketHandler
from PacketHandlers.PlayerPacketHandler import PlayerPacketHandler
from Client import ClientConnection
import Common.Serialization as Serialization
import socket

class Server:
    
    def __init__(self):
        self.players = []
        self.dbService = DatabaseService()
        self.accountPacketHandler = AccountPacketHandler(self, self.dbService)
        self.playerPacketHandler = PlayerPacketHandler(self, self.dbService)
        self.currentID = 0
        self.playerCount = 0
        self.config = Config()
        self.host = ""
        self.port = self.config.port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        print "Server started on, {} on port {}".format("localhost", self.port)
        
    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(5)
            Thread(target = self.handleClientConnection, args= (client, address)).start()
        
    def handleClientConnection(self, client, address):
        try:
            packet = client.recv(1024)
            data = Serialization.deserialize(packet)
            self.accountPacketHandler.handlePacket(data, client)
        except:
            pass
            
    def playerLogin(self, client, username):
        self.currentID += 1
        self.playerCount += 1
        self.dbService.markPlayerOnline(username)
        for player in self.players:
            player.notifyPlayerLoggedOn(username)
            
        print "Players Online : {}".format(self.playerCount)
        self.players.append(ClientConnection(self, self.playerPacketHandler, client, self.currentID, username))
        
    def playerLogoff(self, player, username):
        self.playerCount -= 1
        for player in self.players:
            player.notifyPlayerLoggedOff(username)
        print "Players Online : {}".format(self.playerCount)
        
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
    server = Server().listen()
    print "Server Closed..."
    print "Hit enter to close this window"
    raw_input()
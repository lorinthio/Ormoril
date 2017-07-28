from threading import Thread
from Database import DatabaseService
from PacketHandler import ServerPacketHandler
from Client import ClientConnection
import Common.Serialization as Serialization
import socket

class Server:
    
    def __init__(self):
        self.players = []
        self.dbService = DatabaseService()
        self.packetHandler = ServerPacketHandler(self, self.dbService)
        self.currentID = 0
        self.host = ""
        self.port = 8123
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
            self.packetHandler.handlePacket(data, client)
        except:
            pass
            
    def playerLogin(self, client):
        self.currentID += 1
        self.players.append(ClientConnection(self.packetHandler, client, self.currentID))
        
if __name__ == "__main__":
    server = Server().listen()
    print "Server Closed..."
    print "Hit enter to close this window"
    raw_input()
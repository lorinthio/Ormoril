from Common.Utils import PacketTypes
from PacketHandlers.Character import CharacterPacketHandler
from threading import Thread
from time import sleep
from Common.Serialization import pack, deserialize
import socket

class ClientConnection:
    
    def __init__(self, CharacterFrame):
        self.setupVariables(CharacterFrame)
        
    def setupVariables(self, CharacterFrame):
        self.stopped = False
        self.connected = False
        self.characterPacketHandler = CharacterPacketHandler(self, CharacterFrame)
    
    def connect(self, username, password):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.config = Config()
        self.conn.connect((self.config.ip, self.config.port))
        self.packetSize = 1024
        
        # Send Login Attempt Connect
        
        # If successful start threads
        self.attemptConnect(username, password)
        
        if self.connected:
            print "Client Connected!"
            Thread(target=self.ping).start()
            Thread(target=self.recieve).start()

    def attemptConnect(self, username, password):
        self.send(PacketTypes.LOGIN_ATTEMPT_CONNECT, {"username": username, "password": password})
        packet = deserialize(self.conn.recv(self.packetSize))
        message = packet["message"]
        
        #Player Login Attempt
        if message == PacketTypes.LOGIN_ATTEMPT_RESPONSE:
            success = packet["data"]["success"]
            if success:
                self.connected = True
            else:
                self.connected = False
                exit()        

    def loadConfig(self):
        self.config = Config()

    def ping(self):
        while not self.stopped:
            self.send(PacketTypes.PING, None)
            sleep(3)
            
    def recieve(self):
        while not self.stopped and self.conn:
            try:
                packet = deserialize(self.conn.recv(self.packetSize))
                message = packet["message"]
                
                #Player Login Attempt
                if message == PacketTypes.LOGIN_ATTEMPT_RESPONSE:
                    success = packet["data"]["success"]
                    if success:
                        self.connected = True
                    else:
                        self.connected = False
                        exit()
                if PacketTypes.CHARACTER_PACKETS[0] <= message and message <= PacketTypes.CHARACTER_PACKETS[1]:
                    self.characterPacketHandler.handlePacket(packet)
                
            except:
                self.disconnect()     
                
    def disconnect(self):
        print "Disconnect Called"
        self.stopped = True
        if self.conn:
            self.conn.close()
            self.conn = None    
            
    def send(self, message, data):
        packet = pack(message, data)
        if(self.conn):
            self.conn.send(packet)     
        
class Config:
    
    def __init__(self):
        self.ip = "localhost"
        self.port = 8123
        self.load()
        
    def load(self):
        configFile = open("config.txt", "r")
        for line in configFile.readlines():
            try:
                line = line.lower()
                if "ip" in line:
                    self.ip = line.replace("ip:", "").strip()
                elif "port" in line:
                    self.port = int(line.replace("port:", "").strip())
            except:
                print "There was an issue with line,"
                print " > " + line
                print "in your config.txt"
                
        print "Client Config is pointing to, {} : {}".format(self.ip, self.port)
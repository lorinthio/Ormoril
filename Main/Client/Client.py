from Common.Utils import PacketTypes
from PacketHandlers.Character import CharacterPacketHandler
from threading import Thread
from time import sleep
from Common.Serialization import pack, deserialize
import socket

class ClientConnection:
    
    stopped = False
    connected = False
    packetSize = 1024
    config = None
    characterPacketHandler = None
    player = None
    connection = None
    
    activeWindow = None
    
    def __init__(self, player):
        ClientConnection.loadConfig()
        ClientConnection.player = player
        ClientConnection.connect()
    
    @staticmethod
    def setCharacterFrame(CharacterFrame):
        characterPacketHandler = CharacterPacketHandler(self, CharacterFrame)
        
    @staticmethod
    def setActiveWindow(window):
        ClientConnection.activeWindow = window
    
    @staticmethod
    def connect():
        if not ClientConnection.connection:
            ClientConnection.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ClientConnection.connection.connect((ClientConnection.config.ip, ClientConnection.config.port))
            
            # If successful start threads
            ClientConnection.attemptConnect()
            
            if ClientConnection.connected:
                print "Client Connected!"
                Thread(target=ClientConnection.ping).start()
                Thread(target=ClientConnection.recieve).start()

    @staticmethod
    def attemptConnect():
        ClientConnection.send(PacketTypes.LOGIN_ATTEMPT_CONNECT, {"username": ClientConnection.player.username, "password": ClientConnection.player.password})
        packet = deserialize(ClientConnection.connection.recv(ClientConnection.packetSize))
        message = packet["message"]
        
        #Player Login Attempt
        if message == PacketTypes.LOGIN_ATTEMPT_RESPONSE:
            success = packet["data"]["success"]
            if success:
                ClientConnection.connected = True
                ClientConnection.player.heroes = packet["data"]["heroes"]
                ClientConnection.player.needToCreate = packet["data"]["forceToCreate"]
            else:
                connected = False

    @staticmethod
    def loadConfig():
        if not ClientConnection.config:
            ClientConnection.config = Config()

    @staticmethod
    def ping():
        while not ClientConnection.stopped:
            ClientConnection.send(PacketTypes.PING, None)
            sleep(3)
    
    @staticmethod
    def recieve():
        while not ClientConnection.stopped and ClientConnection.connection:
            try:
                packet = deserialize(ClientConnection.connection.recv(ClientConnection.packetSize))
                if packet:
                    message = packet["message"]
                    
                    #Player Login Attempt
                    if message == PacketTypes.LOGIN_ATTEMPT_RESPONSE:
                        success = packet["data"]["success"]
                        if success:
                            ClientConnection.connected = True
                        else:
                            ClientConnection.connected = False
                    elif message == PacketTypes.FORCE_CLOSE:
                        ClientConnection.disconnect()
                    elif PacketTypes.CHARACTER_PACKETS[0] <= message and message <= PacketTypes.CHARACTER_PACKETS[1]:
                        if ClientConnection.characterPacketHandler:
                            ClientConnection.characterPacketHandler.handlePacket(packet)
            except:
                ClientConnection.disconnect()     
                
    @staticmethod
    def disconnect():
        print "Disconnect Called"
        ClientConnection.stopped = True
        if ClientConnection.connection:
            ClientConnection.connection.close()
            ClientConnection.connection = None
        if ClientConnection.activeWindow:
            ClientConnection.activeWindow.destroy()
            
    @staticmethod
    def send(message, data):
        packet = pack(message, data)
        if ClientConnection.connection:
            ClientConnection.connection.send(packet)     
        
class Config:
    
    ip = None
    port = None
    
    def __init__(self):
        Config.load()
        
    @staticmethod
    def load():
        if not Config.ip:
            configFile = open("config.txt", "r")
            for line in configFile.readlines():
                try:
                    line = line.lower()
                    if "ip" in line:
                        Config.ip = line.replace("ip:", "").strip()
                    elif "port" in line:
                        Config.port = int(line.replace("port:", "").strip())
                except:
                    print "There was an issue with line,"
                    print " > " + line.strip()
                    print "in your config.txt"
                    
            print "Client Config is pointing to, {} : {}".format(Config.ip, Config.port)
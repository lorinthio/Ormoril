from Ormoril.Utils import PacketTypes
from PacketHandlers.Character import CharacterPacketHandler
from threading import Thread
from time import sleep
from Ormoril.Serialization import pack, deserialize
import socket

class ClientConnection:
    
    stopped = False
    connected = False
    packetSize = 1024
    config = None
    activePacketHandler = None
    clientPacketHandler = None
    player = None
    connection = None
    activeWindow = None
    
    def __init__(self, player):
        ClientConnection.setup()
        ClientConnection.player = player
        
    @staticmethod
    def setActiveWindow(window):
        ClientConnection.activeWindow = window
        
    @staticmethod
    def setActivePacketHandler(packetHandler):
        ClientConnection.activePacketHandler = packetHandler
    
    @staticmethod
    def connect():
        try:
            if not ClientConnection.connection:
                ClientConnection.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ClientConnection.connection.connect((ClientConnection.config.ip, ClientConnection.config.port))
                
                # If successful start threads
                ClientConnection.attemptConnect()
                
                if ClientConnection.connected:
                    print "Client Connected!"
                    Thread(target=ClientConnection.ping).start()
                    Thread(target=ClientConnection.recieve).start()
        except Exception, e:
            print e

    @staticmethod
    def attemptConnect():
        if ClientConnection.player.username.strip() != "" and ClientConnection.player.password.strip() != "":
            packet = ClientConnection.sendAndWait(PacketTypes.LOGIN_ATTEMPT_CONNECT, {"username": ClientConnection.player.username, "password": ClientConnection.player.password})
            message = packet["message"]
            if message == PacketTypes.LOGIN_ATTEMPT_RESPONSE:
                success = packet["data"]["success"]
                if success:
                    ClientConnection.connected = True
                    ClientConnection.player.heroes = packet["data"]["heroes"]
                    ClientConnection.player.needToCreate = packet["data"]["forceToCreate"]
                else:
                    connected = False

    @staticmethod
    def setup():
        if not ClientConnection.clientPacketHandler:
            ClientConnection.clientPacketHandler = ClientPacketHandler()        
        if not ClientConnection.config:
            ClientConnection.config = Config()

    @staticmethod
    def ping():
        while not ClientConnection.stopped:
            ClientConnection.send(PacketTypes.PING, None)
            sleep(3)
    
    @staticmethod
    def recieve():
        print "Start Recieve"
        while True:
            if ClientConnection.connection:
                try:
                    packet = deserialize(ClientConnection.connection.recv(ClientConnection.packetSize))
                    if packet:
                        ClientConnection.clientPacketHandler.handlePacket(packet)
                        if ClientConnection.activePacketHandler:
                            ClientConnection.activePacketHandler.handlePacket(packet)
                except:
                    ClientConnection.disconnect()
            else:
                sleep(0.25)
        print "End Recieve"
                
    @staticmethod
    def disconnect():
        print "Disconnect Called"
        ClientConnection.stopped = True
        if ClientConnection.connection:
            ClientConnection.connection.close()
            ClientConnection.connection = None
        if ClientConnection.activeWindow:
            try:
                ClientConnection.activeWindow.destroy()
            except:
                # swallowed error, means window is already closed
                pass
            
    @staticmethod
    def send(message, data):
        packet = pack(message, data)
        if ClientConnection.connection:
            try:
                ClientConnection.connection.send(packet)
            except Exception, error:
                print error
                ClientConnection.connection.close()
                ClientConnection.connection = None
                
    @staticmethod
    def sendAndWait(message, data, packetSize=1024):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            conn.connect((ClientConnection.config.ip, ClientConnection.config.port))
            packet = pack(message, data)
            conn.send(packet)
            data = conn.recv(packetSize)
            return deserialize(data)
        except Exception as error:
            print error
        finally:
            conn.close()
            
class ClientPacketHandler:
    
    def handlePacket(self, packet):
        if packet:
            message = packet["message"]
            if message == PacketTypes.FORCE_CLOSE:
                ClientConnection.disconnect()
                
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
from Common.Utils import PacketTypes
import Common.Serialization as Serialization
import Errors

class AccountPacketHandler:
    
    def __init__(self, Server, Database):
        self.server = Server
        self.database = Database
    
    def handlePacket(self, packet, client):
        msg = packet["message"]
        data = packet["data"]
        
        if(msg == PacketTypes.PLAYER_COUNT):
            self.handlePlayerCount(client)
        elif(msg == PacketTypes.LOGIN):
            self.handleLogin(data, client)
        elif(msg == PacketTypes.ACCOUNT_CREATE):
            self.handleAccountCreate(data, client)
        elif(msg == PacketTypes.LOGIN_ATTEMPT_CONNECT):
            self.handleConnect(data, client)
            
    def handlePlayerCount(self, client):
        sendPacketToClient(client, PacketTypes.PLAYER_COUNT, {"count": self.server.playerCount})
            
    def handleLogin(self, data, client):
        username = data["username"]
        password = data["password"]
        
        account = self.database.getAccountByName(username)
        if account:
            if username == account[1] and password == account[2]:
                sendPacketToClient(client, PacketTypes.LOGIN_SUCCESS, None)
            else:
                sendPacketToClient(client, PacketTypes.LOGIN_FAILURE, None)
        else:
            sendPacketToClient(client, PacketTypes.LOGIN_FAILURE, None)
            
    def handleAccountCreate(self, data, client):
        username = data["username"]
        password = data["password"]
        email = data["email"]
        
        if len(username) < 7 or len(username) > 20:
            # Usernames are between 7 and 20 characters long
            sendPacketToClient(client, PacketTypes.ACCOUNT_CREATE_FAILURE_INVALID_USERNAME, None)
            return
        elif not set('1234567890').intersection(password):
            # Password requires a number and special character
            sendPacketToClient(client, PacketTypes.ACCOUNT_CREATE_FAILURE_INVALID_PASSWORD, None)
            return
        elif '@' not in email:
            # Email requires @
            sendPacketToClient(client, PacketTypes.ACCOUNT_CREATE_FAILURE_INVALID_EMAIL, None)
            return
        elif self.database.getAccountByEmail(email):
            sendPacketToClient(client, PacketTypes.ACCOUNT_CREATE_FAILURE_EMAIL_EXISTS, None)
            return
        elif self.database.getAccountByName(username):
            sendPacketToClient(client, PacketTypes.ACCOUNT_CREATE_FAILURE_USERNAME_EXISTS, None)
            return
        
        try:
            self.database.createAccount(username, password, email)
            sendPacketToClient(client, PacketTypes.ACCOUNT_CREATE_SUCCESS, None)
        except Errors.AccountAlreadyExists:
            sendPacketToClient(client, PacketTypes.ACCOUNT_CREATE_FAILURE_ACCOUNT_EXISTS, None)
            
    def handleConnect(self, data, client):
        username = data["username"]
        password = data["password"]
        
        account = self.database.getAccountByName(username)
        if account:
            if username == account[1] and password == account[2]:
                sendPacketToClient(client, PacketTypes.LOGIN_ATTEMPT_RESPONSE, {"success": True})
                self.server.playerLogin(client, username)
            else:
                sendPacketToClient(client, PacketTypes.LOGIN_ATTEMPT_RESPONSE, {"success": False})           
        else:
            sendPacketToClient(client, PacketTypes.LOGIN_ATTEMPT_RESPONSE, {"success": False})
            
def sendPacketToClient(client, message, data):
    packet = Serialization.pack(message, data)
    client.send(packet)     
from Common.Utils import PacketTypes
import Errors

class ServerPacketHandler:
    
    def __init__(self, Server, Database):
        self.server = Server
        self.database = Database
    
    def handlePacket(self, packet, client):
        msg = packet["message"]
        data = packet["data"]
        
        if(msg == PacketTypes.LOGIN):
            self.handleLogin(data, client)
        elif(msg == PacketTypes.ACCOUNT_CREATE):
            self.handleAccountCreate(data, client)
            
    def handleLogin(self, data, client):
        username = data["username"]
        password = data["password"]
        
        account = self.database.getAccountByName(username)
        if account:
            if username == account[1] and password == account[2]:
                client.send(PacketTypes.LOGIN_SUCCESS, None)
            else:
                client.send(PacketTypes.LOGIN_FAILURE, None)
        else:
            client.send(PacketTypes.LOGIN_FAILURE, None)
            
    def handleAccountCreate(self, data, client):
        username = data["username"]
        password = data["password"]
        email = data["email"]
        
        if len(username) < 7 or len(username) > 20:
            # Usernames are between 7 and 20 characters long
            client.send(PacketTypes.ACCOUNT_CREATE_FAILURE_INVALID_USERNAME, None)
            return
        elif not set('1234567890').intersection(password):
            # Password requires a number and special character
            client.send(PacketTypes.ACCOUNT_CREATE_FAILURE_INVALID_PASSWORD, None)
            return
        elif '@' not in email:
            # Email requires @
            client.send(PacketTypes.ACCOUNT_CREATE_FAILURE_INVALID_EMAIL, None)
            return
        elif self.database.getAccountByEmail(email):
            client.send(PacketTypes.ACCOUNT_CREATE_FAILURE_EMAIL_EXISTS, None)
            return
        elif self.database.getAccountByName(username):
            client.send(PacketTypes.ACCOUNT_CREATE_FAILURE_USERNAME_EXISTS, None)
            return
        
        try:
            self.database.createAccount(username, password, email)
            client.send(PacketTypes.ACCOUNT_CREATE_SUCCESS, None)
        except Errors.AccountAlreadyExists:
            client.send(PacketTypes.ACCOUNT_CREATE_FAILURE_ACCOUNT_EXISTS, None)
        
        
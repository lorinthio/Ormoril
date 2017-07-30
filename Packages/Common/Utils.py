import Serialization as Serialization

class PacketTypes:
    
    # Common
    PING = 0
    
    ###################
    ##    Login
    ###################
    LOGIN_PACKETS = (5, 10)
    # Client
    PLAYER_COUNT = 5
    LOGIN = 6
    LOGIN_ATTEMPT_CONNECT = 7
    # Server
    LOGIN_SUCCESS = 8
    LOGIN_FAILURE = 9
    LOGIN_ATTEMPT_RESPONSE = 10
    
    ###################
    ##    Account 
    ###################
    ACCOUNT_PACKETS = (11,19)
    # Client
    ACCOUNT_CREATE = 11
    # Server
    ACCOUNT_CREATE_SUCCESS = 12
    ACCOUNT_CREATE_FAILURE_INVALID_USERNAME = 13
    ACCOUNT_CREATE_FAILURE_INVALID_PASSWORD = 14
    ACCOUNT_CREATE_FAILURE_INVALID_EMAIL = 15
    ACCOUNT_CREATE_FAILURE_EMAIL_EXISTS = 16
    ACCOUNT_CREATE_FAILURE_USERNAME_EXISTS = 17
    ACCOUNT_CREATE_FAILURE_ACCOUNT_EXISTS = 18
    
    ###################
    ##    Character 
    ###################    
    # Client
    CHARACTER_PACKETS = (20, 30)
    CHARACTER_SPEAK = 20
    CHARACTER_MOVE = 21
    CHARACTER_ATTACK = 22
    CHARACTER_SKILL = 23
    
    # Server
    CHARACTER_LOAD = 25
    CHARACTER_VITAL_TICK = 26
    
    ###################
    ##    Social 
    ###################
    # Server
    PLAYER_ONLINE = 40
    PLAYER_OFFLINE = 41
    CHARACTER_ONLINE = 42
    CHARACTER_OFFLINE = 43
    
    ###################
    ##    Creation 
    ###################
    # Server
    CREATION_PACKETS = (50, 55)
    CREATION_RACES = 50
    CREATION_CLASSES = 51
    

def sendPacketToClient(client, message, data):
    packet = Serialization.pack(message, data)
    client.send(packet)  

def toSqlString(value):
    return "'" + str(value) + "'"
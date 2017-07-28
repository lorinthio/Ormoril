class PacketTypes:
    
    # Common
    PING = 0
    
    ###################
    ##    Login
    ###################
    LOGIN_PACKETS = (5, 9)
    # Client
    LOGIN = 5
    # Server
    LOGIN_SUCCESS = 6
    LOGIN_FAILURE = 7
    
    ###################
    ##    Account 
    ###################
    ACCOUNT_PACKETS = (10,19)
    # Client
    ACCOUNT_CREATE = 10
    # Server
    ACCOUNT_CREATE_SUCCESS = 11
    ACCOUNT_CREATE_FAILURE_INVALID_USERNAME = 12
    ACCOUNT_CREATE_FAILURE_INVALID_PASSWORD = 13
    ACCOUNT_CREATE_FAILURE_INVALID_EMAIL = 14
    ACCOUNT_CREATE_FAILURE_EMAIL_EXISTS = 15
    ACCOUNT_CREATE_FAILURE_USERNAME_EXISTS = 16
    ACCOUNT_CREATE_FAILURE_ACCOUNT_EXISTS = 17
    
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
    

class Config:
    
    def __init__(self):
        self.ServerAddress = "localhost"
        self.Port = 8123
        self.PacketSize = 1024
        
def getConfig():
    return Config()

def toSqlString(value):
    return "'" + str(value) + "'"
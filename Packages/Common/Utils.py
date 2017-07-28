class PacketTypes:
    
    # Common
    PING = 0
    
    ###################
    ##    Login
    ###################
    LOGIN_PACKETS = (5, 9)
    # Client
    LOGIN = 5
    LOGIN_ATTEMPT_CONNECT = 6
    # Server
    LOGIN_SUCCESS = 7
    LOGIN_FAILURE = 8
    LOGIN_ATTEMPT_RESPONSE = 9
    
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
    
    ###################
    ##    Social 
    ###################
    # Server
    PLAYER_COUNT = 40
    PLAYER_ONLINE = 41
    PLAYER_OFFLINE = 42
    CHARACTER_ONLINE = 43
    CHARACTER_OFFLINE = 44

def toSqlString(value):
    return "'" + str(value) + "'"
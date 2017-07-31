import sqlite3
from threading import currentThread
from Common.Objects import Hero
from AccountService import AccountDatabaseService
from CharacterService import CharacterDatabaseService

class DatabaseService:
    
    def __init__(self):
        self.connections = {}
        self.accountService = AccountDatabaseService(self.getCursor, self.getDBConnection)
        self.characterService = CharacterDatabaseService(self.getCursor, self.getDBConnection)
        self.getDBConnection().commit()
        
    def getDBConnection(self):
        thread = currentThread()
        conn = None
        if thread in self.connections:
            conn = self.connections[thread]
        else:
            conn = sqlite3.connect('data.db')
            self.connections[thread] = conn
        return conn
    
    def getCursor(self):
        return self.getDBConnection().cursor()
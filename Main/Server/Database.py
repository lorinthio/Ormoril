import sqlite3
from threading import currentThread
import Errors
from Common.Utils import toSqlString

class DatabaseService:
    
    def __init__(self):
        self.connections = {}
        self.createTables()
        
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
        
    def createTables(self):
        self.getCursor().execute("CREATE TABLE IF NOT EXISTS accounts (id integer primary key autoincrement unique, username varchar(20) unique, password varchar(20), email varchar(50) unique, online integer, onlineAs varchar(20))")
        self.getCursor().execute("CREATE TABLE IF NOT EXISTS characters (id integer primary key autoincrement unique, accountId integer, name varchar(20), race varchar(20), level integer)")
        self.getCursor().execute("CREATE TABLE IF NOT EXISTS vitals (id integer primary key autoincrement unique, accountId integer, name varchar(20), race varchar(20), level integer)")
        self.getDBConnection().commit()

    #####################
    ## Accounts
    #####################

    def createAccount(self, name, password, email):
        nameAccount = self.getAccountByName(name)
        emailAccount = self.getAccountByEmail(email)
        if nameAccount or emailAccount:
            raise Errors.AccountAlreadyExists()
        else:
            c = self.getCursor()
            c.execute("insert into accounts (username, password, email, online, onlineAs) values ({}, {}, {}, {}, {})".format(toSqlString(name), toSqlString(password), toSqlString(email), 0, toSqlString("")))
            self.getDBConnection().commit()
        
    def getAccountByName(self, name):
        command = "select * from accounts where username = {}".format(toSqlString(name))
        c = self.getCursor()
        c.execute(command)
        data = c.fetchone()
        return data
    
    def getAccountByEmail(self, email):
        command = "select * from accounts where email = {}".format(toSqlString(email))
        c = self.getCursor()
        c.execute(command)
        data = c.fetchone()
        return data
    
    def markPlayerOnline(self, username):
        command = "update accounts set online={} where username={}".format(1, toSqlString(username))
        c = self.getCursor()
        c.execute(command)
        self.getDBConnection().commit()
        
    def markPlayerOffline(self, username):
        command = "update accounts set online={} where username={}".format(0, toSqlString(username))
        c = self.getCursor()
        c.execute(command)
        self.getDBConnection().commit()
from Common.Objects import Hero
from Common.ModLoader import ModLoader

class CharacterDatabaseService:
    
    def __init__(self, getCursor, getDBConnection):
        self.getCursor = getCursor
        self.getDBConnection = getDBConnection
        self.createTables()
        
    def createTables(self):
        # Characters
        self.getCursor().execute("CREATE TABLE IF NOT EXISTS characters (id integer primary key autoincrement unique, accountId integer, name varchar(20), level integer, race varchar(20), class varchar(20))")
        # Vitals
        self.getCursor().execute("CREATE TABLE IF NOT EXISTS vitals (id integer primary key autoincrement unique, characterId integer, health integer, mana integer)")
        # Core Stats
        self.getCursor().execute("CREATE TABLE IF NOT EXISTS statistics (id integer primary key autoincrement unique, characterId integer, strength integer, constitution integer, dexterity integer, agility integer, intelligence integer, wisdom integer)")
        
    def getPlayerHeroesByAccountId(self, accountId):
        heroes = []
        command = "select * from characters where accountId = {}".format(accountId)
        c = self.getCursor()
        c.execute(command)
        for row in c.fetchall():
            self.remakeHero(row)
        return heroes
            
    def remakeHero(self, data):
        hero = Hero()
        hero.ID = data[0]
        hero.name = data[2]
        hero.level = data[3]
        hero.Race = ModLoader.getRace(data[4])
        hero.Class = ModLoader.getClass(data[5])
        
        self.fetchVitals(hero)
        self.fetchStats()
        hero.rebuildStats()
        
    def fetchVitals(self, hero):
        command = "select * from vitals where characterId = {}".format(hero.ID)
        c = self.getCursor()
        c.execute(command)
        data = c.fetchone()
        
        if(data):
            hero.health = data[2]
            hero.mana = data[3]
            
    def fetchStats(self, hero):
        command = "select * from statistics where characterId = {}".format(hero.ID)
        c = self.getCursor()
        c.execute(command)
        data = c.fetchone()
        if data:
            hero.strength = data[2]
            hero.constitution = data[3]
            hero.dexterity = data[4]
            hero.agility = data[5]
            hero.intelligence = data[6]
            hero.wisdom = data[7]
from Tkinter import IntVar
from ModLoader import ModLoader

class Player:
    
    def __init__(self):
        self.setupVariables()
        
    def setupVariables(self):
        self.username = ""
        self.password = ""
        self.needToCreate = False
        self.isLoggedIn = False
        self.heroes = []
        self.hero = None
        
class Class:
    
    def __init__(self, name="", description="", abilities={}):
        self.name = name
        self.description = description
        self.abilities = abilities
        self.modload()
        
    def applyToHero(self, hero):
        hero.Class = self
        heroAbilities = hero.abilities
        for level, abilities in self.abilities:
            if level in heroAbilities:
                for ability in abilities:
                    if ability not in heroAbilities[level]:
                        heroAbilities[level].append(ability)
            else:
                heroAbilities[level] = abilities
                
    def modload(self):
        ModLoader.loadClass(self)    
        
class Race:
        
    def __init__(self, name="", description="", abilities={}, **kwargs):
        self.name = name
        self.description = description
        self.abilities = abilities
        self.setupVariables()
        self.handleKeywords(**kwargs)
        self.modload()
        
    def setupVariables(self):
        self.strength = 0 # melee damage
        self.constitution = 0 # health / physical defense
        self.dexterity = 0 # accuracy / crit
        self.agility = 0 # dodge / crit
        self.wisdom = 0 # mana / magic defense
        self.intelligence = 0 # magic damage
        
    def handleKeywords(self, **kwargs):
        if "strength" in kwargs:
            self.strength = kwargs["strength"]
        if "constitution" in kwargs:
            self.constitution = kwargs["constitution"]
        if "dexterity" in kwargs:
            self.dexterity = kwargs["dexterity"]
        if "agility" in kwargs:
            self.agility = kwargs["agility"]
        if "wisdom" in kwargs:
            self.wisdom = kwargs["wisdom"]
        if "intelligence" in kwargs:
            self.intelligence = kwargs["intelligence"]
        
        
    def applyToHero(self, hero):
        hero.Race = self
        
        hero.stats["strength"] = hero.strength + self.strength
        hero.stats["constitution"] = hero.constitution + self.constitution
        hero.stats["dexterity"] = hero.dexterity + self.dexterity
        hero.stats["agility"] = hero.agility + self.agility
        hero.stats["wisdom"] = hero.wisdom + self.wisdom
        hero.stats["intelligence"] = hero.intelligence + self.intelligence
        
        heroAbilities = hero.abilities
        for level, abilities in self.abilities:
            if level in heroAbilities:
                for ability in abilities:
                    if ability not in heroAbilities[level]:
                        heroAbilities[level].append(ability)
            else:
                heroAbilities[level] = abilities        
        
    def modload(self):
        ModLoader.loadRace(self)
        
class Hero:
    
    def __init__(self):
        self.setupVariables()
        
    def setupVariables(self):
        self.ID = 0
        self.level = 1
        self.name = ""
        self.abilities = {}
        self.Race = None
        self.Class = None
        
        # stats is a dictionary of currently active values where race, base stats, and equipment is combined into one single location
        self.stats = {
            "health": 100,
            "maxhealth": 100,
            "mana": 100,
            "maxmana": 100,
            
            "strength": 10,
            "constitution": 10,
            "dexterity": 10,
            "agility": 10,
            "wisdom": 10,
            "intelligence": 10,
            
            "pAttack": 20,
            "pDefense": 20,
            
            "mAttack": 20,
            "mDefense": 20,
            
            "accuracy": 100,
            "dodge": 5
        }
        
        self.health = 100
        self.maxhealth = 100
        self.mana = 100
        self.maxmana = 100
        
        self.strength = 10 # melee damage
        self.constitution = 10 # health / physical defense
        self.dexterity = 10 # accuracy / crit
        self.agility = 10 # dodge / crit
        self.wisdom = 10 # mana / magic defense
        self.intelligence = 10 # magic damage
        
        self.pAttack = 20
        self.pDefense = 20
        
        self.mAttack = 20
        self.mDefense = 20
        
        self.accuracy = 100
        self.dodge = 5
        
    def rebuildStats(self):
        self.stats["strength"] = self.strength
        self.stats["constitution"] = self.constitution
        self.stats["dexterity"] = self.dexterity
        self.stats["agility"] = self.agility
        self.stats["wisdom"] = self.wisdom
        self.stats["intelligence"] = self.intelligence
        
        if self.Race:
            self.Race.applyToHero(self)
        if self.Class:
            self.Class.applyToHero(self)
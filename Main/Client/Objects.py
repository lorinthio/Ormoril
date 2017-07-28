from Tkinter import IntVar

class Player:
    
    def __init__(self):
        self.setupVariables()
        
    def setupVariables(self):
        self.username = ""
        self.isLoggedIn = False
        
class Race:
        
    def __init__(self):
        self.setupVariables()
        
    def setupVariables(self):
        self.maxhealth = 0
        self.maxmana = 0
    
        self.strength = 0 # melee damage
        self.constitution = 0 # health / physical defense
        self.dexterity = 0 # accuracy / crit
        self.agility = 0 # dodge / crit
        self.wisdom = 0 # mana / magic defense
        self.intelligence = 0 # magic damage
    
        self.pAttack = 0
        self.pDefense = 0
    
        self.mAttack = 0
        self.mDefense = 0
    
        self.accuracy = 0
        self.dodge = 0    
        
    def applyToHero(self, hero):
        hero.race = self
        hero.stats["maxhealth"] = hero.maxhealth + self.maxhealth
        hero.stats["maxmana"] = hero.maxmana + self.maxmana
        
        hero.stats["strength"] = hero.strength + self.strength
        hero.stats["constitution"] = hero.constitution + self.constitution
        hero.stats["dexterity"] = hero.dexterity + self.dexterity
        hero.stats["agility"] = hero.agility + self.agility
        hero.stats["wisdom"] = hero.wisdom + self.wisdom
        hero.stats["intelligence"] = hero.intelligence + self.intelligence
        
        hero.stats["pAttack"] = hero.pAttack + self.pAttack
        hero.stats["pDefense"] = hero.pDefense + self.pDefense   
    
        hero.stats["mAttack"] = hero.mAttack + self.mAttack
        hero.stats["mDefense"] = hero.mDefense + self.mDefense
    
        hero.stats["accuracy"] = hero.accuracy + self.accuracy
        hero.stats["dodge"] = hero.dodge + self.dodge        
        
class Hero:
    
    def __init__(self):
        self.setupVariables()
        
    def setupVariables(self):
        self.name = ""
        self.race = None # Race Object
        
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
        self.healthVar = IntVar()
        self.maxhealth = 100
        self.mana = 100
        self.manaVar = IntVar()
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
        
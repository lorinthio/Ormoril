class ModLoader:

    abilities = []    
    classes = []
    creatures = []
    npcs = []
    quests = []
    races = []
    rooms = []
    
    def __init__(self):
        self.loadAbilities()
        self.loadClasses()
        self.loadCreatures()
        self.loadNpcs()
        self.loadQuests()
        self.loadRaces()
        self.loadRooms()
        
    def loadAbilities(self):
        from Mods.Abilities import *
        
    def loadClasses(self):
        from Mods.Classes import *
        
    def loadCreatures(self):
        from Mods.Creatures import *
        
    def loadNpcs(self):
        from Mods.Npcs import *
        
    def loadQuests(self):
        from Mods.Quests import *
        
    def loadRaces(self):
        from Mods.Races import *
        
    def loadRooms(self):
        from Mods.Rooms import *
        
    @staticmethod
    def loadAbility(Ability):
        ModLoader.abilities.append(Ability)
        
    @staticmethod
    def loadClass(Class):
        ModLoader.classes.append(Class)
        
    @staticmethod
    def loadCreature(Creature):
        ModLoader.creatures.append(Creature)
        
    @staticmethod
    def loadNpc(Npc):
        ModLoader.npcs.append(Npc)
        
    @staticmethod
    def loadQuest(Quest):
        ModLoader.quests.append(Npc)
        
    @staticmethod
    def loadRace(Race):
        ModLoader.races.append(Race)
        
    @staticmethod
    def loadRoom(Room):
        ModLoader.rooms.append(Room)
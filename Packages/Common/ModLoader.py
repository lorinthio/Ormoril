class ModLoader:

    abilities = {}
    classes = {}
    creatures = {}
    npcs = {}
    quests = {}
    races = {}
    rooms = []
    
    def __init__(self):
        self._loadAbilities()
        self._loadClasses()
        self._loadCreatures()
        self._loadNpcs()
        self._loadQuests()
        self._loadRaces()
        self._loadRooms()
        
    def _loadAbilities(self):
        from Mods.Abilities import *
        
    def _loadClasses(self):
        from Mods.Classes import *
        
    def _loadCreatures(self):
        from Mods.Creatures import *
        
    def _loadNpcs(self):
        from Mods.Npcs import *
        
    def _loadQuests(self):
        from Mods.Quests import *
        
    def _loadRaces(self):
        from Mods.Races import *
        
    def _loadRooms(self):
        from Mods.Rooms import *
        
    @staticmethod
    def loadAbility(Ability):
        ModLoader.abilities.append(Ability)
        
    @staticmethod
    def loadClass(Class):
        ModLoader.classes[Class.name] = Class
        print "Loaded Class : " + Class.name
        
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
        ModLoader.races[Race.name] = Race
        print "Loaded Race : " + Race.name
        
    @staticmethod
    def loadRoom(Room):
        ModLoader.rooms.append(Room)
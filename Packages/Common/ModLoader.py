from collections import OrderedDict

class ModLoader:

    abilities = OrderedDict()
    classes = OrderedDict()
    creatures = OrderedDict()
    npcs = OrderedDict()
    quests = OrderedDict()
    races = OrderedDict()
    rooms = OrderedDict()
    
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
        
    def getAbility(self, name):
        return self.abilities.get(name.lower())

    def getClass(self, name):
        return self.classes.get(name.lower())

    def getCreature(self, name):
        return self.creatures.get(name.lower())

    def getNpc(self, name):
        return self.npcs.get(name.lower())

    def getQuest(self, name):
        return self.quests.get(name.lower())

    def getRace(self, name):
        return self.races.get(name.lower())

    def getRoom(self, name):
        return self.rooms.get(name.lower())
        
    @staticmethod
    def loadAbility(Ability):
        ModLoader.abilities.append(Ability)
        
    @staticmethod
    def loadClass(Class):
        ModLoader.classes[Class.name.lower()] = Class
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
        ModLoader.races[Race.name.lower()] = Race
        print "Loaded Race : " + Race.name
        
    @staticmethod
    def loadRoom(Room):
        ModLoader.rooms.append(Room)
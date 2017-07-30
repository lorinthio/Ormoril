from Tkinter import *
from Common.WindowHelpers import setupGrid
from Common.Utils import PacketTypes
from Common.Objects import Hero
import Common.Serialization as Serialization
import socket

class CharacterCreationWindow(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.ip = "localhost"
        self.port = 8123
        self.PacketSize = 1024
        self.hero = Hero()
        self.pullRacesAndClasses()
        self.setupVariables()
        self.initializeHero()
        self.makeWindow()
        
    def pullRacesAndClasses(self):
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((self.ip, self.port))
            try:
                packet = Serialization.pack(PacketTypes.CREATION_CLASSES, None)
                conn.send(packet)
                data = conn.recv(self.PacketSize)
                if data:
                    data = Serialization.deserialize(data)
                    messageType = data["message"]
                    if(messageType == PacketTypes.CREATION_CLASSES):
                        self.classes = data["data"]
                        
                packet = Serialization.pack(PacketTypes.CREATION_RACES, None)
                conn.send(packet)
                data = conn.recv(self.PacketSize)
                if data:
                    data = Serialization.deserialize(data)
                    messageType = data["message"]
                    if(messageType == PacketTypes.CREATION_RACES):
                        self.races = data["data"]
            except:
                conn.close()
        except:
            pass
        
    def setupVariables(self):
        self.raceVar = StringVar()
        self.raceVar.trace("w", self.raceChanged)
        self.classVar = StringVar()
        self.classVar.trace("w", self.classChanged)
    
    def raceChanged(self, *args):
        newRace = self.races[self.raceVar.get()]
        self.hero.Race = newRace
        self.hero.rebuildStats()
        self.updateGUIVariables()
    
    def classChanged(self, *args):
        newClass = self.classes[self.classVar.get()]
        self.hero.Class = newClass
        self.hero.rebuildStats()
        self.updateGUIVariables()
    
    def updateGUIVariables(self):
        self.strengthVar.set(self.hero.stats["strength"])
        self.constitutionVar.set(self.hero.stats["constitution"])
        self.dexterityVar.set(self.hero.stats["dexterity"])
        self.agiltyVar.set(self.hero.stats["agility"])
        self.intelligenceVar.set(self.hero.stats["intelligence"])
        self.wisdomVar.set(self.hero.stats["wisdom"])        
    
    def initializeHero(self):
        self.strengthVar = IntVar()
        self.constitutionVar = IntVar()
        self.dexterityVar = IntVar()
        self.agiltyVar = IntVar()
        self.wisdomVar = IntVar()
        self.intelligenceVar = IntVar()        
        
        firstRace = self.races.itervalues().next()
        firstClass = self.classes.itervalues().next()
        
        self.hero.Race = firstRace
        self.hero.Class = firstClass
        
        self.raceVar.set(firstRace.name)
        self.classVar.set(firstClass.name)
        
        self.updateGUIVariables()
    
    def makeWindow(self):
        self.master.minsize(500, 400)
        self.master.maxsize(500, 400)
        
        x = 9
        y = 6
        setupGrid(self.master, x, y)
        # Title
        Label(self.master, text="Character Creation", font=("Helvetica", 24)).grid(row=0, column=0, columnspan=x, sticky=N+E+S+W)
        # Description
        #self.description = Label(self.master, text="Hover over something for a description", font=("Helvetica", 10), relief=GROOVE)
        #self.description.grid(row=y-1, column=0, columnspan=x, sticky=W+E+S)        
        #########
        
        # Race
        Label(self.master, text="Race : ", font=("Helvetica", 14)).grid(row=1, column=1, sticky=E)
        OptionMenu(self.master, self.raceVar, *self.races.keys()).grid(row=1, column=2, columnspan=2, sticky=W+E)
        
        # Class
        Label(self.master, text="Class : ", font=("Helvetica", 14)).grid(row=1, column=5, sticky=E)
        OptionMenu(self.master, self.classVar, *self.classes.keys()).grid(row=1, column=6, columnspan=2, sticky=W+E)
        
        # Stats
        strength = Label(self.master, text="STR : ", font=("Helvetica",14))
        strength.grid(row=2, column=2, sticky=E)
        #strength.bind('<ENTER>', self.hoverStrength)
        Label(self.master, textvariable=self.strengthVar, relief=SUNKEN, font=("Helvetica", 12), padx=5).grid(row=2, column=3, sticky=W)
        
        constitution = Label(self.master, text="CON : ", font=("Helvetica",14))
        constitution.grid(row=2, column=5, sticky=E)
        #constitution.bind("ENTER", self.hoverConstitution)
        Label(self.master, textvariable=self.constitutionVar, relief=SUNKEN, font=("Helvetica", 12), padx=5).grid(row=2, column=6, sticky=W)
    
        dexterity = Label(self.master, text="DEX : ", font=("Helvetica",14))
        dexterity.grid(row=3, column=2, sticky=E)
        #dexterity.bind("ENTER", self.hoverDexterity)
        Label(self.master, textvariable=self.dexterityVar, relief=SUNKEN, font=("Helvetica", 12), padx=5).grid(row=3, column=3, sticky=W)
    
        agility = Label(self.master, text="AGI : ", font=("Helvetica",14))
        agility.grid(row=3, column=5, sticky=E)
        #agility.bind("ENTER", self.hoverAgility)
        Label(self.master, textvariable=self.agiltyVar, relief=SUNKEN, font=("Helvetica", 12), padx=5).grid(row=3, column=6, sticky=W)
    
        intelligence = Label(self.master, text="INT : ", font=("Helvetica",14))
        intelligence.grid(row=4, column=2, sticky=E)
        #intelligence.bind("ENTER", self.hoverIntelligence)
        Label(self.master, textvariable=self.intelligenceVar, relief=SUNKEN, font=("Helvetica", 12), padx=5).grid(row=4, column=3, sticky=W)
    
        wisdom = Label(self.master, text="WIS : ", font=("Helvetica",14))
        wisdom.grid(row=4, column=5, sticky=E)
        #wisdom.bind("ENTER", self.hoverWisdom)
        Label(self.master, textvariable=self.wisdomVar, relief=SUNKEN, font=("Helvetica", 12), padx=5).grid(row=4, column=6, sticky=W)        
        
        self.updateGUIVariables()
        
    def hoverStrength(self, event):
        self.description.configure(text = "Strength : A measure of ones physical strength. Increases physical damage and slightly increases max health")
        
    def hoverConstitution(self, event):
        self.description.configure(text = "Constitution : A measure of ones endurance. Increases max health and slightly increases physical defense")
        
    def hoverDexterity(self, event):
        self.description.configure(text = "Dexterity : A measure of ones precision. Increases accuracy and slightly increases critical chance")
        
    def hoverAgility(self, event):
        self.description.configure(text = "Agility : A measure of ones reactions. Increases dodge and slightly increases critical chance")
        
    def hoverWisdom(self, event):
        self.description.configure(text = "Wisdom : A measure of ones knowledge. Increases maximum mana and slightly increases magic defense")
        
    def hoverIntelligence(self, event):
        self.description.configure(text = "Intelligence : A measure of ones magic. Increases magical damage and slightly increases maximum mana")
        
def startCreation():
    CharacterCreationWindow().mainloop()
    
if __name__ == "__main__":
    startCreation()
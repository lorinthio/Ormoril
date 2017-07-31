from Tkinter import *
import Tkconstants as constants
import Tkinter as tk
from Common.WindowHelpers import setupGrid
from Common.Utils import PacketTypes
from Common.Objects import Hero
from collections import OrderedDict
import Common.Serialization as Serialization
import socket

class CharacterCreationWindow(Frame):
    
    def __init__(self, player, master=None):
        Frame.__init__(self, master)
        self.ip = "localhost"
        self.port = 8123
        self.PacketSize = 1024
        self.player = player
        self.pullRacesAndClasses()
        self.setupVariables()
        if self.races and self.classes:
            self.initializeHero()
            self.randomize()
        self.makeWindow()
        
        
    def pullRacesAndClasses(self):
        self.races = OrderedDict({})
        self.classes = OrderedDict({})
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
                        for key, value in data["data"].iteritems():
                            self.classes[key.title()] = value
                        
                packet = Serialization.pack(PacketTypes.CREATION_RACES, None)
                conn.send(packet)
                data = conn.recv(2048)
                if data:
                    data = Serialization.deserialize(data)
                    messageType = data["message"]
                    if(messageType == PacketTypes.CREATION_RACES):
                        for key, value in data["data"].iteritems():
                            self.races[key.title()] = value
            except Exception, e:
                print e.message
                print e
                conn.close()
        except:
            pass
        
    def setupVariables(self):
        self.hero = Hero()
        
        self.strengthVar = IntVar()
        self.constitutionVar = IntVar()
        self.dexterityVar = IntVar()
        self.agiltyVar = IntVar()
        self.wisdomVar = IntVar()
        self.intelligenceVar = IntVar()  
        
        self.strengthCoords = None
        
        self.raceVar = StringVar()
        self.raceVar.trace("w", self.raceChanged)
        self.raceDescriptionVar = StringVar()
        self.classVar = StringVar()
        self.classVar.trace("w", self.classChanged)
        self.classDescriptionVar = StringVar()
    
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
        
        if(self.hero.Race):
            self.raceDescriptionVar.set(self.hero.Race.description)
        if(self.hero.Class):        
            self.classDescriptionVar.set(self.hero.Class.description)
    
    def initializeHero(self):
        firstRace = self.races.itervalues().next()
        firstClass = self.classes.itervalues().next()
        
        self.hero.Race = firstRace
        self.hero.Class = firstClass
        
        self.raceVar.set(firstRace.name)
        self.classVar.set(firstClass.name)
        
        self.updateGUIVariables()
    
    def makeWindow(self):
        width = 500
        height = 400
        self.master.minsize(width, height)
        self.master.maxsize(width, height)
        self.master.iconbitmap(r'icon.ico')
        self.master.title("Character Creation")
        
        # Title
        Label(self.master, text="Character Creation", font=("Helvetica", 24)).place(relx=0.5, y=20, anchor=CENTER)
        # Description
        self.description = Label(self.master, text="Hover over something for a description", font=("Helvetica", 10), wraplength=400, relief=GROOVE)
        self.description.place(relx=0.5, y=360, height=40, width=width, anchor=N)        
        #########
        
        # Race
        if self.races:
            Label(self.master, text="Race : ", font=("Helvetica", 14)).place(x=100, y=70, anchor=E)
            OptionMenu(self.master, self.raceVar, *self.races.keys()).place(x=100, y=70, width=120, anchor=W)
            
            Label(self.master, textvariable=self.raceDescriptionVar, font=("Helvetica", 12), wraplength=200, relief=SUNKEN).place(x=120, y=90, width=200, height=100, anchor=N)
        
        # Class
        if self.classes:
            Label(self.master, text="Class : ", font=("Helvetica", 14)).place(x=344, y=70, anchor=E)
            OptionMenu(self.master, self.classVar, *self.classes.keys()).place(x=344, y=70, width=120, anchor=W)
            
            Label(self.master, textvariable=self.classDescriptionVar, font=("Helvetica", 12), wraplength=200, relief=SUNKEN).place(x=380, y=90, width=200, height=100, anchor=N)
            
        
        # Stats
        strength = Label(self.master, text="STR : ", font=("Helvetica",14))
        strength.place(x=175, y=220, anchor=E)
        strength.bind("<Enter>", self.hoverStrength)
        Label(self.master, textvariable=self.strengthVar, relief=SUNKEN, font=("Helvetica", 12), padx=5).place(x=175, y=220, width=30, anchor=W)
        
        constitution = Label(self.master, text="CON : ", font=("Helvetica",14))
        constitution.place(x=350, y=220, anchor=E)
        constitution.bind("<Enter>", self.hoverConstitution)
        Label(self.master, textvariable=self.constitutionVar, relief=SUNKEN, font=("Helvetica", 12), padx=5).place(x=350, y=220, width=30, anchor=W)
    
        dexterity = Label(self.master, text="DEX : ", font=("Helvetica",14))
        dexterity.place(x=175, y=250, anchor=E)
        dexterity.bind("<Enter>", self.hoverDexterity)
        Label(self.master, textvariable=self.dexterityVar, relief=SUNKEN, font=("Helvetica", 12), padx=5).place(x=175, y=250, width=30, anchor=W)
    
        agility = Label(self.master, text="AGI : ", font=("Helvetica",14))
        agility.place(x=350, y=250, anchor=E)
        agility.bind("<Enter>", self.hoverAgility)
        Label(self.master, textvariable=self.agiltyVar, relief=SUNKEN, font=("Helvetica", 12), padx=5).place(x=350, y=250, width=30, anchor=W)
    
        intelligence = Label(self.master, text="INT : ", font=("Helvetica",14))
        intelligence.place(x=175, y=280, anchor=E)
        intelligence.bind("<Enter>", self.hoverIntelligence)
        Label(self.master, textvariable=self.intelligenceVar, relief=SUNKEN, font=("Helvetica", 12), padx=5).place(x=175, y=280, width=30, anchor=W)
    
        wisdom = Label(self.master, text="WIS : ", font=("Helvetica",14))
        wisdom.place(x=350, y=280, anchor=E)
        wisdom.bind("<Enter>", self.hoverWisdom)
        Label(self.master, textvariable=self.wisdomVar, relief=SUNKEN, font=("Helvetica", 12), padx=5).place(x=350, y=280, width=30, anchor=W)       
        
        Button(self.master, text="Roll", command=self.randomize).place(x=100, y=320, width=80, height=30, anchor=NE)
        Button(self.master, text="Finish", command=self.finish).place(x=width-100, y=320, width=80, height=30, anchor=NW)
        
        self.updateGUIVariables()
        
    def enter(self, event):
        print "Entered" + str(event)
        
    def randomize(self):
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((self.ip, self.port))
            try:
                packet = Serialization.pack(PacketTypes.CREATION_RANDOMIZE, None)
                conn.send(packet)
                data = conn.recv(self.PacketSize)
                if data:
                    data = Serialization.deserialize(data)
                    messageType = data["message"]
                    if(messageType == PacketTypes.CREATION_RANDOMIZE):
                        stats = data["data"]
                        self.hero.strength = stats[0]
                        self.hero.constitution = stats[1]
                        self.hero.dexterity = stats[2]
                        self.hero.agility = stats[3]
                        self.hero.intelligence = stats[4]
                        self.hero.wisdom = stats[5]
                        self.hero.rebuildStats()
                        self.updateGUIVariables()
            except:
                conn.close()
        except:
            pass        
        
    def finish(self):
        self.player.hero = self.hero
        return
        
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
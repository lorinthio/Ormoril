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
        
        self.strAdded = 0
        self.conAdded = 0
        self.dexAdded = 0
        self.agiAdded = 0
        self.intAdded = 0
        self.wisAdded = 0
        
        self.strengthVar = IntVar()
        self.constitutionVar = IntVar()
        self.dexterityVar = IntVar()
        self.agiltyVar = IntVar()
        self.wisdomVar = IntVar()
        self.intelligenceVar = IntVar()  
        
        self.allocationVar = StringVar()
        self.pointsRemaining = 6
        
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
        
        self.allocationVar.set("Points Remaining ( {} )".format(self.pointsRemaining))
        
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
        
        backgroundColor = "Azure2"
        self.plusminus = PhotoImage(file="plusminus.gif")
        
        Label(self.master, bg=backgroundColor).place(x=0, y=0, relwidth=1,relheight=1)
        
        # Title
        Label(self.master, text="Character Creation", font=("Helvetica", 24), bg=backgroundColor).place(relx=0.5, y=20, anchor=CENTER)
        # Description
        self.description = Label(self.master, text="Hover over something for a description", font=("Helvetica", 10), wraplength=400, relief=GROOVE, bg=backgroundColor)
        self.description.place(relx=0.5, y=360, height=40, width=width, anchor=N)
        #########
        
        # Race
        if self.races:
            Label(self.master, text="Race : ", font=("Helvetica", 14), bg=backgroundColor).place(x=100, y=70, anchor=E)
            OptionMenu(self.master, self.raceVar, *self.races.keys()).place(x=100, y=70, width=120, anchor=W)
            
            Label(self.master, textvariable=self.raceDescriptionVar, font=("Helvetica", 12), wraplength=200, relief=SUNKEN, bg=backgroundColor).place(x=120, y=90, width=200, height=100, anchor=N)
        
        # Class
        if self.classes:
            Label(self.master, text="Class : ", font=("Helvetica", 14), bg=backgroundColor).place(x=344, y=70, anchor=E)
            OptionMenu(self.master, self.classVar, *self.classes.keys()).place(x=344, y=70, width=120, anchor=W)
            
            Label(self.master, textvariable=self.classDescriptionVar, font=("Helvetica", 12), wraplength=200, relief=SUNKEN, bg=backgroundColor).place(x=380, y=90, width=200, height=100, anchor=N)
            
        
        # Stats
        strength = Label(self.master, text="STR : ", font=("Helvetica",14), bg=backgroundColor)
        strength.place(x=150, y=220, anchor=E)
        strength.bind("<Enter>", self.hoverStrength)
        Label(self.master, textvariable=self.strengthVar, relief=SUNKEN, font=("Helvetica", 12), padx=5, bg=backgroundColor).place(x=150, y=220, width=30, anchor=W)
        label = Label(self.master, image=self.plusminus)
        label.place(x=200, y=220, width=28, height=28, anchor=CENTER)
        label.bind("<Button-1>", lambda event, var=self.strengthVar, name="strength": self.leftclick(event, var, name))
        label.bind("<Button-3>", lambda event, var=self.strengthVar, name="strength": self.rightclick(event, var, name))
        label.bind("<Enter>", self.hoverPlusMinus)
        
        constitution = Label(self.master, text="CON : ", font=("Helvetica",14), bg=backgroundColor)
        constitution.place(x=350, y=220, anchor=E)
        constitution.bind("<Enter>", self.hoverConstitution)
        Label(self.master, textvariable=self.constitutionVar, relief=SUNKEN, font=("Helvetica", 12), padx=5, bg=backgroundColor).place(x=350, y=220, width=30, anchor=W)
        label = Label(self.master, image=self.plusminus)
        label.place(x=400, y=220, width=28, height=28, anchor=CENTER)
        label.bind("<Button-1>", lambda event, var=self.constitutionVar, name="constitution": self.leftclick(event, var, name))
        label.bind("<Button-3>", lambda event, var=self.constitutionVar, name="constitution": self.rightclick(event, var, name))
        label.bind("<Enter>", self.hoverPlusMinus)
    
        dexterity = Label(self.master, text="DEX : ", font=("Helvetica",14), bg=backgroundColor)
        dexterity.place(x=150, y=250, anchor=E)
        dexterity.bind("<Enter>", self.hoverDexterity)
        Label(self.master, textvariable=self.dexterityVar, relief=SUNKEN, font=("Helvetica", 12), padx=5, bg=backgroundColor).place(x=150, y=250, width=30, anchor=W)
        label = Label(self.master, image=self.plusminus)
        label.place(x=200, y=250, width=28, height=28, anchor=CENTER)
        label.bind("<Button-1>", lambda event, var=self.dexterityVar, name="dexterity": self.leftclick(event, var, name))
        label.bind("<Button-3>", lambda event, var=self.dexterityVar, name="dexterity": self.rightclick(event, var, name))
        label.bind("<Enter>", self.hoverPlusMinus)
    
        agility = Label(self.master, text="AGI : ", font=("Helvetica",14), bg=backgroundColor)
        agility.place(x=350, y=250, anchor=E)
        agility.bind("<Enter>", self.hoverAgility)
        Label(self.master, textvariable=self.agiltyVar, relief=SUNKEN, font=("Helvetica", 12), padx=5, bg=backgroundColor).place(x=350, y=250, width=30, anchor=W)
        label = Label(self.master, image=self.plusminus)
        label.place(x=400, y=250, width=28, height=28, anchor=CENTER)
        label.bind("<Button-1>", lambda event, var=self.agiltyVar, name="agility": self.leftclick(event, var, name))
        label.bind("<Button-3>", lambda event, var=self.agiltyVar, name="agility": self.rightclick(event, var, name))
        label.bind("<Enter>", self.hoverPlusMinus)
    
        intelligence = Label(self.master, text="INT : ", font=("Helvetica",14), bg=backgroundColor)
        intelligence.place(x=150, y=280, anchor=E)
        intelligence.bind("<Enter>", self.hoverIntelligence)
        Label(self.master, textvariable=self.intelligenceVar, relief=SUNKEN, font=("Helvetica", 12), padx=5, bg=backgroundColor).place(x=150, y=280, width=30, anchor=W)
        label = Label(self.master, image=self.plusminus)
        label.place(x=200, y=280, width=28, height=28, anchor=CENTER)
        label.bind("<Button-1>", lambda event, var=self.intelligenceVar, name="intelligence": self.leftclick(event, var, name))
        label.bind("<Button-3>", lambda event, var=self.intelligenceVar, name="intelligence": self.rightclick(event, var, name))
        label.bind("<Enter>", self.hoverPlusMinus)
    
        wisdom = Label(self.master, text="WIS : ", font=("Helvetica",14), bg=backgroundColor)
        wisdom.place(x=350, y=280, anchor=E)
        wisdom.bind("<Enter>", self.hoverWisdom)
        Label(self.master, textvariable=self.wisdomVar, relief=SUNKEN, font=("Helvetica", 12), padx=5, bg=backgroundColor).place(x=350, y=280, width=30, anchor=W)   
        label = Label(self.master, image=self.plusminus)
        label.place(x=400, y=280, width=28, height=28, anchor=CENTER)    
        label.bind("<Button-1>", lambda event, var=self.wisdomVar, name="wisdom": self.leftclick(event, var, name))
        label.bind("<Button-3>", lambda event, var=self.wisdomVar, name="wisdom": self.rightclick(event, var, name))
        label.bind("<Enter>", self.hoverPlusMinus)
        
        Label(self.master, textvariable=self.allocationVar, font=("Helvetica", 12), padx=5, bg=backgroundColor).place(relx=0.5, y=320, anchor=CENTER)
        
        Button(self.master, text="Roll", command=self.randomize).place(x=100, y=320, width=80, height=30, anchor=NE)
        Button(self.master, text="Finish", command=self.finish).place(x=width-100, y=320, width=80, height=30, anchor=NW)
        
        self.updateGUIVariables()
        
    def leftclick(self, event, var, name):
        augment = self.pointsRemaining > 0
        
        if augment:
            var.set(var.get() + 1)
            self.pointsRemaining -= 1
            self.allocationVar.set("Points Remaining ( {} )".format(self.pointsRemaining))
            
            if(name == "strength"):
                self.strAdded += 1
            if(name == "constitution"):
                self.conAdded += 1
            if(name == "dexterity"):
                self.dexAdded += 1
            if(name == "agility"):
                self.agiAdded += 1
            if(name == "intelligence"):
                self.intAdded += 1
            if(name == "wisdom"):
                self.wisAdded += 1
            
    def rightclick(self, event, var, name):
        augment = False
        if(name == "strength"):
            augment = var.get() > self.hero.stats["strength"]
        if(name == "constitution"):
            augment = var.get() > self.hero.stats["constitution"]
        if(name == "dexterity"):
            augment = var.get() > self.hero.stats["dexterity"]
        if(name == "agility"):
            augment = var.get() > self.hero.stats["agility"]
        if(name == "intelligence"):
            augment = var.get() > self.hero.stats["intelligence"]
        if(name == "wisdom"):
            augment = var.get() > self.hero.stats["wisdom"]
        
        if augment:
            var.set(var.get()-1)
            self.pointsRemaining += 1
            self.allocationVar.set("Points Remaining ( {} )".format(self.pointsRemaining))
        
    def enter(self, event):
        print "Entered" + str(event)
        
    def randomize(self):
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((self.ip, self.port))
            try:
                packet = Serialization.pack(PacketTypes.CREATION_RANDOMIZE, { "username": self.player.username })
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
                        
                        self.strAdded = 0
                        self.conAdded = 0
                        self.dexAdded = 0
                        self.agiAdded = 0
                        self.intAdded = 0
                        self.wisAdded = 0
                        
                        self.pointsRemaining = 6
                        self.allocationVar.set("Points Remaining ( {} )".format(self.pointsRemaining))
                        self.hero.rebuildStats()
                        self.updateGUIVariables()
            except:
                conn.close()
        except:
            pass        
        
    def finish(self):
        self.player.hero = self.hero
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((self.ip, self.port))
            try:
                self.hero.strength += self.strAdded
                self.hero.constitution += self.conAdded
                self.hero.dexterity += self.dexAdded
                self.hero.agility += self.agiAdded
                self.hero.intelligence += self.intAdded
                self.hero.wisdom += self.wisAdded
                
                packet = Serialization.pack(PacketTypes.CREATION_FINAL, { "username": self.player.username, "hero": self.player.hero})
                conn.send(packet)
                data = conn.recv(self.PacketSize)
                if data:
                    data = Serialization.deserialize(data)
                    messageType = data["message"]
                    if(messageType == PacketTypes.CREATION_SUCCESS):
                        print "Creation Complete!"
                    if(messageType == PacketTypes.CREATION_INVALID):
                        print "Creation INVALID!"
            except Exception, e:
                print e
                print e.message
                conn.close()
        except:
            pass
        
    def hoverPlusMinus(self, event):
        self.description.configure(text = "Point Allocation : Use LEFT-CLICK to ADD points and RIGHT-CLICK to REMOVE the points you've added")
        
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
from Tkinter import *
from Common.WindowHelpers import setupGrid

class CharacterCreationWindow(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.setupVariables()
        self.makeWindow()
        
    def setupVariables(self):
        self.setupRaces()
        return
    
    def setupRaces(self):
        self.races = {"Human", "Elf", "Dwarf", "Planetouched", "Blackblood"}
        self.classes = { "Warrior", "Rogue", "Magician" }
        self.raceVar = StringVar()
        self.raceVar.set("Human")
        self.classVar = StringVar()
        self.classVar.set("Warrior")
    
    def makeWindow(self):
        self.master.minsize(500, 500)
        self.master.maxsize(500, 500)
        
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
        OptionMenu(self.master, self.raceVar, *self.races).grid(row=1, column=2, columnspan=2, sticky=W)
        
        # Class
        Label(self.master, text="Class : ", font=("Helvetica", 14)).grid(row=1, column=5, sticky=E)
        OptionMenu(self.master, self.classVar, *self.classes).grid(row=1, column=6, columnspan=2, sticky=W)
        
        # Stats
        strength = Label(self.master, text="STR : ", font=("Helvetica",14))
        strength.grid(row=2, column=2, sticky=E)
        #strength.bind('<ENTER>', self.hoverStrength)
        Label(self.master, text="10", relief=SUNKEN, font=("Helvetica", 12)).grid(row=2, column=3, sticky=W)
        
        constitution = Label(self.master, text="CON : ", font=("Helvetica",14))
        constitution.grid(row=2, column=5, sticky=E)
        #constitution.bind("ENTER", self.hoverConstitution)
        Label(self.master, text="10", relief=SUNKEN, font=("Helvetica", 12)).grid(row=2, column=6, sticky=W)
    
        dexterity = Label(self.master, text="DEX : ", font=("Helvetica",14))
        dexterity.grid(row=3, column=2, sticky=E)
        #dexterity.bind("ENTER", self.hoverDexterity)
        Label(self.master, text="10", relief=SUNKEN, font=("Helvetica", 12)).grid(row=3, column=3, sticky=W)
    
        agility = Label(self.master, text="AGI : ", font=("Helvetica",14))
        agility.grid(row=3, column=5, sticky=E)
        #agility.bind("ENTER", self.hoverAgility)
        Label(self.master, text="10", relief=SUNKEN, font=("Helvetica", 12)).grid(row=3, column=6, sticky=W)
    
        intelligence = Label(self.master, text="INT : ", font=("Helvetica",14))
        intelligence.grid(row=4, column=2, sticky=E)
        #intelligence.bind("ENTER", self.hoverIntelligence)
        Label(self.master, text="10", relief=SUNKEN, font=("Helvetica", 12)).grid(row=4, column=3, sticky=W)
    
        wisdom = Label(self.master, text="WIS : ", font=("Helvetica",14))
        wisdom.grid(row=4, column=5, sticky=E)
        #wisdom.bind("ENTER", self.hoverWisdom)
        Label(self.master, text="10", relief=SUNKEN, font=("Helvetica", 12)).grid(row=4, column=6, sticky=W)        
        
        
        
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
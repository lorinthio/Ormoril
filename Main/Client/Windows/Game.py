from Tkinter import *
from ttk import Progressbar, Style
from Common.WindowHelpers import setupGrid
from Common.Objects import Player, Hero
import Common.Serialization as Serialization

class GameWindow(Frame):
    
    def __init__(self, player, master=None):
        self.player = player
        Frame.__init__(self, master)
        setupGrid(self.master, 7, 6)
        self.characterFrame = CharacterFrame(self.master)
        self.setupVariables()
        self.setupWindow()
        self.setupChatFrame()
        self.entryBar()
        self.setupKeyBindings()

    def setupVariables(self):
        self.entryVar = StringVar()
        self.chatText = None

    def setupWindow(self):
        self.master.title("Text Based Adventure")
        self.master.maxsize(1366, 968)
        self.master.minsize(900,600)
        self.master.iconbitmap(r'icon.ico')
        self.master["bg"] = "white"
        
    def setupChatFrame(self):
        chatText = Text(self.master, wrap=WORD, state=DISABLED)
        chatText.grid(row=0, column=3, rowspan=6, columnspan=4, sticky=W+E+S+N)
        scrollbar = Scrollbar(self.master, command=chatText.yview)
        chatText['yscrollcommand'] = scrollbar.set
        self.chatText = chatText
        
    def setupKeyBindings(self):
        self.master.bind('<Return>', 
                    lambda event:
                         enterChatVar(self.chatText, self.entryVar))
        
    def entryBar(self):
        Entry(self.master, textvariable=self.entryVar).grid(row=5, column=3, rowspan=1, columnspan=4, sticky=W+E+S)

class CharacterFrame(Frame):
    
    def __init__(self, master):
        self.setupVariables()
        frame = Frame(master)
        frame.grid(row=0, column=0, rowspan=6, columnspan=3, sticky=W+E+S+N)
    
        Label(frame, text="Character", font=("Helvetica", 16)).grid(row=0, column=0, sticky=W)
        
        #Health
        health = Label(frame, text="Health", font=("Helvetica", 12))
        health.grid(row=1, column=0, sticky=W)
        self.widgets["healthText"] = health
        can = Canvas(frame, width=200, height=14)
        can.grid(row=2, column=0, sticky=W+E)
        self.widgets["healthCanvas"] = can
        self.widgets["healthBar"] = can.create_rectangle(0, 0, 200, 14, fill="green")
        
        #Mana
        mana = Label(frame, text="Mana", font=("Helvetica", 12))
        mana.grid(row=3, column=0, sticky=W)
        self.widgets["manaText"] = mana
        can = Canvas(frame, width=200, height=14)
        can.grid(row=4, column=0, sticky=W+E)
        self.widgets["manaCanvas"] = can
        self.widgets["manaBar"] = can.create_rectangle(0, 0, 200, 14, fill="blue")
        
    def changeVital(self, vital, curValue, maxValue):
        vitalTitle = vital.title()
        self.widgets[vital + "Text"].configure(text = vitalTitle + " : " + str(curValue) + " / " + str(maxValue))
        fraction = (1.0 * curValue) / (1.0* maxValue)
        self.widgets[vital + "Canvas"].coords(self.widgets[vital + "Bar"], 0, 0, 200 * fraction, 14)
        
    def setupVariables(self):
        self.hero = Hero()
        self.widgets = {}
        
    def handleCharacterPacket(self, packet):
        return
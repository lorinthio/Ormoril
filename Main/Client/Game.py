from Tkinter import *
from ttk import Progressbar, Style
from Commands import enterChatVar
from Common.WindowHelpers import setupGrid
from Objects import Player, Hero
from Client import ClientConnection
import Common.Serialization as Serialization

class GameWindow(Frame):
    
    def __init__(self, player, master=None):
        self.player = player
        Frame.__init__(self, master)
        setupGrid(self.master, 7, 6)
        self.setupVariables()
        self.connect()
        self.setupWindow()
        self.setupChatFrame()
        self.characterFrame = CharacterFrame(self.master, self.client)
        self.entryBar()
        self.setupKeyBindings()

    def setupVariables(self):
        self.entryVar = StringVar()
        self.chatText = None

    def setupWindow(self):
        self.master.title("Text Based Adventure")
        self.master.maxsize(1366, 968)
        self.master.minsize(900,600)
        self.master["bg"] = "white"
        
    def setupChatFrame(self):
        chatText = Text(self.master, wrap=WORD)
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
        
    def connect(self):
        self.client = ClientConnection()
        self.client.connect()
        self.master.protocol("WM_DELETE_WINDOW", self.disconnect)
        
    def disconnect(self):
        self.client.disconnect()
        self.master.destroy()

class CharacterFrame(Frame):
    
    def __init__(self, master, client):
        self.setupVariables()
        frame = Frame(master)
        frame.grid(row=0, column=0, rowspan=6, columnspan=3, sticky=W+E+S+N)
    
        Label(frame, text="Character", font=("Helvetica", 16)).grid(row=0, column=0, sticky=W)
        
        Label(frame, text="Health", font=("Helvetica", 12)).grid(row=1, column=0, sticky=W)
        can = Canvas(frame, width=200, height=14)
        can.grid(row=2, column=0, sticky=W+E)
        can.create_rectangle(0, 0, 200, 14, fill="green")
        Label(frame, text="Mana", font=("Helvetica", 12)).grid(row=3, column=0, sticky=W)
        can = Canvas(frame, width=200, height=14)
        can.grid(row=4, column=0, sticky=W+E)
        rect = can.create_rectangle(0, 0, 200, 14, fill="blue")
        
        can.coords(rect, 0,0,100,14)
        
    def setupVariables(self):
        self.hero = Hero()
        
    def handleCharacterPacket(self, packet):
        return

def start(player):
    win = GameWindow(player)
    win.mainloop()
    
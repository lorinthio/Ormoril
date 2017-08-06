from Tkinter import *
from Ormoril.UiUtils import enterChatVar
from Ormoril.WindowHelpers import setupGrid, centerWindow, makeNotification
from Ormoril.Utils import PacketTypes
from Ormoril.Objects import Player
from Application.Client import ClientConnection
import cPickle as pickle
import socket
import Ormoril.Serialization as Serialization

class LoginWindow(Frame):
    
    def __init__(self, player, master=None):
        Frame.__init__(self, master)
        self.player = player
        self.setupVariables()
        self.createLoginWindow()
        self.packetHandler = LoginPacketHandler(self)
        ClientConnection.setActivePacketHandler(self.packetHandler)
        
    def setupVariables(self):
        self.username = StringVar()
        self.password = StringVar()
        self.email = StringVar()
        self.activeFrame = None
        self.PacketSize = 1024
        
    def createLoginWindow(self):
        if self.activeFrame:
            self.activeFrame.destroy()
        width = 250
        height = 110
        
        frame = Frame(self.master)
        setupGrid(self.master, 2, 4)
        frame.grid(row=1, column=0, rowspan=3, columnspan=2)
        self.activeFrame = frame
        setupGrid(frame, 2, 4)
        self.master.title("Login")
        self.master.minsize(width, height)
        self.master.maxsize(width, height)
        
        playerCount = self.getPlayerCount()
        serverOnline = playerCount != None
        Label(frame, text="Server Status : ".format(playerCount)).grid(row=0, column=0, sticky=E)
        if serverOnline:
            Label(frame, text="Online", foreground="forest green").grid(row=0, column=1, sticky=W)
        else:
            Label(frame, text="Offline", foreground="red").grid(row=0, column=1, sticky=W)
        
        Label(frame, text="Players Online : ").grid(row=1, column=0, sticky=E)
        Label(frame, text="{}".format(playerCount)).grid(row=1, column=1, sticky=W)
        Label(frame, text="Username : ").grid(row=2, column=0, sticky=E)
        Label(frame, text="Password : ").grid(row=3, column=0, sticky=E)
        Entry(frame, textvariable=self.username).grid(row=2, column=1, sticky=W)
        Entry(frame, textvariable=self.password, show="*").grid(row=3, column=1, sticky=W)
        Button(frame, command=self.attemptLogin, text="Login").grid(row=4, column=0)
        Button(frame, command=self.createAccountCreationWindow, text="Register").grid(row=4, column=1)
        centerWindow(self.master, width, height)
        self.master.iconbitmap(r'Images/icon.ico')
        
    def createAccountCreationWindow(self):
        if self.activeFrame:
            self.activeFrame.destroy()
        width = 250
        height = 90
        
        frame = Frame(self.master)
        self.master.iconbitmap(r'Images/icon.ico')
        setupGrid(self.master, 2, 4)
        frame.grid(row=0, column=0, rowspan=4, columnspan=2)
        self.activeFrame = frame
        
        self.master.title("Register")
        Label(frame, text="Email : ").grid(row=0, column=0, sticky=E)
        Label(frame, text="Username : ").grid(row=1, column=0, sticky=E)
        Label(frame, text="Password : ").grid(row=2, column=0, sticky=E)
        Entry(frame, textvariable=self.email).grid(row=0, column=1, sticky=W)
        Entry(frame, textvariable=self.username).grid(row=1, column=1, sticky=W)
        Entry(frame, textvariable=self.password, show="*").grid(row=2, column=1, sticky=W)
        Button(frame, command=self.attemptCreate, text="Create").grid(row=3, column=0)
        Button(frame, command=self.createLoginWindow, text="Cancel").grid(row=3, column=1) 
        centerWindow(self.master, width, height)       
        
        
    def attemptLogin(self):
        try:
            packet = ClientConnection.sendAndWait(PacketTypes.LOGIN, {"username": self.username.get().lower(), "password": self.password.get()})
            if packet:
                self.packetHandler.handlePacket(packet)
        except:
            self.failedConnection()        
      
    def getPlayerCount(self):
        try:
            data = ClientConnection.sendAndWait(PacketTypes.PLAYER_COUNT, None)
            if data:
                messageType = data["message"]
                if(messageType == PacketTypes.PLAYER_COUNT):
                    return data["data"]["count"]
        except:
            pass
      
    def updatePlayer(self):
        self.player.username = self.username.get()
        self.player.password = self.password.get()
        self.player.isLoggedIn = True
      
    def attemptCreate(self):
        try:
            packet = ClientConnection.sendAndWait(PacketTypes.ACCOUNT_CREATE, {"username": self.username.get().lower(), "password": self.password.get(), "email": self.email.get()})
            if packet:
                self.packetHandler.handlePacket(packet)
        except:
            self.failedConnection()
            
    def showError(self, message):
        top = makeNotification("Error!")
        Message(top, text=message, width=250).pack()
        Button(top, text="Close", command=top.destroy).pack() 
        
    def showAccountCreateSuccess(self):
        top = makeNotification("Account Creation Success!")
        Message(top, text="Your account was created successfully!", width=250).pack()
        Button(top, text="Close", command=top.destroy).pack()
        
        self.createLoginWindow()
        
    def showLoginSuccess(self):
        top = makeNotification("Login Success!")
        Message(top, text="You have successfully logged in!", width=250).pack()
        Button(top, text="Close", command=top.destroy).pack()
        
    def showLoginFailure(self):
        top = makeNotification("Login Failure!")
        Message(top, text="Invalid username/password", width=250).pack()
        Button(top, text="Close", command=top.destroy).pack()
                
    def failedConnection(self):
        top = makeNotification("Connection Failed!")
        Message(top, text="There was no response from the server", width=250).pack()
        Button(top, text="Close", command=top.destroy).pack()    
        
    def close(self):
        self.master.destroy()

class LoginPacketHandler:
    
    def __init__(self, loginWindow):
        self.loginWindow = loginWindow
        
    def handlePacket(self, packet):
        message = packet["message"]
        data = packet["data"]
        
        self.handleLoginAttempt(message, data)
        self.handleLoginResult(message, data)
        self.handleAccountCreation(message, data)
            
    def handleLoginAttempt(self, message, data):
        if message == PacketTypes.LOGIN_ATTEMPT_RESPONSE:
            success = data["success"]
            if success:
                ClientConnection.connected = True
            else:
                ClientConnection.connected = False
                
    def handleLoginResult(self, messageType, data):
        if(messageType == PacketTypes.LOGIN_SUCCESS):
            self.loginWindow.showLoginSuccess()
            self.loginWindow.updatePlayer()
            self.loginWindow.close()
        elif(messageType == PacketTypes.LOGIN_FAILURE):
            self.loginWindow.showLoginFailure()
            
    def handleAccountCreation(self, messageType, data):
        if(messageType == PacketTypes.ACCOUNT_CREATE_FAILURE_ACCOUNT_EXISTS):
            self.loginWindow.showError("Account exists with your username or email!")
        elif(messageType == PacketTypes.ACCOUNT_CREATE_FAILURE_EMAIL_EXISTS):
            self.loginWindow.showError("Account exists with that email!")
        elif(messageType == PacketTypes.ACCOUNT_CREATE_FAILURE_USERNAME_EXISTS):
            self.loginWindow.showError("Account exists with that username!")
        elif(messageType == PacketTypes.ACCOUNT_CREATE_FAILURE_INVALID_PASSWORD):
            self.loginWindow.showError("Your password must contain a number!")
        elif(messageType == PacketTypes.ACCOUNT_CREATE_FAILURE_INVALID_USERNAME):
            self.loginWindow.showError("Your username must be 7-20 characters long!")
        elif(messageType == PacketTypes.ACCOUNT_CREATE_FAILURE_INVALID_EMAIL):
            self.loginWindow.showError("Please enter a valid email!")
        elif(messageType == PacketTypes.ACCOUNT_CREATE_SUCCESS):
            self.loginWindow.showAccountCreateSuccess()        

def login(player):
    win = LoginWindow(player)
    win.mainloop()
    
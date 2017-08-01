# Import from other libraries
from Common.Objects import Player
from Windows.Login import login
from Windows.Game import GameWindow
from Windows.CharacterCreation import CharacterCreationWindow
from Client import ClientConnection

class Application:
     
     def __init__(self):
          self.player = Player()
          
     def start(self):
          login(self.player)
          client = ClientConnection(self.player)
          
          if self.player.needToCreate:
               self.loadWindow(CharacterCreationWindow(self.player))
          if self.player.isLoggedIn and self.player.hero:
               self.loadWindow(GameWindow(self.player))

     def loadWindow(self, window):
          ClientConnection.setActiveWindow(window.master)
          window.master.protocol("WM_DELETE_WINDOW", self.disconnect)
          window.mainloop()

     def disconnect(self):
          ClientConnection.disconnect()

if __name__ == "__main__":
     Application().start()
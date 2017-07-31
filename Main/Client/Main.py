# Import from other libraries
from Common.Objects import Player
from Windows.Login import login
from Windows.Game import GameWindow
from Windows.CharacterCreation import CharacterCreationWindow
from Client import ClientConnection

if __name__ == "__main__":
     player = Player()
     login(player)
     client = ClientConnection(player)
     if player.needToCreate:
          win = CharacterCreationWindow(player)
          ClientConnection.setActiveWindow(win.master)
          win.mainloop()
     if player.isLoggedIn and player.hero:
          win = GameWindow(player)
          ClientConnection.setActiveWindow(win.master)
          win.mainloop()
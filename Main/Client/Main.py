# Import from other libraries
from Objects import Player
from Login import login
from Game import start

if __name__ == "__main__":
     player = Player()
     login(player)
     if player.isLoggedIn:
          start(player)
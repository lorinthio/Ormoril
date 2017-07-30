from Common.Objects import Race
from Common.ModLoader import ModLoader

black = Race(name="Blackblood", strength=-1, constitution=-2, agility=2, wisdom=-1, intelligence=2)
ModLoader.loadRace(black)
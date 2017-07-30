from Common.Objects import Race
from Common.ModLoader import ModLoader

halforc = Race(name="Half-Orc", strength = 3, constitution = 2, agility = -2, dexterity=-1, wisdom = -1, intelligence = -1)
ModLoader.loadRace(halforc)
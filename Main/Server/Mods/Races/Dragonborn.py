from Common.Objects import Race
from Common.ModLoader import ModLoader

dragon = Race(name="Dragonborn", strength=2, constitution=1, agility=-3, dexterity=-2, intelligence=2)
ModLoader.loadRace(dragon)
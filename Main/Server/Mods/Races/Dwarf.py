from Common.Objects import Race
from Common.ModLoader import ModLoader

dwarf = Race(name="Dwarf", description="These stout beings are hearty folk who enjoy a strong drink over anything else", strength = 2, constitution = 2, agility = -2, wisdom = -1, intelligence = -1)
ModLoader.loadRace(dwarf)
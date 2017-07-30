from Common.Objects import Race
from Common.ModLoader import ModLoader

plane = Race(name="Planetouched", strength=-1, constitution=2, agility=-1, wisdom=1, intelligence=-1)
ModLoader.loadRace(plane)
from Common.Objects import Race
from Common.ModLoader import ModLoader

plane = Race(name="Planetouched", description="Not too different in appearance from humans, these creatures have been blessed by god and walk the world to spread their good will", strength=-1, constitution=2, agility=-1, wisdom=1, intelligence=-1)
ModLoader.loadRace(plane)
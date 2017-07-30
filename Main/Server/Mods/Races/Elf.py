from Common.Objects import Race
from Common.ModLoader import ModLoader

elf = Race(name="Elf", dexterity=2, wisdom=2, strength=-1, intelligence=-2, constitution=-1)
ModLoader.loadRace(elf)
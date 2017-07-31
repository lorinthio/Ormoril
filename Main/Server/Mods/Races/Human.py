from Common.Objects import Race
from Common.ModLoader import ModLoader

human = Race(name="Human", description="A race of humanoids that are of diverse appearances and relatively average ability")
ModLoader.loadRace(human)
from Common.Objects import Race
from Common.ModLoader import ModLoader

black = Race(name="Blackblood", description="A dark skinned and dark blooded creature who is focused more on deadly arts than the safety of others", strength=-1, constitution=-2, agility=2, wisdom=-1, intelligence=2)
ModLoader.loadRace(black)
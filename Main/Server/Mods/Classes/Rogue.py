from Common.Objects import Class
from Common.ModLoader import ModLoader

rogue = Class(name="Rogue", description="A scrappy thief who focuses more on deception rather than brute force")
ModLoader.loadClass(rogue)
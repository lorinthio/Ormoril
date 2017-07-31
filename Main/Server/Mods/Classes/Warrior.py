from Common.Objects import Class
from Common.ModLoader import ModLoader

warrior = Class(name="Warrior", description="A tough fighter who focuses on defending his friends and bashing in skulls!")
ModLoader.loadClass(warrior)
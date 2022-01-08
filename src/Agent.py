import random

from src.Node import Node
from src.Pokemon import Pokemon


class Agent(Node):
    def __init__(self, id: int,pos:tuple, value: float, src: int, dest: int, speed: float):
        super().__init__(id, pos)
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.list = []
        self.onduty = False
        self.pokemon = []
        self.name = self.generateName()
        self.path = self.getPath()

    def generateName(self):
        names = ("Ash", "Brock", "Dawn", "Helio")
        return random.choice(names)

    def getPath(self):
        path = (f"..\\imgs\\{self.name}.png")
        return path

    def __repr__(self):
        return "Agent" + super().__repr__() + f" value={self.value}, " \
                                              f"src={self.src}, dest={self.dest}, speed={self.speed}"
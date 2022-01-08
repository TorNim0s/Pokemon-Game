import random

from src.Node import Node


class Pokemon(Node):
    def __init__(self, id: int, pos: tuple, value, type):
        super().__init__(id, pos)
        self.value = value
        self.type = type
        self.loc = ()
        self.name = self.generateName()
        self.path = self.getPath()
        self.occupide = False
        self.chosen = False


    def generateName(self):
        list = ("Pikachu", "Bulbasaur", "squirtle", "Charizard")
        return random.choice(list)

    def getPath(self):
        path = (f"..\\data\\{self.name}.png")
        return path

    def __repr__(self):
        return "Pokemon" + super().__repr__() + f"value ={self.value}, type = {self.type}, loc={self.loc}"
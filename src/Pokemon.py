import random

from src.Node import Node


class Pokemon(Node):
    def __init__(self, id: int, pos: tuple, value, type):
        super().__init__(id, pos)
        self.value = value
        self.type = type
        self.loc = ()
        self.name = self.generateName()
        self.occupide = False

    def generateName(self):
        list = ("Bulbasaur", "Ivysaur", "Venusaur", "VenusaurMega", "Venusaur","Charmander",
                "Charmeleon","Charizard", "Squirtle", "Wartortle","Blastoise","Caterpie",
                "Metapod","Butterfree","Weedle","Kakuna","Beedrill","Pidgey","Pidgeotto",
                "Pidgeot","Rattata","Raticate","Spearow","Fearow","Ekans","Arbok","Pikachu",
                "Raichu","Sandshrew","Sandslash")
        return random.choice(list)

    def __repr__(self):
        return "Pokemon" + super().__repr__() + f"value ={self.value}, type = {self.type}, loc={self.loc}"
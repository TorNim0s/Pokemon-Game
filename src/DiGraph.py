from src.Agent import Agent
from src.Node import Node
from src.Pokemon import Pokemon


class DiGraph():

    def __init__(self):
        self._nodes = {}
        self._inedges = {}
        self._outedges = {}
        self._mc = 0
        self._agents = {}
        self._pokemons = {}

        self.__edgesCounter_ = 0
        self.__nodesCounter_ = 0
        self.__agentsCounter_ = 0
        self.__pokemonsCounter_ = 0

        self.bound = ()

    def getNode(self, node_id):
        return self._nodes[node_id]

    def getAgent(self, agent_id):
        return self._agents[agent_id]

    def clearPokemons(self):
        self._pokemons.clear()

    def v_size(self) -> int:
        return self.__nodesCounter_

    def e_size(self) -> int:
        return self.__edgesCounter_

    def a_size(self) -> int:
        return self.__agentsCounter_

    def p_size(self) -> int:
        return self.__pokemonsCounter_

    def get_mc(self) -> int:
        return self._mc

    def getWeight(self, src, dst):
        return self._outedges[src][dst]

    def calc_bound(self):
        # get data proportions
        min_x = min(list(self._nodes.values()), key=lambda n: n.getPos()[0]).getPos()[0]
        min_y = min(list(self._nodes.values()), key=lambda n: n.getPos()[1]).getPos()[1]
        max_x = max(list(self._nodes.values()), key=lambda n: n.getPos()[0]).getPos()[0]
        max_y = max(list(self._nodes.values()), key=lambda n: n.getPos()[1]).getPos()[1]
        self.bound = {"min_x":min_x, "min_y":min_y, "max_x":max_x, "max_y":max_y}

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self._outedges.keys() or id2 not in self._inedges.keys():
            return False

        if id2 in self._outedges[id1].keys() or id1 in self._inedges[id2].keys():
            return False

        self._outedges[id1][id2] = weight
        self._inedges[id2][id1] = weight
        self.__edgesCounter_ += 1

        return True

    def add_agent(self, id, pos:tuple, value, src, dest, speed) -> bool:
        if id in self._agents.keys():
            return False

        agent = Agent(id, pos, value, src, dest, speed)
        self._agents[id] = agent

        return True

    def add_pokemon(self, id, pos, value, type) -> bool:
        if pos in self._pokemons.keys():
            return False

        pokemon = Pokemon(id, pos, value, type)
        self._pokemons[pos] = pokemon

        return True

    def get_pokemon(self, pos):
        return self._pokemons[pos]

    def del_pokemon(self, pokemon):
        if(not pokemon):
            return

        self._pokemons.__delitem__(pokemon.getPos())

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self._nodes.keys():
            return False

        nd = Node(node_id,pos)
        self._nodes[node_id] = nd

        self._inedges[node_id] = {}
        self._outedges[node_id] = {}

        self.__nodesCounter_ += 1

        return True

    def remove_node(self, node_id: int) -> bool:
        if node_id not in self._nodes:
            return False

        self._nodes.__delitem__(node_id)
        for edge in self._outedges[node_id]:
            self._inedges[edge].__delitem__(node_id)
            self.__edgesCounter_ -= 1

        for edge in self._inedges[node_id]:
            self._outedges[edge].__delitem__(node_id)
            self.__edgesCounter_ -= 1

        self._outedges.__delitem__(node_id)
        self._inedges.__delitem__(node_id)

        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 not in self._outedges.keys() or node_id2 not in self._inedges.keys():
            return False

        if node_id2 not in self._outedges[node_id1] or node_id1 not in self._inedges[node_id2]:
            return False

        self._outedges[node_id1].__delitem__(node_id2)
        self._inedges[node_id2].__delitem__(node_id1)

        self.__edgesCounter_ -= 1

        return True

    def get_all_a(self) -> dict:
        return self._agents

    def get_all_p(self) -> dict:
        return self._pokemons

    def get_all_v(self) -> dict:
        return self._nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self._inedges[id1]

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self._outedges[id1]

    def __repr__(self):
        return f"DiGraph:\n" \
               f"Node({self._nodes})\n" \
               f"Edges({self._outedges})\n" \
               f"Agents({self._agents})\n" \
               f"Pokemon({self._pokemons})\n"
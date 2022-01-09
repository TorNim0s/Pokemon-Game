import math
import sys
from typing import List


from src.DiGraph import DiGraph
from src.Node import Node

EPS1 = 0.001
EPS2 = EPS1 * EPS1

class GraphAlgo():

    def __init__(self, graph = DiGraph()):
        self._graph = graph


    def shortest_path(self, id1: int, id2: int) -> (float, list):
        prev, dist = self.DijkstraAlgo(id1)
        path = []
        nd = prev[id2]
        while (nd != None and prev[nd.getID()] != None):
            path.insert(0,nd.getID())
            nd = prev[nd.getID()]

        if nd != None:
            path.insert(0, nd.getID())

        path.append(id2)

        return((dist[id2], path))

    def DijkstraAlgo(self, src):
        visit = []
        dist = []
        prev = []
        for i in range(self._graph.v_size()):
            visit.append(i)
            dist.append(sys.maxsize)
            prev.append(None)
        dist[src] = 0

        while (visit):
            lowerIndex = 0
            lowerValue = dist[visit[lowerIndex]]
            for i in range(len(visit)):
                if(lowerValue > dist[visit[i]]):
                    lowerIndex = i
                    lowerValue = dist[visit[i]]
            edges = self._graph.all_out_edges_of_node(visit[lowerIndex])
            for dst, weight in edges.items():
                alt = dist[visit[lowerIndex]] + weight
                if(alt < dist[dst]):
                    dist[dst] = alt
                    prev[dst] = self._graph.getNode(visit[lowerIndex])

            visit.remove(visit[lowerIndex])

        return prev,dist


    def get_graph(self):
        return self._graph

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        if not node_lst:  # if cities list is empty return null
            return None
        totalWeight = 0
        salesman = []
        start = node_lst[0]
        salesman.append(start)  # adding to the list the starting city
        for node in node_lst:  # loop on all the cities and find for them the shortest path
            dst = node
            if dst in salesman:
                continue

            weight, path = self.shortest_path(start, dst)
            for j in path:  # loop on all nodes that are part of the path from one city to another
                if not j == start:
                    salesman.append(j)  # add them to the list
                    totalWeight += weight

            start = dst  # update the starting city for the next iteration

        return salesman, totalWeight

    def GBA(self, agent):
        """
        Get Best Agent to the pokemon
        """

        if agent.onduty:
            return

        a_pos = agent.src

        best = {}
        lst = {}
        pokemon_save = {}
        # shortest path-> weight / speed
        for index, pokemon in enumerate(self._graph.get_all_p().values()):
            if pokemon.occupide:
                continue
            p_src, p_dst = pokemon.loc

            time = 0
            lst2 = []

            lst2, time = self.TSP((a_pos, p_src, p_dst))

            # lst2, time = self.TSP(a_pos, p_src, p_dst)
            time /= pokemon.value
            best[index] = time
            lst[index] = lst2
            pokemon_save[index] = pokemon

        if not best:
            return

        lowesetTime = min(best.values())
        res = list(filter(lambda x: best[x] == lowesetTime, best))
        list_lowest = lst[res[0]]

        list_lowest.reverse()
        agent.list = list_lowest
        agent.onduty = True
        agent.pokemon = pokemon_save[res[0]]
        pokemon_save[res[0]].occupide = True




    def isOnEdge(self, src: Node, dst: Node, pos, type):
        srcPos = src.getPos()
        dstPos = dst.getPos()

        if (type < 0 and dst.getID() > src.getID()):
            return False

        if (type > 0 and src.getID() > dst.getID()):
            return False

        dist = math.dist(srcPos, dstPos)
        d1 = math.dist(srcPos, pos) + math.dist(pos, dstPos)

        if (dist > d1 - EPS2):
            return True

        return False

    def PFL(self):
        """
        Pokemon Find Location -> find the edge the pokemon is at
        """
        for pokemon in self._graph.get_all_p().values():
            p_x, p_y = pokemon.getPos()
            for src, node in self._graph.get_all_v().items():
                for edge in self._graph.all_in_edges_of_node(src).keys():
                    dst = edge

                    if not self.isOnEdge(node,self._graph.getNode(dst),pokemon.getPos(), pokemon.type):
                        continue

                    pokemon.loc = (src, dst)

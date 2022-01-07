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

    def load_from_json(self, file_name: str) -> bool:
        pass

    def save_to_json(self, file_name: str) -> bool:
        pass

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

    def centerPoint(self) -> (int, float):
        maxDis = sys.maxsize
        nodeKey = 0
        nodes = self._graph.get_all_v()
        for node in nodes.values():
            src = node.getID()
            maxShortPath = 0
            nodes2 = self._graph.get_all_v()
            for dst in nodes2.values():
                if(dst!=node):
                    checkPath = self.shortest_path(src,dst.getID())
                    dist = checkPath[0]
                    if(dist > maxShortPath):
                        maxShortPath = dist
            if(maxShortPath< maxDis):
                maxDis = maxShortPath
                nodeKey = src

        return (nodeKey, maxDis)

    def GBA(self):
        """
        Get Best Agent to the pokemon
        """

        for pokemon in self._graph.get_all_p().values():

            p_src, p_dst = pokemon.loc

            best = {}
            lst = {}
            for index, agent in enumerate(self._graph.get_all_a().values()):
                if(agent.onduty):
                    continue
                a_pos = agent.src
                lst2, time = self.TSP((a_pos,p_src,p_dst))
                best[index] = time
                lst[index] = lst2

                lowesetTime = min(best.values())
                res = list(filter(lambda x: best[x] == lowesetTime, best))
                list_lowest = lst[res[0]]

                if(len(list_lowest) > 0):
                    list_lowest.reverse()
                    agent.list = list_lowest
                    agent.onduty = True
                    agent.pokemon = pokemon

    def GBA2(self):
        """
        Get Best Agent to the pokemon
        """

        for agent in self._graph.get_all_a().values():
            if agent.onduty:
                continue

            print(f"agent:{agent} -> duty:{agent.onduty}")

            a_pos = agent.src

            best = {}
            lst = {}

            for index, pokemon in  enumerate(self._graph.get_all_p().values()):

                if not self.checkIfAvailable(pokemon, agent):
                    continue

                p_src, p_dst = pokemon.loc

                lst2, time = self.TSP((a_pos, p_src, p_dst))
                best[index] = time
                lst[index] = lst2

            lowesetTime = min(best.values())
            res = list(filter(lambda x: best[x] == lowesetTime, best))
            list_lowest = lst[res[0]]

            list_lowest.reverse()
            agent.list = list_lowest
            agent.onduty = True
            agent.pokemon = pokemon

    def GBA3(self):
        """
        Get Best Agent to the pokemon
        """

        for agent in self._graph.get_all_a().values():
            if (agent.onduty):
                continue

            agent.pokemon = []

            total_list = []

            for i in range(self._graph.p_size()/self._graph.a_size()):
                a_pos = agent.src

                best = {}
                lst = {}

                for index, pokemon in  enumerate(self._graph.get_all_p().values()):

                    if not self.checkIfAvailable(pokemon):
                        continue

                    p_src, p_dst = pokemon.loc

                    lst2, time = self.TSP((a_pos, p_src, p_dst))
                    best[index] = time
                    lst[index] = lst2

                lowesetTime = min(best.values())
                res = list(filter(lambda x: best[x] == lowesetTime, best))
                list_lowest = lst[res[0]]
                list_lowest.reverse()

                total_list.append(list_lowest)

            agent.list = list_lowest
            agent.onduty = True
            agent.pokemon.append(pokemon)


    def checkIfAvailable(self, pokemon, a):
        for agent in self._graph.get_all_a().values():
            if not agent.pokemon or a == agent:
                continue
            if agent.pokemon.loc == pokemon.loc:
                print(f"Agent {agent._id}: -> {agent.pokemon}")
                return False

        return True

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

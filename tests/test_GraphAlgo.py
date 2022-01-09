from unittest import TestCase

from src.GraphAlgo import GraphAlgo
from src.Agent import Agent
from src.Pokemon import Pokemon


class TestGraphAlgo(TestCase):

    def test_shortest_path(self):
        graphAlgo = GraphAlgo()
        graphAlgo.get_graph().add_node(0)
        graphAlgo.get_graph().add_node(1)
        graphAlgo.get_graph().add_node(2)
        graphAlgo.get_graph().add_node(3)
        graphAlgo.get_graph().add_node(4)
        graphAlgo.get_graph().add_edge(0, 1, 1)
        graphAlgo.get_graph().add_edge(1, 2, 3)
        graphAlgo.get_graph().add_edge(2, 3, 4)
        graphAlgo.get_graph().add_edge(2, 4, 5)

        src = graphAlgo.get_graph().getNode(0).getID()
        dst = graphAlgo.get_graph().getNode(3).getID()
        weight, path = graphAlgo.shortest_path(src, dst)
        self.assertEqual(weight, 8)
        self.assertEqual(path, [0, 1, 2,3])




    def test_tsp(self):
        graphAlgo = GraphAlgo()
        graphAlgo.get_graph().add_node(0)
        graphAlgo.get_graph().add_node(1)
        graphAlgo.get_graph().add_node(2)
        graphAlgo.get_graph().add_node(3)
        graphAlgo.get_graph().add_node(4)
        graphAlgo.get_graph().add_edge(0, 1, 1)
        graphAlgo.get_graph().add_edge(1, 2, 3)
        graphAlgo.get_graph().add_edge(2, 3, 4)
        graphAlgo.get_graph().add_edge(2, 4, 5)

        path, weight = graphAlgo.TSP([0, 1, 2])

        self.assertEqual(weight, 4)
        self.assertEqual(path, [0,1,2])


    def test_is_on_edge(self):
        graphAlgo = GraphAlgo()
        graphAlgo.get_graph().add_node(0,(10,16))
        graphAlgo.get_graph().add_node(1,(13,17))
        graphAlgo.get_graph().add_node(2,(18,21))
        graphAlgo.get_graph().add_node(3,(18,18))
        graphAlgo.get_graph().add_node(4,(70,49))
        graphAlgo.get_graph().add_edge(0, 1, 1)
        graphAlgo.get_graph().add_edge(1, 2, 3)
        graphAlgo.get_graph().add_edge(2, 3, 4)
        graphAlgo.get_graph().add_edge(3, 4, 5)
        graphAlgo.get_graph().add_edge(4, 0, 9)
        graphAlgo.get_graph().add_pokemon(1,(18,20),4,-1)

        self.assertEqual(True ,graphAlgo.isOnEdge(graphAlgo.get_graph().getNode(2),graphAlgo.get_graph().getNode(3),(18,20),0))

    def test_pfl(self):
        graphAlgo = GraphAlgo()
        graphAlgo.get_graph().add_node(0, (10, 16))
        graphAlgo.get_graph().add_node(1, (13, 17))
        graphAlgo.get_graph().add_node(2, (18, 21))
        graphAlgo.get_graph().add_node(3, (18, 18))
        graphAlgo.get_graph().add_node(4, (70, 49))
        graphAlgo.get_graph().add_edge(0, 1, 1)
        graphAlgo.get_graph().add_edge(1, 2, 3)
        graphAlgo.get_graph().add_edge(2, 3, 4)
        graphAlgo.get_graph().add_edge(3, 4, 5)
        graphAlgo.get_graph().add_edge(4, 0, 9)
        graphAlgo.get_graph().add_pokemon(1, (18,20), 4, -1)
        graphAlgo.PFL()
        for pok in graphAlgo.get_graph().get_all_p().values():
            self.assertEqual((3,2),pok.loc)
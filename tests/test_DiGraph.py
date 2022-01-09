from unittest import TestCase

from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


class TestDiGraph(TestCase):

    def test_v_size(self):
        graph = DiGraph()
        g_algo = GraphAlgo(graph)
        print(g_algo.get_graph().v_size())
        g_algo.get_graph().add_node(1,(8, 4))
        g_algo.get_graph().add_node(2,(10, 6))
        print(g_algo.get_graph().v_size())

        self.assertEqual(2,g_algo.get_graph().v_size())


    def test_get_node(self):
        graph = DiGraph()
        g_algo = GraphAlgo(graph)
        g_algo.get_graph().add_node(1,(8,4))
        node=g_algo.get_graph().getNode(1).getID()
        self.assertEqual(node,1)


    def test_e_size(self):
        graph = DiGraph()
        g_algo = GraphAlgo(graph)
        print(g_algo.get_graph())
        g_algo.get_graph().add_node(1, (8, 4))
        g_algo.get_graph().add_node(2, (13, 9))
        g_algo.get_graph().add_edge(1,2,5)
        print(g_algo.get_graph())
        self.assertEqual(1, g_algo.get_graph().e_size())

    def test_add_edge(self):
        graph=DiGraph()
        g_algo = GraphAlgo(graph)
        g_algo.get_graph().add_node(8, (28.12364, 22.426164, 0))
        g_algo.get_graph().add_node(3, (28.32364, 25.346164, 0))
        g_algo.get_graph().add_edge(3, 8, 2.5)
        self.assertEqual({3: 2.5}, g_algo.get_graph().all_in_edges_of_node(8))

    def test_add_node(self):
        graph = DiGraph()
        g_algo = GraphAlgo(graph)
        g_algo.get_graph().add_node(8, (28.12364, 22.426164, 0))
        g_algo.get_graph().add_node(3, (28.32364, 25.346164, 0))
        g_algo.get_graph().add_edge(3, 8, 2.5)
        self.assertEqual(3, g_algo.get_graph().getNode(3).getID())

    def test_remove_node(self):
        graph = DiGraph()
        g_algo = GraphAlgo(graph)
        for n in range(3):
            g_algo.get_graph().add_node(n)
        g_algo.get_graph().add_edge(0, 1, 2)
        g_algo.get_graph().add_edge(1, 2, 2.5)
        g_algo.get_graph().add_edge(2, 1, 5.2)
        # g_algo.get_graph().remove_node(0)
        self.assertEqual(True, g_algo.get_graph().remove_node(0))

    def test_remove_edge(self):
        graph = DiGraph()
        g_algo = GraphAlgo(graph)
        for n in range(3):
            g_algo.get_graph().add_node(n)
        g_algo.get_graph().add_edge(0, 1, 2)
        g_algo.get_graph().add_edge(1, 2, 2.5)
        g_algo.get_graph().add_edge(2, 1, 5.2)
        # g_algo.get_graph().remove_node(0)
        self.assertEqual(True, g_algo.get_graph().remove_edge(0,1))

    def test_get_all_v(self):
        graph = DiGraph()
        g_algo = GraphAlgo(graph)
        for n in range(3):
            g_algo.get_graph().add_node(n)
        g_algo.get_graph().add_edge(0, 1, 2)
        g_algo.get_graph().add_edge(1, 2, 2.5)
        g_algo.get_graph().add_edge(2, 1, 5.2)
        self.assertEqual(3, g_algo.get_graph().v_size())

    def test_all_in_edges_of_node(self):
        graph = DiGraph()
        g_algo = GraphAlgo(graph)

        g_algo.get_graph().add_node(0)
        g_algo.get_graph().add_node(1)
        g_algo.get_graph().add_node(2)
        g_algo.get_graph().add_edge(0, 1, 2)
        g_algo.get_graph().add_edge(0, 2, 2.5)
        g_algo.get_graph().add_edge(2, 1, 5.2)
        self.assertEqual({0: 2, 2: 5.2} ,g_algo.get_graph().all_in_edges_of_node(1))

    def test_all_out_edges_of_node(self):
        graph = DiGraph()
        g_algo = GraphAlgo(graph)

        g_algo.get_graph().add_node(0)
        g_algo.get_graph().add_node(1)
        g_algo.get_graph().add_node(2)
        g_algo.get_graph().add_edge(0, 1, 2)
        g_algo.get_graph().add_edge(0, 2, 2.5)
        g_algo.get_graph().add_edge(2, 1, 5.2)
        self.assertEqual({1: 2, 2:2.5}, g_algo.get_graph().all_out_edges_of_node(0))

    def test_add_agent(self):
        graph = DiGraph()
        g_algo = GraphAlgo(graph)
        self.assertEqual(True,g_algo.get_graph().add_agent("nir",(10,8),4,2,5,4))

    def test_add_pokemon(self):
        graph = DiGraph()
        g_algo = GraphAlgo(graph)
        self.assertEqual(True, g_algo.get_graph().add_pokemon(1,(14,3),5,1))





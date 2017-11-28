import os
import random
import sys
import time

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../node/'))
if not path in sys.path:
    sys.path.insert(1, path)
del path
import node
import dijkstraAlgo
import floyd_WarshallAlgo
import unittest


class TestAlgo(unittest.TestCase):
    def setUp(self):
        self.dijkstra = dijkstraAlgo.DijkstraAlgo()
        self.floyd_Warshall = floyd_WarshallAlgo.Floyd_WarshallAlgo()
        self.graph = {}

        

        self.nodeA = node.Node()
        self.nodeA.connections = {'2': 28.46853, '3': 39.6262476667, '4': 17.8152866667};

        self.nodeB = node.Node()
        self.nodeB.connections = {'1': 39.6262476667, '2': 11.8031383333, '4': 12.8671733333};

        self.nodeC = node.Node()
        self.nodeC.connections = {'1': 28.46853, '3': 11.8031383333, '4': 19.93348};

        self.nodeD = node.Node()
        self.nodeD.connections = {'1': 17.8152866667, '2': 19.93348, '3': 12.8671733333};

        self.graph = {'1': self.nodeA,
                      '2': self.nodeB,
                      '3': self.nodeC,
                      '4': self.nodeD}

        self.big_graph = {}
        for i in range(20):
            aNode = node.Node();
            for j in range(20):
                if j != i:
                    aNode.connections[`j`] = random.randint(1, 11)
            self.big_graph[`i`] = aNode

    def test_addConnection_raise_TypeError(self):
        with self.assertRaises(TypeError):
            self.dijkstra.findRoutingPath([])
        with self.assertRaises(TypeError):
            self.floyd_Warshall.findRoutingPath([])

    # Dijkstra
    def test_algo_Dijkstra_complets_the_routingPath_of_the_sourceNode(self):
        self.dijkstra.findRoutingPath(self.graph)
        print "######### Dijkstra ######### "
        TestAlgo.print_graph(self.graph)

    # Floyd Warshall
    def test_algo_Floyd_Warshall_complets_the_routingPath_of_the_sourceNode(self):
        startTime = time.time()
        self.floyd_Warshall.findRoutingPath(self.graph)
        t = time.time() - startTime
        print "######### Floyd Warshall #########"
        TestAlgo.print_graph(self.graph)

    def test_benchMark(self):
        start_time = time.time()
        self.dijkstra.findRoutingPath(self.big_graph)
        print "####Dijkstra time       : %s" % (time.time() - start_time)

        start_time = time.time()
        self.floyd_Warshall.findRoutingPath(self.big_graph)
        print "####Floyd_Warshall time : %s" % (time.time() - start_time)

    @staticmethod
    def print_graph(graph):
        for key in graph:
            print "from " + key + ":"
            for key2 in graph:
                print "       to {} ->{}  value: {}".format(key2, graph[key].routingPath[key2].path,
                                                            graph[key].routingPath[key2].value)
        print "--------------------------------------------"


if __name__ == '__main__':
    unittest.main()

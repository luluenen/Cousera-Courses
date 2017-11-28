import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), './node/'))
if not path in sys.path:
    sys.path.insert(1, path)

path = os.path.abspath(os.path.join(os.path.dirname(__file__), './algo/'))
if not path in sys.path:
    sys.path.insert(1, path)

del path
import node

from controller import output_log_file
import floyd_WarshallAlgo

import unittest


class TestController(unittest.TestCase):
    def setUp(self):
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

    def test_output_log_file(self):
        self.floyd_Warshall.findRoutingPath(self.graph)
        output_log_file(self.graph)

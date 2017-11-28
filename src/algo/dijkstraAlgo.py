import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../node/'))
if not path in sys.path:
    sys.path.insert(1, path)

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils/'))
if not path in sys.path:
    sys.path.insert(1, path)
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
if not path in sys.path:
    sys.path.insert(1, path)
del path
import algo
import node
import utils
from priodict import priorityDictionary

class DijkstraAlgo:
	@staticmethod
	def __DijkstraFromSource(graph, sourceNode):
		utils.Utils.isStr(sourceNode)
		if sourceNode not in graph:
			raise ValueError('the source node is not in the graph')

		D = {}	# dictionary of final distances
		P = {}	# dictionary of predecessors
		Q = priorityDictionary()	# estimated distances of non-final vertices
		Q[sourceNode] = 0
	
		for anode in Q:
			D[anode] = Q[anode]
			graph[sourceNode].routingPath[anode]=node.Path([],0.0)
		
			for neighbor in graph[anode].connections:
				sourceToNeighborLenght = D[anode] + graph[anode].connections[neighbor]
				if neighbor in D:
					if sourceToNeighborLenght < D[neighbor]:
						raise ValueError, "Dijkstra: found better path to already-final vertex"
				elif neighbor not in Q or sourceToNeighborLenght < Q[neighbor]:
					Q[neighbor] = sourceToNeighborLenght
					P[neighbor] = anode
			graph[sourceNode].routingPath[anode].value = Q[anode]	
			end = anode;
			while 1:
				graph[sourceNode].routingPath[anode].path.append(end)
				if end == sourceNode: break
				end = P[end]				
			graph[sourceNode].routingPath[anode].path.reverse()
	
	def findRoutingPath(self,graph):
		utils.Utils.isDict(graph)	
		for key in graph:
			DijkstraAlgo.__DijkstraFromSource(graph,key)

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

class Floyd_WarshallAlgo:
	def findRoutingPath(self,graph):
		utils.Utils.isDict(graph)

		dist = {}
		pred = {}
		for u in graph:
		    dist[u] = {}
		    pred[u] = {}
		    for v in graph:
		        dist[u][v] = 1000
		        pred[u][v] = -1
		    dist[u][u] = 0
		    for neighbor in graph[u].connections:
		        dist[u][neighbor] = graph[u].connections[neighbor]
		        pred[u][neighbor] = u

		for t in graph:
		    for u in graph:
		        for v in graph:
		            newdist = dist[u][t] + dist[t][v]
		            if newdist < dist[u][v]:
		                dist[u][v] = newdist
		                pred[u][v] = pred[t][v]
		for s in graph:
			for d in graph:
				graph[s].routingPath[d]=node.Path([],0.0)
				end = d;
				graph[s].routingPath[d].value = dist[s][d]
				while 1:
					graph[s].routingPath[d].path.append(end)
					if end == s: break
					end = pred[s][end]
				graph[s].routingPath[d].path.reverse()

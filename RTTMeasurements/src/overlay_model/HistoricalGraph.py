# MesuresOverlayRipeAtlas
#
# Copyright (C) 2016 Florencia ALVAREZ ETCHEVERRY
# <florencia.alvarezetcheverry@telecom-bretagne.eu>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, version 2.

import logging

from src.common.settings import PROBE_NOT_FOUND
from src.overlay_model.Graph import Graph


class HistoricalGraph(Graph):
    """
    This class represents the network and has the information measured through
    measurment's time.
    """
    def __init__(self, nodes, start_time, stop_time, interval):
        self._size = int((stop_time-start_time).total_seconds()/interval)
        super(HistoricalGraph, self).__init__(nodes, self._size)
        self.is_ready = False
        self._completed_state = [0] * self._size
        self._ready_graph = None
        self._start = start_time
        self._stop = stop_time
        self._interval = interval

    def __getitem__(self, key, second=None):
        return super(HistoricalGraph, self).__getitem__(key, second)

    def __setitem__(self, key, value):
        """
        Adds the rtt value to the key's list of values through time
        @param key: Tuple of ids (edge of graph)
        @param value: Tuple of (rtt, timestamp)

        @return: -
        """

        edge_values = super(HistoricalGraph, self).__getitem__(key)
        with self._lock:
            diff = value[1] - self._start.timestamp()
            value_index = int(diff/self._interval)
            try:
                if edge_values[value_index] != PROBE_NOT_FOUND:
                    logging.info("Repeated value for edge %s, position %s, "
                                 "timestamp %s.", key,
                                 value_index,
                                 value[1])
                edge_values[value_index] = value[0]
            except IndexError:
                logging.error("Value in graph out of index. Edge %s, position "
                              "%s, timestamp %s.", key,
                              value_index,
                              value[1])

    def get_all_graphs(self):
        """
        Generates and returns a list with all the graphs with
        the rtts retrieved.
        @return: List of <Graph>
        """
        graph_list = []
        for i in range(self._size):
            g = Graph(self.nodes)
            for key in self.keys():
                element = self[key].pop(0)
                g[key] = element
            graph_list.append(g)
        return graph_list

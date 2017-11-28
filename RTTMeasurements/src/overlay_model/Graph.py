# MesuresOverlayRipeAtlas
#
# Copyright (C) 2016 Florencia ALVAREZ ETCHEVERRY
# <florencia.alvarezetcheverry@telecom-bretagne.eu>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, version 2.

import logging
from threading import Lock

from src.common.exceptions import InvalidIPAddress, InvalidProbeNumber
from src.common.settings import PROBE_NOT_FOUND


class Graph(dict):
    """
    This class represents the network, having a list of the probes of Node type,
    and synchronized access.
    """

    def __init__(self, nodes, lists=False):
        super(Graph, self).__init__()
        self.nodes = nodes
        self.nb_probes = len(nodes)
        self.nodes_ids = [n.id for n in self.nodes]
        self._lock = Lock()

        for id_i in self.nodes_ids:
            for id_j in self.nodes_ids:
                if id_i != id_j:
                    if lists:
                        Graph.__setitem__(self, (id_i, id_j),
                                          [PROBE_NOT_FOUND]*lists)
                    else:
                        Graph.__setitem__(self, (id_i, id_j), PROBE_NOT_FOUND)
        logging.info("Initialized with the list of nodes: %s.", nodes)
        assert len(list(self.keys())) == (self.nb_probes*(self.nb_probes-1))/2

    def __getitem__(self, key, second=None):
        with self._lock:
            return super(Graph, self).__getitem__(tuple(sorted(key)))

    def __setitem__(self, key, value):
        assert len(key) == 2, "Key must be a Tuple of 2"
        with self._lock:
            super(Graph, self).__setitem__(tuple(sorted(key)), value)

    def get_id_by_address(self, address):
        with self._lock:
            for n in self.nodes:
                if n.ip_address == address:
                    return n.id
            logging.error("IP address %s not found.", address)
            raise InvalidIPAddress

    def get_id_by_probe(self, probe_number):
        with self._lock:
            for n in self.nodes:
                if n.probe_id == probe_number:
                    return n.id
            logging.error("Probe number %s not found.", probe_number)
            raise InvalidProbeNumber

    def get_node_by_id(self, node_id):
        with self._lock:
            for n in self.nodes:
                if n.id == node_id:
                    return n
            logging.error("Node id %s not found.", node_id)
            raise InvalidProbeNumber

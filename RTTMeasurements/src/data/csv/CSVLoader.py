# MesuresOverlayRipeAtlas
#
# Copyright (C) 2016 Florencia ALVAREZ ETCHEVERRY
# <florencia.alvarezetcheverry@telecom-bretagne.eu>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, version 2.

import csv
import logging
import random

from src.data.Loader import Loader
from src.overlay_model.Node import Node


class CSVLoader(Loader):
    def __init__(self, probe_file):
        self.probe_file = probe_file

    def load_probe_nodes(self, nb_probes, choose_random=False):
        """
        Reads from the CSV file the list of nodes in the graph, with its id,
        probe_id and adress.
        Row format: [id, probe_id, ip]
        @param nb_probes: Number of probes to read from the file
        @type nb_probes: int

        @param choose_random: If True it will load nb_probes random probes
        @type choose_random: bool

        @return: List of Node instances
        """
        nodes = []
        with open(self.probe_file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",")
            spamreader.__next__()
            for i, row in enumerate(spamreader, start=1):
                node = Node(n_id=int(row[0]),
                            probe_id=int(row[1]),
                            address=row[2])
                nodes.append(node)
                if not choose_random and i >= nb_probes:
                    break

        if choose_random:
            rnd_nodes = []
            length = len(nodes)
            for i in range(nb_probes):
                rnd = random.randrange(length)
                rnd_nodes.append(nodes[rnd])
            logging.info("Successfully read %s random probes.",
                         nb_probes)
            return rnd_nodes

        logging.info("Successfully read %s first probes.", nb_probes)
        return nodes

    def load_measurement(self, file):
        """
        Reads the CSV file of the measurement created, loading the list of
        probes and the measurements ids.
        @param file: Path to the measurements file.
        @type file: str

        @return: (json string of probes list, string list of measurements ids)
        @rtype: tuple
        """
        with open(file, 'r') as msm_file:
            nodes = msm_file.readline()
            msm_ids = msm_file.readline()
        logging.info("Successfully loaded node list and measurements ids.")
        return nodes, msm_ids

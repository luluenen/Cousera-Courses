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

from src.data.Saver import Saver
from src.data.csv import files_configuration as files


class CSVSaver(Saver):

    def __init__(self):
        self.initialized = False

    def _save_execution(self, file_name, graph):
        """
        Saves the measures graph in a CSV file following the following format:
            Probes  0   1   2...
            0       0   x   y
            1       x   0   z
            2       y   z   0
            ...

        @param file_name: Name of the file to save the measurement data
        @type file_name: str

        @param graph: Graph instance with Nodes and its measures
        @type graph: Graph

        @return: -
        """
        with open(file_name, 'a', newline='') as m_file:
            cols = ['Probes'] + graph.nodes_ids
            writer = csv.DictWriter(m_file, cols, delimiter=",")
            if not self.initialized:
                writer.writeheader()
                self.initialized = True

            for i in range(graph.nb_probes):
                row = {
                    'Probes': i,
                    i: 0
                }
                for j in range(graph.nb_probes):
                    if j != i:
                        row[j] = graph[i, j]
                writer.writerow(row)

        logging.info("Graph saved to CSV file.")

    def save_measures(self, graph, folder):
        """
        Saves the measures graph in a CSV file inside the given folder.
        Calls _save_execution().

        @param graph: Graph instance with Nodes and its measures
        @type graph: Graph

        @param folder: Name of the folder to save the measurement data
        @type folder: str

        @return: -
        """

        file = folder + files.OUTPUT_FILE
        try:
            self._save_execution(file, graph)

        except EnvironmentError as e:
            logging.error("%s. Error saving measurements, "
                          "using default folder.", e)
            self._save_execution(files.MEASURES_PATH + files.OUTPUT_FILE, graph)

    def save_msm_launch(self, time, nodes, msm_ids):
        """
        Saves the measurement file with 2 lines. The fist one is a json list of
        the Nodes, the second one is a list of the msm ids.
        @param time: Datetime to save in the correct folder.
        @type time: Datetime

        @param nodes: List of probes used.
        @type nodes: List <Nodes>

        @param msm_ids: Ids of the measurements created with Ripe Atlas.
        @type msm_ids: List<int>

        @return: -
        """

        folder = files.MEASURES_PATH + "{:%Y%m%d_%H%M%S}".format(time)

        with open(folder + files.MSM_CREATED_FILE, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile,
                                delimiter=',',
                                escapechar=' ',
                                quoting=csv.QUOTE_NONE)
            writer.writerow([nodes])
            writer.writerow(msm_ids)
        logging.info("Saved nodes and measurements ids successfully.")
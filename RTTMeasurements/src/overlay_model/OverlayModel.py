# MesuresOverlayRipeAtlas
#
# Copyright (C) 2016 Florencia ALVAREZ ETCHEVERRY
# <florencia.alvarezetcheverry@telecom-bretagne.eu>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, version 2.

import importlib
import json
import logging

from os import path

from ripe.atlas.cousteau import Measurement, AtlasResultsRequest

from src.data.JsonLoader import JsonLoader
from src.data.RawSaver import RawSaver
from src.data.csv.CSVLoader import CSVLoader
from src.data.csv.CSVSaver import CSVSaver
from src.common import settings as conf
from src.overlay_model.HistoricalGraph import HistoricalGraph
from src.overlay_model.Node import Node


class OverlayModel(object):

    def __init__(self, probe_file, params_file=None, time=None):
        self.data_loader = CSVLoader(probe_file)
        self.csv_saver = CSVSaver()
        self.nodes = []
        self.params_file = params_file
        self.msm_ids = None
        self.folder = None
        self._time = time

    def make_measures(self, params):
        """
        Creates and runs the measurements using Ripe Atlas.

        @param params: Parameters to launch the measurements.
        @type params: dict

        @return: -
        """

        # Load measure class
        try:
            measure_type = conf.MEASURES[params['measure_type']]
            imp_mod = importlib.import_module(measure_type)
            measure_class = getattr(imp_mod, measure_type.split('.')[-1])

        except(ImportError, AttributeError, KeyError) as e:
            measure_type = conf.DEF_MEASURE_TYPE
            imp_mod = importlib.import_module(measure_type)
            measure_class = getattr(imp_mod,
                                    measure_type.split('.')[-1])
            logging.error("%s. Couldn't create measure of type requested"
                          ", creating type %s instead.", e, measure_class)
        logging.info("Loaded successfully measure type %s.",
                     measure_type)
        try:
            nb_probes = int(params['nb_probes'])
        except (KeyError, ValueError) as e:
            nb_probes = conf.DEF_N_PROBES
            logging.error("%s. Couldn't load the number of probes "
                          "requested. Loading default number %s instead.",
                          e, nb_probes)
        try:
            random = True if params['random'] == 'True' else False
        except KeyError:
            random = conf.DEF_RANDOM

        # Load list of probes
        logging.info("Loading %s probes, random: %s.", nb_probes, random)
        nodes = self.data_loader.load_probe_nodes(nb_probes, random)

        # Instance measure class
        measure = measure_class(nodes, params)

        logging.info("Launching measurements.")
        self.msm_ids = measure.launch_measures()

        logging.info("Saving input parameters.")
        measure.parameters['nb_probes'] = nb_probes
        measure.parameters['random'] = random
        RawSaver.save_parameters(measure.parameters, self._time)

        logging.info("Saving nodes list and ids.")
        self.csv_saver.save_msm_launch(self._time, measure.nodes, self.msm_ids)

    def load_params(self):
        return JsonLoader.load_measure_params(self.params_file)

    def load_measure_info(self, file):
        """
        Read and initialize parameters: nodes and list of measurements ids
        @param file: Path and name of the file with the nodes and msm ids.
        @type file: str

        @return:
        """
        logging.info("Loading measurement info.")
        self.folder = path.split(file)[0] + path.sep
        nodes_str, msm_ids_str = self.data_loader.load_measurement(file)
        nodes = nodes_str.replace(" ", "")
        nodes_list = json.loads(nodes)
        for dic in nodes_list:
            node = Node(n_id=dic['id'],
                        probe_id=dic['probe_id'],
                        address=dic['ip_address'])
            self.nodes.append(node)
        self.msm_ids = [int(s) for s in msm_ids_str.split(',')]
        logging.info("Measurement information initialized.")

    def get_results(self):
        """
        Retrieve with the Ripe Atlas API the measurements results.
        @return: -
        """
        m = Measurement(id=self.msm_ids[0])
        hist_graph = HistoricalGraph(self.nodes, m.start_time, m.stop_time,
                                     m.interval)
        logging.info("Graph saver initialized.")

        for m in self.msm_ids:
            measure = Measurement(id=m)
            logging.debug("%s", vars(measure))

        for msm_id in self.msm_ids:
            success, results = AtlasResultsRequest(msm_id=msm_id).create()

            if not success:
                logging.error("Error fetching results for %s. %s",
                              msm_id, results)
            else:
                logging.info("Successfully retrieved %s results.", len(results))

                for result in results:
                    if int(result['lts']) == conf.INVALID_LTS \
                            or int(result['lts']) > conf.MAX_LTS:
                        logging.info("Value not considered, probe out of sync. "
                                     "Probe id: %s, target addr: %s, lts: %s, "
                                     "rtt: %s", result['prb_id'],
                                     result['dst_addr'],
                                     result['lts'],
                                     result['avg'])
                        continue
                    rtt = float(result['avg'])
                    if rtt == conf.RIPEATLAS_NO_RTT:
                        rtt = conf.NOT_MEASURED
                    id_probe_src = result['prb_id']
                    target_addr = result['dst_addr']

                    id_src = hist_graph.get_id_by_probe(id_probe_src)
                    id_trg = hist_graph.get_id_by_address(target_addr)

                    hist_graph[id_src, id_trg] = (rtt, result['timestamp'])
        logging.info("Finished getting the results.")

        graphs = hist_graph.get_all_graphs()

        c = 0
        for graph in graphs:
            self.csv_saver.save_measures(graph, self.folder)
            c += 1
        logging.info("Finished saving %s graphs into CSV file.", c)


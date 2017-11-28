# MesuresOverlayRipeAtlas
#
# Copyright (C) 2016 Florencia ALVAREZ ETCHEVERRY
# <florencia.alvarezetcheverry@telecom-bretagne.eu>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, version 2.

import logging

from datetime import datetime

from src.common import settings as conf
from src.common.exceptions import AtlasKeyMissing
from src.overlay_model.Graph import Graph


class Measure(object):
    def __init__(self, nodes, params):

        self.graph = Graph(nodes)
        self.parameters = {}

        self._initialize_parameters(params)
        self._load_key(params)

    def launch_measures(self):
        """
        Launch the measures to ripe atlas and retrieve its ids.
        @return: List of measurements ids
        """
        nb_probes = len(self.graph.nodes)
        msm_ids = []

        for i in range(nb_probes - 1):
            target_node = self.graph.nodes[i]
            src_list = self.graph.nodes[i + 1:]

            # Create and send measurement request
            measure_id = self._make_measure(src_list, target_node)
            msm_ids.append(measure_id)

        return msm_ids

    def _initialize_parameters(self, params):
        """
        Validates and initializes parameters with given or defaults values.

        @param params: Dictionary of the parameters to launch the measurements.
        @type params: dict

        @return: -
        """
        try:
            self.parameters['af'] = int(params['af'])
        except (KeyError, ValueError) as e:
            self.parameters['af'] = conf.DEF_AF
            logging.error("%s. Using default af: %s.",
                          e, conf.DEF_AF)
        try:
            # Periodic measure
            try:
                self.parameters['start'] = datetime.strptime(
                                                params['start'],
                                                "%Y-%m-%dT%H:%M:%S.%f")
                self.parameters['end'] = datetime.strptime(
                                                params['end'],
                                                "%Y-%m-%dT%H:%M:%S.%f")
            except ValueError:
                logging.info("Using date format without seconds.")
                self.parameters['start'] = datetime.strptime(params['start'],
                                                             "%Y-%m-%dT%H:%M")
                self.parameters['end'] = datetime.strptime(params['end'],
                                                           "%Y-%m-%dT%H:%M")
            self.parameters['is_oneoff'] = False

            try:
                # An interval is only possible for a non one-off measure
                self.parameters['interval'] = int(params['interval'])
            except (KeyError, ValueError) as e:
                self.parameters['interval'] = conf.DEF_MEASURE_INTERVAL
                logging.error("%s. Using default interval: %s.",
                              e, conf.DEF_MEASURE_INTERVAL)
            logging.info("Parameters of periodic measure loaded.")

        # One-off measure
        except (KeyError, ValueError) as e:
            self.parameters['start'] = datetime.utcnow()
            self.parameters['end'] = self.parameters['start']
            self.parameters['interval'] = ""
            self.parameters['is_oneoff'] = True
            logging.info("Parameters of one-off measure loaded.")

    def _load_key(self, params):
        """
        Reads an initializes the Atlas Key.

        @param params: Dictionary of the parameters to launch the measurements.
        @type params: dict

        @raise: AtlasKeyMissing
        @return: -
        """
        try:
            key = params['key']
        except KeyError:
            raise AtlasKeyMissing("Measures can't be done without an Atlas Key.")
        self._atlas_create_key = key
        logging.info("Atlas API Key successfully loaded.")

    def _make_measure(self, src_list, target_probe):
        raise NotImplementedError

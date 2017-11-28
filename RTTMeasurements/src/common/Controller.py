# MesuresOverlayRipeAtlas
#
# Copyright (C) 2016 Florencia ALVAREZ ETCHEVERRY
# <florencia.alvarezetcheverry@telecom-bretagne.eu>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, version 2.

import logging


class Controller:

    def __init__(self, model):
        self.model = model

    def generate_measures(self):
        """
        Creates and runs the measurements with the Ripe Atlas API.
        @return: -
        """

        logging.info("Getting parameters.")
        measure_params = self.model.load_params()
        logging.info("Starting creation of measurements.")
        self.model.make_measures(measure_params)
        logging.info("Finished launching measures.")

    def generate_results(self, file):
        """
        Retrieves current available results of the measurements.
        @param file: Path and name of the file with the nodes and msm ids.
        @type file: str

        @return: -
        """
        logging.info("Getting information of measurement.")
        self.model.load_measure_info(file)
        logging.info("Getting results.")
        self.model.get_results()

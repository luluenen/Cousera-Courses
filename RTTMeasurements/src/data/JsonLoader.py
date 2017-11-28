# MesuresOverlayRipeAtlas
#
# Copyright (C) 2016 Florencia ALVAREZ ETCHEVERRY
# <florencia.alvarezetcheverry@telecom-bretagne.eu>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, version 2.

import json
import logging


class JsonLoader(object):

    @staticmethod
    def load_measure_params(file):
        """
        Reads and loads json file of the input parameters.
        @param file: Path and name of the json file with the parameters.
        @type file: str

        @return: Parameters for the measurement loaded
        @rtype: dict
        """

        with open(file) as data_file:
            try:
                params = json.load(data_file)
            except ValueError:
                logging.exception("Input json bad formatted.")
                raise
        logging.info("Parameters loaded from %s.", file)
        return params

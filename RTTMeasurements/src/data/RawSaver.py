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
import os

from src.data.csv.files_configuration import MEASURES_PATH, PARAM_INPUT_FILE


class RawSaver(object):

    def __init__(self, start_time):
        # Prepare folder to save raw data
        folder = "{:%Y%m%d_%H%M%S}".format(start_time)
        self.path = MEASURES_PATH + folder + os.sep
        self.results = []
        logging.info("Using %s folder to save the data.", self.path)

    @staticmethod
    def save_parameters(params, time):
        """
        Saves the actual used parameters for the measurements.
        @param params: Dictionary with the parameters
        @type params: dict

        @param time: Datetime to save in the correct folder.
        @type time: Datetime

        @return: -
        """

        parameters = params.copy()
        folder = MEASURES_PATH + "{:%Y%m%d_%H%M%S}".format(time)
        try:
            parameters['start'] = params['start'].isoformat()
            parameters['end'] = params['end'].isoformat()
        except AttributeError:
            parameters.pop('start')
            parameters.pop('end')

        logging.debug("Params: %s", parameters)
        try:
            with open(folder + PARAM_INPUT_FILE, 'w') as fp:
                json.dump(parameters, fp,
                          indent=2, separators=(',', ':'))
        except EnvironmentError as e:
            logging.error("%s. Error saving measurements, "
                          "using default folder.", e)
            folder = MEASURES_PATH
            with open(folder + PARAM_INPUT_FILE, 'w') as fp:
                json.dump(parameters, fp,
                          indent=4, separators=(',', ':'))
        logging.info("Parameters saved to json file.")

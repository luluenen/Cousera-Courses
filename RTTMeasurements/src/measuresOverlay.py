# MesuresOverlayRipeAtlas
#
# Copyright (C) 2016 Florencia ALVAREZ ETCHEVERRY
# <florencia.alvarezetcheverry@telecom-bretagne.eu>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, version 2.

import logging
import argparse as ap
import os
from datetime import datetime

from src.common import settings as conf
from src.data.csv.files_configuration import MEASURES_PATH, MSM_CREATED_FILE
from src.overlay_model.OverlayModel import OverlayModel
from src.common.Controller import Controller


def main(probe_file, params_file):

    time = datetime.utcnow()
    try:
        path = MEASURES_PATH + "{:%Y%m%d_%H%M%S}".format(time) + os.sep
        os.mkdir(path)
    except OSError as e:
        print("%s. Couldn't create folder to save the data.", e)
        path = MEASURES_PATH + "{:%Y%m%d_%H%M%S}-".format(time)
    logging.basicConfig(filename=path+conf.LOGFILE,
                        format='%(asctime)s -%(levelname)s- '
                               '%(module)s (%(funcName)s): %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S',
                        level=conf.LOG_LVL)

    logging.info("Main: STARTING")

    model = OverlayModel(probe_file, params_file, time)
    controller = Controller(model)

    controller.generate_measures()

    logging.info("Main: FINISHED")


if __name__ == "__main__":

    parser = ap.ArgumentParser(
        description="Generates and run the Ripe Atlas measurements with the "
                    "requested parameters and between all the probes. Output "
                    "files are generated in a folder named with the current "
                    "(local) time.",
        formatter_class=ap.ArgumentDefaultsHelpFormatter,
        epilog="To retrieve the results of this measure(s) run 'results.py' "
               "using the output file {} of this program."
                    .format(MSM_CREATED_FILE))
    parser.add_argument('--probes',
                        dest="probes",
                        default=conf.PROBES_INPUT,
                        help="CSV f"
                             "ile of probes for the measurement.")

    parser.add_argument('--params',
                        dest="parameters",
                        default=conf.PARAMS_FILE,
                        help="Json file to load the parameters of the "
                             "measurement.")

    ns = parser.parse_args()
    main(ns.probes, ns.parameters)

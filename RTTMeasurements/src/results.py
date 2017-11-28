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

from os import path

from src.common import settings as conf
from src.common.Controller import Controller
from src.overlay_model.OverlayModel import OverlayModel


def main(file):
    folder = path.split(file)[0] + path.sep
    logging.basicConfig(filename=folder+conf.RES_LOGFILE,
                        format='%(asctime)s -%(levelname)s- '
                               '%(module)s (%(funcName)s): %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S',
                        level=conf.LOG_LVL)

    logging.info("Main - STARTING")

    model = OverlayModel(None)
    controller = Controller(model)

    controller.generate_results(file)
    logging.info("Main - FINISHED")

if __name__ == '__main__':

    parser = ap.ArgumentParser()

    parser.add_argument('file',
                        help="File of measurement execution to get the data.")

    ns = parser.parse_args()
    main(ns.file)







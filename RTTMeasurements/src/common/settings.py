# MesuresOverlayRipeAtlas
#
# Copyright (C) 2016 Florencia ALVAREZ ETCHEVERRY
# <florencia.alvarezetcheverry@telecom-bretagne.eu>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, version 2.

import logging

PROBE_NOT_FOUND = -1
NOT_MEASURED = 2000
RIPEATLAS_NO_RTT = -1
INVALID_LTS = -1
MAX_LTS = 180

LOG_LVL = logging.DEBUG
LOGFILE = "creation.log"
RES_LOGFILE = "results.log"

PARAMS_FILE = "input_data/measure_parameters.json"
PROBES_INPUT = "input_data/probes.csv"

MEASURES = {
    'rtt': "src.overlay_model.measure.RTTMeasure",
}  # to add other types of measures (like Ping), childs of Measure

# default measure parameters
DEF_AF = 4
DEF_MEASURE_TYPE = MEASURES['rtt']
DEF_N_PROBES = 2
DEF_N_PACKETS = 1
DEF_MEASURE_INTERVAL = 60  # seconds
DEF_PACKET_INTERVAL = 1000  # milliseconds
DEF_RANDOM = False

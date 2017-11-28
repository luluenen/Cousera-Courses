# MesuresOverlayRipeAtlas
#
# Copyright (C) 2016 Florencia ALVAREZ ETCHEVERRY
# <florencia.alvarezetcheverry@telecom-bretagne.eu>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, version 2.

import json


class Node:
    """
    A node of the Graph. Represents a probe analysed.

    Attributes:
        id          (int): Local identification of the Node (read from file)
        probe_id    (int): Number of Atlas probe
        ip_address (string): IP adress of the probe. Format '0.0.0.0'
    """
    def __init__(self, n_id, probe_id=None, address=None):
        self.id = n_id
        self.probe_id = probe_id
        self.ip_address = address

    def __repr__(self):
        dic = {
            'id': self.id,
            'probe_id': self.probe_id,
            'ip_address': self.ip_address
        }
        s = json.dumps(dic, separators=(',', ':'), sort_keys=True)
        return s
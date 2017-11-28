# MesuresOverlayRipeAtlas
#
# Copyright (C) 2016 Florencia ALVAREZ ETCHEVERRY
# <florencia.alvarezetcheverry@telecom-bretagne.eu>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, version 2.


class Loader(object):

    def load_probe_nodes(self, nb_probes, choose_random=False):
        raise NotImplementedError

    def load_measurement(self, file):
        raise NotImplementedError

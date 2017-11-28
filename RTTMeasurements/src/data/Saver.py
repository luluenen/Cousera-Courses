# MesuresOverlayRipeAtlas
#
# Copyright (C) 2016 Florencia ALVAREZ ETCHEVERRY
# <florencia.alvarezetcheverry@telecom-bretagne.eu>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, version 2.


class Saver(object):

    def save_measures(self, graph, params):
        raise NotImplementedError

    def save_msm_launch(self, time, nodes, msm_ids):
        raise NotImplementedError
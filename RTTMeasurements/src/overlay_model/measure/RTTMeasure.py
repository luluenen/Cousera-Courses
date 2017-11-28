# MesuresOverlayRipeAtlas
#
# Copyright (C) 2016 Florencia ALVAREZ ETCHEVERRY
# <florencia.alvarezetcheverry@telecom-bretagne.eu>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, version 2.

import logging

from ripe.atlas.cousteau import (Ping, AtlasSource, AtlasCreateRequest)

from src.common import settings as conf
from src.common.exceptions import MeasureNotCreated
from src.overlay_model.measure.Measure import Measure


class RTTMeasure(Measure):

    def __init__(self, nodes, params):
        Measure.__init__(self, nodes, params)
        try:
            self.parameters['packets'] = int(params['packets'])
        except (KeyError, ValueError) as e:
            self.parameters['packets'] = conf.DEF_N_PACKETS
            logging.error("%s. Using default num of packets: %s.",
                          e, conf.DEF_N_PACKETS)
        try:
            self.parameters['packet_interval'] = int(params['packet_interval'])
        except (KeyError, ValueError) as e:
            self.parameters['packet_interval'] = conf.DEF_PACKET_INTERVAL
            logging.error("%s. Using default packet_interval: %s.",
                          e, conf.DEF_PACKET_INTERVAL)
        logging.info("Ping parameters successfully loaded.")

    def _make_measure(self, src_list, target_probe):
        """
        Makes a Ping measure between a list of probes to one target probe.
        (The list has all the higher-id nodes of the target)

        @param src_list: List of source probes
        @type: List of <Node>

        @param target_probe: Destination probe
        @type target_probe: Node

        @return: Measurement id
        @rtype: int
        """

        probe_id_src_list = [str(probe.probe_id) for probe in src_list]
        id_src_list = [probe.id for probe in src_list]
        nb_probes = len(src_list)
        src_values = ",".join(probe_id_src_list)

        # Ping object with the measurment parameters
        ping = Ping(
                af=self.parameters['af'],
                packets=self.parameters['packets'],
                target=target_probe.ip_address,
                description="Measure to Probe {} from {}".format(
                    target_probe.id,
                    str(id_src_list).strip('[]')),
                interval=self.parameters['interval'],
                packet_interval=self.parameters['packet_interval']
                )

        source = AtlasSource(
                type="probes",
                value=src_values,
                requested=nb_probes
                )

        if self.parameters['is_oneoff']:
            atlas_request = AtlasCreateRequest(
                            key=self._atlas_create_key,
                            measurements=[ping],
                            sources=[source],
                            is_oneoff=True)
            logging.info("Creating one-off measurement request targeting probe "
                         "%s.", target_probe)
        else:
            # periodic measurement
            atlas_request = AtlasCreateRequest(
                            key=self._atlas_create_key,
                            measurements=[ping],
                            sources=[source],
                            is_oneoff=False,
                            start_time=self.parameters['start'],
                            stop_time=self.parameters['end'])
            logging.info("Creating periodic measurement request to probe %s.",
                         target_probe)

        (is_success, response) = atlas_request.create()

        if not is_success:
            logging.error("Couldn't create measurement to probe %s."
                          " Response: %s", target_probe, response)

            raise MeasureNotCreated

        id_result = response['measurements'][0]
        logging.info("Measurement request done to probe %s with id: %s.",
                     target_probe, id_result)

        return id_result

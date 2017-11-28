# MesuresOverlayRipeAtlas
#
# Copyright (C) 2016 Florencia ALVAREZ ETCHEVERRY
# <florencia.alvarezetcheverry@telecom-bretagne.eu>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, version 2.

"""
Script to retrieve one specific dataset.
"""
import json

import src.common.settings as conf
from ripe.atlas.cousteau import AtlasResultsRequest
from ripe.atlas.cousteau import Measurement

from src.data.csv.CSVLoader import CSVLoader
from src.data.csv.CSVSaver import CSVSaver
from src.overlay_model.HistoricalGraph import HistoricalGraph
from src.overlay_model.Node import Node

loader = CSVLoader("../../30probes.csv")
nodes_str, ids_str = loader.load_measurement(
    "./output_data/20160808_161300/measurement.csv")

nodes_strp = nodes_str.replace(" ", "")
nodes_list = json.loads(nodes_strp)
nodes = []
for dic in nodes_list:
    node = Node(n_id=dic['id'],
                probe_id=dic['probe_id'],
                address=dic['ip_address'])
    nodes.append(node)
ids = [int(s) for s in ids_str.split(',')]

m = Measurement(id=ids[0])
hist_graph = HistoricalGraph(nodes, m.start_time, m.stop_time, m.interval)

for msm_id in ids:
    success, results = AtlasResultsRequest(msm_id=msm_id).create()

    if not success:
        print("Error fetching results for {0}. {1}".format(msm_id, results))
    else:
        print("Successfully retrieved {} results.".format(len(results)))

        for result in results:
            if int(result['lts']) == -1 or int(result['lts']) > 180:
                print("Value not considered, probe out of sync. "
                      "Probe id: {}, target addr: {}, lts: {}, rtt: {}"
                      .format(result['prb_id'],
                              result['dst_addr'],
                              result['lts'],
                              result['avg']))
                continue
            rtt = float(result['avg'])
            if rtt == conf.RIPEATLAS_NO_RTT:
                rtt = conf.NOT_MEASURED
            id_probe_src = result['prb_id']
            target_addr = result['dst_addr']

            id_src = hist_graph.get_id_by_probe(id_probe_src)
            id_trg = hist_graph.get_id_by_address(target_addr)

            hist_graph[id_src, id_trg] = (rtt, result['timestamp'])

graphs = hist_graph.get_all_graphs()

csv_saver = CSVSaver()
c = 0
for graph in graphs:
    csv_saver.save_measures(graph, "./output_data/20160808_161300")
    c += 1

print("Finished {} measures".format(c))

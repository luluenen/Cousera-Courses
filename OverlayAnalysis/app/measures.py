import json
import os
from app import app


class Measure():
    measures_info = []

    def load_measure_list(self):
        root = app.config['DATA_ROOT']
        measures = [item for item in os.listdir(root)
                    if os.path.isdir(os.path.join(root, item))]
        for m in measures:
            with open(root + m + '/input_parameters.json') as params_f:
                measure = json.load(params_f)
                measure['creation_time'] = m
                if 'net' not in measure:
                    measure['net'] = "Ripe Atlas"
                self.measures_info.append(measure)

    def load_msm_creation(self, index):
        """
        Loads nodes info and measurements ids from the msm requested (index of
        list) and sets it to 'more' key in msm's dict.
        :param index: Index of the measurement in the list measures_info.
        :return: -
        """
        file = app.config['DATA_ROOT'] + self.measures_info[index][
            'creation_time'] + "/measurement.csv"

        with open(file, 'r') as msm_file:
            nodes_str = msm_file.readline()
            msm_ids_str = msm_file.readline()

        nodes = nodes_str.replace(" ", "").encode('utf-8')
        nodes_list = json.loads(nodes)
        msm_ids = [int(s) for s in msm_ids_str.split(',')]
        self.measures_info[index]['more'] = [nodes_list, msm_ids]

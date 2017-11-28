# coding:utf-8
import os
import sys
import shutil
import argparse as ap
from Tkinter import *

from Interface import Interface
from collections import OrderedDict
from operator import itemgetter
from visu import MyWindow
from gi.repository import Gtk
from graph_tool.all import *

path = os.path.abspath(os.path.join(os.path.dirname(__file__), './node/'))
if not path in sys.path:
    sys.path.insert(1, path)

path = os.path.abspath(os.path.join(os.path.dirname(__file__), './algo/'))
if not path in sys.path:
    sys.path.insert(1, path)

path = os.path.abspath(os.path.join(os.path.dirname(__file__), './measure/'))
if not path in sys.path:
    sys.path.insert(1, path)
del path
import node
import floyd_WarshallAlgo
from AtlasMeasure import AtlasMeasure
import datetime

"""
Controller: intergration of Algo, Measure and Visu
"""


class Controller:
    def __init__(self, nb_probes):
        self.measure = AtlasMeasure()
        self.data = dict()
        self.algo = floyd_WarshallAlgo.Floyd_WarshallAlgo()
        self.nb_probes = nb_probes

    def getData(self):
        import csv

        self.data = dict()
        with open("%s" % self.measure.measureFile, "r") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",")
            spamreader.next()
            for row in spamreader:
                if row[0] != "" and int(row[0]) < self.nb_probes + 1:
                    self.data[row[0]] = []
                    for i in row[1:self.nb_probes + 1]:
                        if i != "":
                            self.data[row[0]].append(float(i))
                        else:
                            self.data[row[0]].append(2000)
        return

    def node_dict_generator(self):
        nodes = dict()
        for key, values in self.data.items():
            anode = node.Node()
            anode.connections = dict()
            anode.ip_address = self.measure.getProbeAddress(self.measure.getProbeId(int(key)))
            for i in range(len(values)):
                if values[i] != 0:
                    anode.connections['%d' % (i + 1)] = values[i]
            nodes[key] = anode

        self.data = nodes


def output_log_file(data):
    f = open("log", "a")
    log = (datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y") + "\n")
    indexes = data.keys()

    for i in indexes:
        for j in indexes:
            if len(data[i].routingPath[j].path) > 2:
                print i, j , data[i].routingPath[j].path
                log += (
                    i + "-" + j + " : " + str(data[i].routingPath[j].path) + "\n")
    log +="\n"
    f.write(log)
    f.close()


def main(*args):
    # We suppress the list of probes case for now
    visu = args[1]
    if not args:
        nb_probes = 10
    else:
        nb_probes = int(args[0])
        c = Controller(nb_probes)
        if len(args)==3 and args[2] is not None: # if there is a file
            filename = args[2]
            shutil.copyfile(filename,"./data/measureFile.csv")
        else:
            c.measure.measureGraph(c.nb_probes)
        c.getData()
        c.node_dict_generator()
        c.algo.findRoutingPath(c.data)
        output_log_file(c.data)
        if visu:
            visualisation = MyWindow(c.data)
            visualisation.show_all()
            Gtk.main()
    """else:
        probes = [int(i) for i in args[0].split(",")]
        nb_probes = len(probes)
        c = Controller(nb_probes)
        c.measure.makeLinks(probes, 50)"""


if __name__ == "__main__":
    parser = ap.ArgumentParser(description="Argument to define the probes used")
    parser.add_argument('integer', type=int, nargs="?",
                        help="integer to define how many prob to use")
    parser.add_argument('--p', dest='probes', default=[], nargs="*",
                        help='define a probe list for the measurement (default: empty list, will use stored probe list)')
    parser.add_argument('--no-visu', action='store_false', dest='visu', default=True,
                        help='disable visu, see the results in the log file')
    parser.add_argument('--f', dest='measure', nargs='?', default='./data/measureFile.csv',
                        help='give a measure file to apply the algorithm')
    parser.set_defaults(visu=True)
    parser.set_defaults(measure=None)
    ns = parser.parse_args()
    if ns.probes:
        print ns.probes
    elif ns.integer and ns.measure == None:
        main(ns.integer, ns.visu)
    elif ns.integer and ns.measure:
	    main(ns.integer, ns.visu, ns.measure)
    else:
        # We start the interface
        fenetre = Tk()
        fenetre.wm_title("RIPE/Atlas Measure")
        interface = Interface(fenetre)
        interface.mainloop()
        interface.destroy()

        main(interface.argument, interface.visu, interface.filePath)

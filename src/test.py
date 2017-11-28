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
from ThreadAtlas import Thread_stats

thread = Thread_stats("ahah")
thread.start()

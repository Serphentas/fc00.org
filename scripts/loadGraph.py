import os
import sys
import inspect
import datetime as dt

from argparse import ArgumentParser

CWD = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(CWD))

import json
from fc00.graphData import insert_graph_data
from fc00 import APP

with APP.app_context():

    f = open('./graph.json', 'r')
    payload = json.load(f)

    insert_graph_data({'LOG': 'log.txt'}, payload, 'asd@example.com', '127.0.0.1', 2)

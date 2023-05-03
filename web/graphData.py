import json
from web.models import insert_graph
from web.graphModel import GraphEdge, GraphNode
import traceback
import time

def insert_graph_data(config, data, mail, ip, version):
    graph_data = data['data']

    log = '[%s] ip: %s, version: %d, mail: %r, nodes: %d, edges: %d' % (
        time.strftime('%Y-%m-%d %H:%M:%S'), ip,
        version, mail, len(graph_data['nodes']), len(graph_data['edges']))

    with open(config['LOG'], 'a') as f:
        f.write(log + '\n')

    if mail == 'your@email.here':
        return 'Please change email address in config.'

    if version != 2:
        return 'You are using outdated version of sendGraph script. Get new version from https://github.com/zielmicha/fc00.org/blob/master/scripts/sendGraph.py'

    nodes = dict()
    edges = []

    try:
        for n in graph_data['nodes']:
            try:
                node = GraphNode(n['ip'], version=n['version'])
                nodes[n['ip']] = node
            except Exception:
                print(e)

        for e in graph_data['edges']:
            try:
                edge = GraphEdge(nodes[e['a']], nodes[e['b']])
                edges.append(edge)
            except Exception as e:
                print(e)
    except Exception:
        return 'Invalid JSON nodes'

    print("Accepted %d nodes and %d links." % (len(nodes), len(edges)))

    if len(nodes) == 0 or len(edges) == 0:
        return 'No valid nodes or edges'

    uploaded_by = ip

    insert_graph(nodes, edges, uploaded_by)

    return None

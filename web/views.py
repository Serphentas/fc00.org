from flask import render_template, request

from web import APP
from web.models import Node, Edge
from web.graphData import insert_graph_data
from web.graphPlotter import position_nodes, get_graph_json

GRAPH_TIME_LIMIT = 60*60*3

def get_ip():
        try:
            ip = request.headers[APP.config['REAL_IP_HEADER']]
        except KeyError:
            ip = None
        return ip

@APP.context_processor
def add_ip():
        return dict(ip=get_ip())

@APP.route('/')
@APP.route('/network')
def page_network():
    return render_template('network.html', page='network')

@APP.route('/network/graph')
def network_graph():
    # logic used to be once on startup, wrote to static/graph.json
    nodes = Node.get_nodes(GRAPH_TIME_LIMIT)
    edges = Edge.get_edges(60*60*24*7, nodes)
    print('%d nodes, %d edges' % (len(nodes), len(edges)))

    return get_graph_json(
        position_nodes(nodes, edges)
    )

@APP.route('/about')
def page_about():
    return render_template('about.html', page='about')

@APP.route('/sendGraph', methods=['POST'])
def page_sendGraph():
    print("Receiving graph from %s" % (request.remote_addr))

    data = request.form['data']
    mail = request.form.get('mail', 'none')
    version = int(request.form.get('version', '1'))
    ret = insert_graph_data(ip=get_ip(), config=APP.config, data=data, mail=mail, version=version)

    if ret == None:
        return 'OK'
    else:
        return 'Error: %s' % ret

@APP.route('/js-licenses')
def page_js_licenses():
    return render_template('js-licenses.html', page='js-licenses')

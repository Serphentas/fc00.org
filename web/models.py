import time

from web import DB
from web.graphModel import GraphEdge, GraphNode
from web.utils import valid_cjdns_ip, valid_cjdns_version


class Node(DB.Model):
    __tablename__ = 'nodes'

    ip = DB.Column(
        DB.String,
        primary_key=True
    )
    label = DB.Column(DB.String)
    version = DB.Column(DB.Integer)
    first_seen = DB.Column(DB.DateTime)
    last_seen = DB.Column(DB.DateTime)

    def __init__(self, ip, label, version, first_seen, last_seen):
        if not valid_cjdns_ip(ip):
            raise ValueError('Invalid IP address')

        if not valid_cjdns_version(version):
            raise ValueError('Invalid version')

        self.ip = ip
        self.label = label or ip[-4:]
        self.version = version
        self.first_seen = first_seen
        self.last_seen = last_seen

    def __lt__(self, that):
        return self.ip < that.ip

    def __eq__(self, that):
        return self.ip == that.ip

    def __repr__(self):
        return 'Node(ip="{}", version={}, label="{}")' % (
            self.ip,
            self.version,
            self.label
        )

    @classmethod
    def get_nodes(cls, time_limit):
        since = int(time.time() - time_limit)
        db_nodes = cls.query.filter(cls.last_seen > since).all()

        return {x.ip: GraphNode(x.ip, x.version, x.label) for x in db_nodes}

    @classmethod
    def insert(cls, node):
        now = int(time.time())

        db_node = cls.query.filter_by(ip=node.ip).first()
        if db_node:
            db_node.label = node.label or ip[-4:]
            db_node.version = node.version
            db_node.last_seen = now
        else:
            db_node = Node(
                node.ip,
                node.label,
                node.version,
                now, now,
            )

        DB.session.add(db_node)
        DB.session.commit()

class Edge(DB.Model):
    __tablename__ = 'edges'

    a = DB.Column(
        DB.String,
        primary_key=True
    )
    b = DB.Column(
        DB.String,
        primary_key=True
    )
    first_seen = DB.Column(DB.DateTime)
    last_seen = DB.Column(DB.DateTime)
    uploaded_by = DB.Column(DB.String)

    def __init__(self, a, b, first_seen, last_seen, uploaded_by):
        self.a, self.b = sorted([a, b])
        self.first_seen = first_seen
        self.last_seen = last_seen
        self.uploaded_by = uploaded_by

    def __eq__(self, that):
        return self.a.ip == that.a.ip and self.b.ip == that.b.ip

    def __repr__(self):
        return 'Edge(a.ip="{}", b.ip="{}")'.format(
            self.a.ip,
            self.b.ip
        )

    @classmethod
    def get_edges(cls, time_limit, nodes):
        since = int(time.time() - time_limit)
        db_edges = cls.query.filter(cls.last_seen > since).all()

        edges = []
        for e in db_edges:
            try:
                edges.append(GraphEdge(nodes[e['a']], nodes[e['b']]))
            except KeyError:
                pass

        return edges

    @classmethod
    def insert(cls, edge, uploaded_by):
        now = int(time.time())

        db_edge = Edge.query.filter_by(a=edge.a, b=edge.b).first()
        if db_edge:
            db_node.last_seen = now
        else:
            db_edge = Edge(
                edge.a, edge.b,
                now. now,
                edge.uploaded_by
            )

        DB.session.add(db_edge)
        DB.session.commit()

def insert_graph(self, nodes, edges, uploaded_by):
    for n in nodes.itervalues():
        Node.insert(n)

    for e in edges:
        Edge.insert(e, uploaded_by)

def get_graph(self, time_limit):
    nodes = Node.get_nodes(time_limit)
    edges = Edge.get_edges(nodes, time_limit)
    return (nodes, edges)

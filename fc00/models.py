from fc00 import DB
from fc00.graphModel import GraphEdge, GraphNode
from fc00.utils import valid_cjdns_ip, valid_cjdns_version, now

class Node(DB.Model):
    __tablename__ = 'nodes'

    ip = DB.Column(
        DB.String,
        primary_key=True
    )
    label = DB.Column(DB.String)
    version = DB.Column(DB.Integer)
    first_seen = DB.Column(DB.Time)
    last_seen = DB.Column(DB.Time)

    def __init__(self, ip, label, version):
        if not valid_cjdns_ip(ip):
            raise ValueError('Invalid IP address')

        if not valid_cjdns_version(version):
            raise ValueError('Invalid version')

        timestamp = now().time()

        self.ip = ip
        self.label = label or ip[-4:]
        self.version = version
        self.first_seen = timestamp
        self.last_seen = timestamp

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
        db_nodes = cls.query.filter(
            cls.last_seen > (now().timestamp() - time_limit)
        ).all()

        return {x.ip: GraphNode(x.ip, x.version, x.label) for x in db_nodes}

    @classmethod
    def insert(cls, node):
        db_node = cls.query.filter_by(ip=node.ip).first()
        if db_node:
            db_node.label = node.label or ip[-4:]
            db_node.version = node.version
            db_node.last_seen = now().time()
        else:
            db_node = Node(
                node.ip,
                node.label,
                node.version,
            )

        DB.session.add(db_node)
        DB.session.commit()

class Edge(DB.Model):
    __tablename__ = 'edges'

    a = DB.Column(
        DB.String,
        DB.ForeignKey('nodes.ip'),
        primary_key=True,
    )
    b = DB.Column(
        DB.String,
        DB.ForeignKey('nodes.ip'),
        primary_key=True
    )
    first_seen = DB.Column(DB.Time)
    last_seen = DB.Column(DB.Time)
    uploaded_by = DB.Column(DB.String)

    def __init__(self, a, b, uploaded_by):
        self.a, self.b = a, b
        self.first_seen = self.last_seen = now().time()
        self.uploaded_by = uploaded_by

    def __eq__(self, that):
        return self.a == that.a and self.b == that.b

    def __repr__(self):
        return 'Edge(a="{}", b="{}")'.format(
            self.a,
            self.b
        )

    @classmethod
    def get_edges(cls, time_limit, nodes):
        db_edges = cls.query.filter(
            cls.last_seen > (now().timestamp() - time_limit),
        ).all()

        edges = []
        for e in db_edges:
            try:
                edges.append(GraphEdge(nodes[e.a], nodes[e.b]))
            except KeyError as e:
                print(e)

        return edges

    @classmethod
    def insert(cls, edge, uploaded_by):
        db_edge = Edge.query.filter_by(a=edge.a.ip, b=edge.b.ip).first()
        if db_edge:
            db_edge.last_seen = now().time()
        else:
            db_edge = Edge(
                edge.a.ip, edge.b.ip,
                uploaded_by
            )

        DB.session.add(db_edge)
        DB.session.commit()

def insert_graph(nodes, edges, uploaded_by):
    for ip in nodes:
        Node.insert(nodes[ip])

    for e in edges:
        Edge.insert(e, uploaded_by)

def get_graph(time_limit):
    nodes = Node.get_nodes(time_limit)
    edges = Edge.get_edges(nodes, time_limit)
    return (nodes, edges)

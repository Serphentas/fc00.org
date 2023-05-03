from fc00.utils import valid_cjdns_ip, valid_cjdns_version

class GraphNode:
    def __init__(self, ip, version=None, label=None):
        self.ip = ip
        self.version = version
        self.label = ip[-4:] if label == None else label

    def __lt__(self, that):
        return self.ip < that.ip

    def __repr__(self):
        return 'Node(ip="{}", version={}, label="{}")'.format(
            self.ip,
            self.version,
            self.label
        )

class GraphEdge:
    def __init__(self, a, b):
        self.a, self.b = sorted([a, b])

    def __eq__(self, that):
        return self.a.ip == that.a.ip and self.b.ip == that.b.ip

    def __repr__(self):
        return 'Edge(a="{}", b="{}")'.format(
            self.a.ip,
            self.b.ip
        )

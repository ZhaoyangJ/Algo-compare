from collections import defaultdict

class Graph(object):

    def __init__(self, connection, directed = False):
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_connections(connection)

    def add_connection(self, connection):
        for node1, node2 in connection:
            self.add(node1, node2)

    def add(self, node1, node2):
        self._graph[node1].add(node2)
        if not self._directed:
            self._graph[node2].add(node1)

    def remove(self, node):
        for n, cxns in self._graph.iteritems():
            try:
                cxn.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        return node1 in self._graph and node2 in self._graph[node1]

    def find_path(self, node1, node2, path=[]):
        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self._graph:
            return None
        for node in self._graph[node1]:
            if node not in path:
                new_path = self.find_path(node, node2, path)
                if new_path:
                    return new_path
        return None

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))

from collections import defaultdict
from subprocess import call

class GraphNodeFactory:
    def __init__(self):
        self.node_map = {}

    def get_node(self, v):
        key = self.get_key(v)

        if key not in self.node_map:
            self.node_map[key] = GraphNode(v)

        return self.node_map[key]

    def get_key(self, v):
        return str(v)

node_factory = GraphNodeFactory()


class GraphNode:
    def __init__(self, vertex):
        self.vertex = vertex
        # self.edges = []

    def get_intersect_edge(self):
        return self.vertex.get_intersect_edge()

    # def add_edge(self, edge):
    #     self.edges.append(edge)

    def get_vertex(self):
        return self.vertex

    def get_distance(self, node):
        return self.vertex.get_distance(node.get_vertex())

    def __str__(self):
        return str(self.vertex)


class GraphEdge:
    def __init__(self, segment, is_isoline=False):
        self.segment = segment
        self.is_isoline = is_isoline

    def get_segment(self):
        return self.segment

    def isoline(self):
        return self.is_isoline

    def __str__(self):
        return 'isoline' if self.isoline() else 'border'


class Graph:
    def __init__(self):
        self.graph = defaultdict(list) # node -> [(edge, node), ...]

    def add_edge(self, src_node, dst_node, edge):
        self.graph[src_node].append((edge, dst_node))

    def get_edge(self, node):
        for edge, _ in self.graph[node]:
            if edge.isoline():
                return edge
        edge, _ = self.graph[node][0]
        return edge

    def remove_edge(self, node, edge):
        for _edge, dst_node in self.graph[node]:
            if edge == _edge:
                self.graph[node].remove((_edge, dst_node))

    def get_not_isoline_edge(self, node):
        for edge, dst_node in self.graph[node]:
            if not edge.isoline():
                return edge

    def get_next_node(self, node, edge):
        for _edge, dst_node in self.graph[node]:
            if edge == _edge:
                return dst_node

    def get_isocontour_segment(self, start_node):
        isocontour_segment = []
        edge = self.get_edge(start_node)
        node = start_node
        h = []

        while True:
            prev_node = node
            if not edge.isoline(): #border
                isocontour_segment.append(node.get_vertex())
                node = self.get_next_node(node, edge)
                self.remove_edge(prev_node, edge)
                if node == start_node:
                    break
                edge = self.get_edge(node)
            else:
                isocontour_segment.append(node.get_vertex())
                h.append(node.get_vertex().z())
                isocontour_segment.extend(edge.get_segment())
                node = self.get_next_node(node, edge)
                self.remove_edge(prev_node, edge)
                edge = self.get_not_isoline_edge(node)
            if node == start_node:
                break

        return (h, isocontour_segment)

    def clear(self):
        del_nodes = [node for node in self.graph if self.graph[node] == []]
        for node in del_nodes:
            del self.graph[node]

    def get_node(self):
        for node in self.graph:
            if self.graph[node] != []:
                return node
        return None

    def print_it(self, filename, scale=1100):
        # dot -Kneato -n -Tpdf out.dot > out.pdf
        with open(filename, 'w') as out:
            out.write('digraph g {\n')
            node_map = {}
            i = 1
            for node in self.graph:
                x = node.get_vertex().x()*scale
                y = node.get_vertex().y()*scale
                out.write('\tn%s [label="%s", pos="%s,%s"];\n' % (i, node, x, y))
                node_map[node] = 'n%s' % i
                i += 1
            for node in self.graph:
                for edge, node_next in self.graph[node]:
                    if edge.isoline():
                        edge_label="isoline"
                    else:
                        edge_label="border"
                    out.write('\t%s -> %s [label="%s"];\n' % (node_map[node], node_map[node_next], edge_label))
            out.write('}')
        pdf_name = filename + '.pdf'
        call(['dot', '-Kneato', '-n', '-Tpdf', '-o', pdf_name, filename])


from collections import defaultdict
from itertools import cycle, chain

from isoline import get_isoline, print_isoline
from obj_io import read_obj_file
import matplotlib.pyplot as plt


obj_filename='examples/landscape_mini_new.obj'
start = 0
end = 0.24
step = 0.02


_, triangles = read_obj_file(obj_filename)

h_range = []
while start < end:
    h_range.append(start)
    start += step
h_range.append(end)

isocontours = defaultdict(list)
segments_not_closed = []

for h in h_range:
    isoline = get_isoline(h, triangles)
    for segment in isoline:
        if segment['closed']:
            isocontours[h].append(segment['vertices'])
        else:
            segments_not_closed.append(segment['vertices'])


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
        self.edges = []

    def get_intersect_edge(self):
        return self.vertex.get_intersect_edge()

    def add_edge(self, edge):
        self.edges.append(edge)

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


class Graph:
    def __init__(self):
        self.graph = defaultdict(list) # node -> [(edge, node), ...]

    def add_edge(self, src_node, dst_node, edge):
        self.graph[src_node].append((edge, dst_node))

    def get_edge(self, node):
        edge, _ = self.graph[node][0]
        return edge

    def remove_edge(self, node, edge):
        for _edge, dst_node in self.graph[node]:
            if edge == _edge:
                self.graph[node].remove((_edge, dst_node))

    def get_not_isoline_edge(self, node):
        for edge, dst_node in self.graph[node]:
            if edge.isoline():
                return edge

    def get_next_node(self, node, edge):
        for _edge, dst_node in self.graph[node]:
            if edge == _edge:
                return dst_node

    def get_isocontour_segment(self, start_node):
        print 'start'

        isocontour_segment = []
        print 'start_node', start_node
        print 'start_node_edges', map(lambda (x,y): str(x)+' '+str(y), self.graph[start_node])
        edge = self.get_edge(start_node)
        node = start_node
        h = None

        while True:
            if not edge.isoline():
                isocontour_segment.append(node.get_vertex())
                node = self.get_next_node(node, edge)
                self.remove_edge(node, edge)
                edge = self.get_edge(node)
            else:
                isocontour_segment.append(node.get_vertex())
                h = node.get_vertex().z()
                isocontour_segment.extend(edge.get_segment())
                node = self.get_next_node(node, edge)
                self.remove_edge(node, edge)
                edge = self.get_not_isoline_edge(node)
            if node == start_node:
                break

        print 'end'
        return (h, isocontour_segment)

    def clear(self):
        for node in self.graph:
            if self.graph[node] == []:
                del self.graph[node]

    def get_node(self):
        return self.graph.keys()[0]

    def print_it(self, filename):
        with open(filename, 'w') as out:
            out.write('digraph g {\n')
            node_map = {}
            i = 1
            for node in self.graph:
                out.write('\tn%s {%s}\n' % (i, node))
                node_map[node] = 'n%s' % i
                i += 1

            for node in self.graph:
                for edge, node_next in self.graph[node]:
                    out.write('\t%s -> %s\n' % (node_map[node], node_map[node_next]))


            out.write('}')





graph = Graph()

nodes_by_edge = defaultdict(list) #edge -> [node, ...]

for segment in segments_not_closed:
    node1 = node_factory.get_node(segment[0])
    node2 = node_factory.get_node(segment[-1])

    graph.add_edge(node1, node2, GraphEdge(segment[1:-1]))
    graph.add_edge(node2, node1, GraphEdge(segment[1:-1]))

    nodes_by_edge[node1.get_intersect_edge()].append(node1)
    nodes_by_edge[node2.get_intersect_edge()].append(node2)


border_edges = list(set(edge for edge in chain.from_iterable(triangle.get_edges() for triangle in triangles) if not edge.not_border()))

for edge in border_edges:
    print edge
    if edge in nodes_by_edge:
        v1, v2 = edge.get_ordered_vertices()
        node1 = node_factory.get_node(v1)
        node2 = node_factory.get_node(v2)
        
        prev_node = node1
        for node in sorted(nodes_by_edge[edge], key=lambda x: x.get_distance(node1)):
            graph.add_edge(prev_node, node, GraphEdge([]))
            prev_node = node

            print '\t', node, node.get_distance(node1)
        #print '\t', node2, node2.get_distance(node1)

        graph.add_edge(prev_node, node2, GraphEdge([]))
    else:
        v1, v2 = edge.get_ordered_vertices()
        node1 = node_factory.get_node(v1)
        node2 = node_factory.get_node(v2)
        
        graph.add_edge(node1, node2, GraphEdge([]))

# for node in graph.graph:
#     print node, graph.graph[node]

graph.print_it('out.dot')

# while graph.graph:
#     node = graph.get_node()
#     h, segment = graph.get_isocontour_segment(node)
#     print h, segment
#     isocontours[h].append(segment)
#     graph.clear()
#     print '---------'
#     break



# for edge in sorted(border_edges, key= lambda x: str(x)):
#     print edge
#print map(str, border_edges)
#print_isoline(isoline)



# color_generator = cycle('bgrcmk')

# for segment in segments_not_closed:
#     color = color_generator.next()

#     x = [vertex.x() for vertex in segment]
#     y = [vertex.y() for vertex in segment]

#     plt.plot(x, y, color=color)

# plt.show()


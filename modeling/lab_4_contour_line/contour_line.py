from collections import defaultdict
from itertools import cycle, chain

from geometry import Vertex
from graph import Graph, GraphEdge, node_factory
from isoline import get_isoline, print_isoline
from obj_io import read_obj_file
import matplotlib.pyplot as plt


obj_filename='examples/landscape_big/landscape.obj'
start = 0
end = 4.25
step = 0.25 #0.05, 0.1
color_interval = [0.3, 0.9]

plt.axis('equal')

_, triangles = read_obj_file(obj_filename)

h_range = []
while start <= end:
    h_range.append(start)
    start += step
#print h_range

isocontours = defaultdict(list)
segments_not_closed = []

for h in h_range:
    isoline = get_isoline(h, triangles)
    #print_isoline(isoline)
    for segment in isoline:
        if segment['closed']:
            isocontours[h].append(segment['vertices'])
        else:
            segments_not_closed.append(segment['vertices'])

#plt.show()

graph = Graph()

nodes_by_edge = defaultdict(list) #edge -> [node, ...]

for segment in segments_not_closed:
    node1 = node_factory.get_node(segment[0])
    node2 = node_factory.get_node(segment[-1])

    graph.add_edge(node1, node2, GraphEdge(segment[1:-1], True))
    graph.add_edge(node2, node1, GraphEdge(list(reversed(segment[1:-1])), True))

    nodes_by_edge[node1.get_intersect_edge()].append(node1)
    nodes_by_edge[node2.get_intersect_edge()].append(node2)


border_edges = list(set(edge for edge in chain.from_iterable(triangle.get_edges() for triangle in triangles) if not edge.not_border()))

for edge in border_edges:
    if edge in nodes_by_edge:
        v1, v2 = edge.get_ordered_vertices()
        node1 = node_factory.get_node(v1)
        node2 = node_factory.get_node(v2)
        
        prev_node = node1
        for node in sorted(nodes_by_edge[edge], key=lambda x: x.get_distance(node1)):
            graph.add_edge(prev_node, node, GraphEdge([]))
            prev_node = node

        graph.add_edge(prev_node, node2, GraphEdge([]))
    else:
        v1, v2 = edge.get_ordered_vertices()

        node1 = node_factory.get_node(v1)
        node2 = node_factory.get_node(v2)
        
        graph.add_edge(node1, node2, GraphEdge([]))


#graph.print_it('out.dot')


node = graph.get_node()
while node:
    h, segment = graph.get_isocontour_segment(node)
    # x = [vertex.x() for vertex in segment]
    # y = [vertex.y() for vertex in segment]
    # x.append(x[0])
    # y.append(y[0])

    # plt.plot(x, y, color='k')
    # plt.show()

    if h:
        isocontours[max(h)].append(segment)
    else:
        isocontours[0].append(segment)
    node = graph.get_node()

delta_color = (color_interval[1] - color_interval[0])/len(h_range)
color = color_interval[1]

#h_range = h_range[:6]

for h in h_range:
    print color
    for segment in isocontours[h]:
        x = [vertex.x() for vertex in segment]
        y = [vertex.y() for vertex in segment]
        x.append(x[0])
        y.append(y[0])

        plt.fill(x, y, color=str(color))
        plt.plot(x, y, color='k')

    color -= delta_color
    plt.show()
    

# color = color_interval[1]
# for h in h_range:
#     for segment in isocontours[h]:
#         x = [vertex.x() for vertex in segment]
#         y = [vertex.y() for vertex in segment]
#         x.append(x[0])
#         y.append(y[0])

#         plt.fill(x, y, color=str(color))
#         #plt.plot(x, y, color='k')
#     color -= delta_color
# plt.show()
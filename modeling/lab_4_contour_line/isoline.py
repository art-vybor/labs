import matplotlib.pyplot as plt
from itertools import cycle


def filter_triangles(h, triangles, delta_h=0.00001):

    triangles_marked = []
    while True:
        triangles_marked = filter(lambda x: x.isoline_exist(h), triangles)

        if any(triangle.edge_in_isoline(h) for triangle in triangles_marked):
            h -= delta_h
        else:
            break
    return h, triangles_marked


def get_isoline_subsegment(h, edge, triangle, triangles_marked):
    start_vertex = edge.get_vertex_of_isoline_intersection(h)
    subsegment = [start_vertex]

    start_edge = edge
    while edge.not_border():
        adjacent_triangle = edge.get_adjacent_triangle(triangle)
        if adjacent_triangle not in triangles_marked:
            break

        del triangles_marked[adjacent_triangle]

        edge = adjacent_triangle.get_other_intersection_edge(h, edge)
        triangle = adjacent_triangle
        
        subsegment.append(edge.get_vertex_of_isoline_intersection(h))
    return subsegment, edge
        


def get_isoline_segment(h, triangles_marked):
    triangle = triangles_marked.popitem()[0]

    edges = triangle.get_intersection_isoline_edges(h)
    
    subsegment_left, finish_edge = get_isoline_subsegment(h, edges[0], triangle, triangles_marked)

    if finish_edge != edges[1]:
        subsegment_right, _ = get_isoline_subsegment(h, edges[1], triangle, triangles_marked)
        return {'vertices': list(reversed(subsegment_left)) + subsegment_right, 'closed': False}
    else:
        return {'vertices': subsegment_left , 'closed': True}



def get_isoline(h, triangles):
    h, triangles = filter_triangles(h, triangles)

    triangles_marked = {triangle: 1 for triangle in triangles}

    isoline = []
    while triangles_marked:
        isoline_segment = get_isoline_segment(h, triangles_marked)
        isoline.append(isoline_segment)

    return isoline

color_generator = cycle('bgrcmk')

def print_isoline(isoline):    
    color = color_generator.next()
    for segment in isoline:
        x = [vertex.x() for vertex in segment['vertices']]
        y = [vertex.y() for vertex in segment['vertices']]

        if segment['closed']:
            x.append(x[0])
            y.append(y[0])

        plt.plot(x, y, color=color)

    #plt.plot(x, y)
    

from itertools import chain
from math import sqrt

class Vertex:
    def __init__(self, x, y, z, intersect_edge=None):
        self.coordinates = {'x': x, 'y': y, 'z': z}
        self.intersect_edge = intersect_edge
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_intersect_edge(self):
        return self.intersect_edge

    def x(self):
        return self.coordinates['x']

    def y(self):
        return self.coordinates['y']

    def z(self):
        return self.coordinates['z']

    def get_distance(self, v):
        return sqrt((self.x()-v.x())**2 + \
            (self.y()-v.y())**2 + \
            (self.z()-v.z())**2)

    def equal_to(self, v, eps=0.000001):
        if abs(self.x()-v.x()) < eps and \
            abs(self.y()-v.y()) < eps and \
            abs(self.z()-v.z()) < eps:
            return True
        return False

    def __str__(self):
        return '(%s, %s, %s)' % (self.coordinates['x'], self.coordinates['y'], self.coordinates['z'])


class EdgeFactory:
    def __init__(self):
        self.edge_map = {}

    def get_edge_by_vertex(self, v1, v2):
        key1 = self.get_key(v1, v2)
        key2 = self.get_key(v2, v1)

        if key2 in self.edge_map:
            return self.edge_map[key2]

        if key1 not in self.edge_map:
            self.edge_map[key1] = Edge([v1, v2])

        return self.edge_map[key1]

    def get_key(self, v1, v2):
        return str(v1)+str(v2)

edge_factory = EdgeFactory()


class Edge:
    def __init__(self, vertices):
        self.vertices = vertices
        self.triangles = []

        for vertex in vertices:
            vertex.add_edge(self)

    def get_vertices(self):
        return self.vertices

    def add_triangle(self, triangle):
        self.triangles.append(triangle)

    def intersect_isoline(self, h):
        return self.vertices[0].z() < h and h < self.vertices[1].z() or \
                self.vertices[1].z() < h and h < self.vertices[0].z()

    def get_ordered_vertices(self):
        edges = self.triangles[0].get_edges()
        another_edge = edges[0] if self != edges[0] else edges[1]
        v1, v2 = self.vertices
        v3, v4 = another_edge.get_vertices()
        if v1.equal_to(v3):
            v3 = v4

        x1, y1 = v1.x(), v1.x()
        x2, y2 = v2.x(), v2.x()
        x3, y3 = v3.x(), v3.x()

        D = (v3.x() - v1.x()) * (v2.y() - v1.y()) - (v3.y() - v1.y()) * (v2.x() - v1.x()) #http://www.cyberforum.ru/delphi/thread652199.html

        if D < 0: return [v2, v1]
        return [v1, v2]

    def get_vertex_of_isoline_intersection(self, h):
        vA = self.vertices[0]
        vB = self.vertices[1]
        d = (h-vA.z()) / (vB.z()-vA.z())
        x = d*(vB.x()-vA.x()) + vA.x()
        y = d*(vB.y()-vA.y()) + vA.y()
        return Vertex(x,y,h, self)

    def get_adjacent_triangle(self, triangle):
        if self.triangles[0] == triangle:
            return self.triangles[1]
        return self.triangles[0]

    def not_border(self):
        return len(self.triangles) > 1

    def __str__(self):
        return '[%s, %s]' % tuple(self.vertices)


class Triangle:
    def __init__(self, vertices):
        self.edges = [edge_factory.get_edge_by_vertex(vertices[0], vertices[1]), 
                      edge_factory.get_edge_by_vertex(vertices[1], vertices[2]), 
                      edge_factory.get_edge_by_vertex(vertices[2], vertices[0])]

        for edge in self.edges:
            edge.add_triangle(self)

    def get_vertices(self):
        return list(set(chain.from_iterable([edge.get_vertices() for edge in self.edges])))

    def isoline_exist(self, h):
        vertices_z = [vertex.z() for vertex in self.get_vertices()]
        return min(vertices_z) < h and h < max(vertices_z)

    def get_edges(self):
        return self.edges

    def edge_in_isoline(self, h):
        for edge in self.edges:
            if edge.get_vertices()[0] == h and edge.get_vertices()[1] == h:
                return True
        return False

    def get_intersection_isoline_edges(self, h):
        return filter(lambda x: x.intersect_isoline(h), self.edges)


    def get_other_intersection_edge(self, h, edge):
        edges = self.get_intersection_isoline_edges(h)
        if edges[0] == edge:
            return edges[1]
        return edges[0]

    def __str__(self):
        return '{%s, %s, %s}' % tuple(self.get_vertices())
import itertools

obj_filename='examples/landscape_mini.obj'
h = 0.8
delta_h = 0.00001

class Vertex:
    def __init__(self, x, y, z):
        self.coordinates = {'x': x, 'y': y, 'z': z}
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_z(self):
        return self.coordinates['z']

    def __str__(self):
        return '(%s, %s, %s)' % (self.coordinates['x'], self.coordinates['y'], self.coordinates['z'])


class Edge:
    def __init__(self, vertices):
        self.vertices = vertices
        self.triangles = []

        for vertex in vertices:
            vertex.add_edge(self)

    def get_vertices(self):
        return self.vertices

    def add_trianle(self, triangle):
        self.triangles.append(triangle)

    def __str__(self):
        return '[%s, %s]' % tuple(self.vertices)


class Triangle:
    def __init__(self, vertices):
        self.edges = [Edge([vertices[0], vertices[1]]), 
                      Edge([vertices[1], vertices[2]]), 
                      Edge([vertices[2], vertices[0]])]

        for edge in edges:
            edge.add_triangle(self)

    def get_vertices():
        return list(set(itertools.chain.from_iterable([edge.get_vertices() for edge in self.edges)))

    def isoline_exist(self, h):
        vertices_z = [vertex.get_z() for vertex in self.get_vertices()]
        return min(vertices_z) < h and h < max(vertices_z)

    def get_edges(self):
        return self.edges

    def edge_in_isoline(self, h):
        for edge in self.edges:
            if edge[0].get_vertices()[0] == h and edge[1].get_vertices()[1] == h:
                return True
        return False

    def __str__(self):
        return '{%s, %s, %s}' % tuple(self.get_vertices())


def read_obj_file(filename):
    vertices = {}
    triangles = []
    vertices_idx = 1
    with open(filename) as obj_file:
        for line in obj_file:
            if line:
                splitted_line = line.split()
                line_type, args = splitted_line[0], splitted_line[1:]
                
                if line_type == 'v': # vertex
                    x, y, z = map(float, args)
                    vertices[vertices_idx] = Vertex(x, y, z)
                    vertices_idx += 1
                elif line_type == 'f': # triagle
                    triangle_vertices = [vertices[int(arg.split('//')[0])] for arg in args] # get vertices by index
                    triangles.append(Triangle(triangle_vertices))

    return vertices, triangles


def get_isoline(h, vertices, triangles):
    isoline = []
        triangles_marked = []
        while True:
            triangles_marked = [triangle for triangle in triangles if triangle.isoline_exist(h)]

            if any(triangle.edge_in_isoline(h) for triangle in triangles_marked):
                h -= delta_h
            else:
                break

        for triangle in triangles_marked:
            triangle.get_segment_of_isoline()

            print triangle




vertices, triangles = read_obj_file(obj_filename)
get_isoline(h, vertices, triangles)
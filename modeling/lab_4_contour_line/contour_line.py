import itertools

obj_filename='examples/landscape_mini.obj'
delta_h = 0.00001

class Vertex:
    def __init__(self, x, y, z):
        self.coordinates = {'x': x, 'y': y, 'z': z}
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)

    def x(self):
        return self.coordinates['x']

    def y(self):
        return self.coordinates['y']

    def z(self):
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

    def add_triangle(self, triangle):
        self.triangles.append(triangle)

    def intersect_isoline(self, h):
        return self.vertices[0].z() < h and h < self.vertices[1].z() or \
                self.vertices[1].z() < h and h < self.vertices[0].z()

    def get_vertex_of_isoline_intersection(self, h):
        vA = self.vertices[0]
        vB = self.vertices[1]
        d = (h-vA.z()) / (vB.z()-vA.z())
        x = d*(vB.x()-vA.x()) + vA.x()
        y = d*(vB.y()-vA.y()) + vA.y()
        return Vertex(x,y,h)

    def get_adjacent_triangle(self, triangle):
        if self.triangles[0] == triangle:
            return self.triangle[1]
        return self.triangle[0]

    def not_border(self):
        return len(self.triangles) > 1

    def __str__(self):
        return '[%s, %s]' % tuple(self.vertices)


class Triangle:
    def __init__(self, vertices):
        self.edges = [Edge([vertices[0], vertices[1]]), 
                      Edge([vertices[1], vertices[2]]), 
                      Edge([vertices[2], vertices[0]])]

        for edge in self.edges:
            edge.add_triangle(self)

    def get_vertices(self):
        return list(set(itertools.chain.from_iterable([edge.get_vertices() for edge in self.edges])))

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


def filter_triangles(h, triangles):
    triangles_marked = []
    while True:
        triangles_marked = filter(lambda x: x.isoline_exist(h), triangles)

        if any(triangle.edge_in_isoline(h) for triangle in triangles_marked):
            h -= delta_h
        else:
            break
    return h, triangles_marked


def get_isoline_subsegment(h, edge, triangle, triangles_marked):
    subsegment = []
    print edge, edge.triangles
    while edge.not_border():
        adjacent_triangle = edge.get_adjacent_triangle(triangle)

        del triangles_marked[adjacent_triangle]

        edge = adjacent_triangle.get_other_intercetion_edge()

        subsegment.append(edge.get_vertex_of_isoline_intersection(h))
    return subsegment
        


def get_isoline_segment(h, triangles_marked):
    triangle = triangles_marked.popitem()[0]

    isoline_segment = []

    edges = triangle.get_intersection_isoline_edges(h)
    v0 = edges[0].get_vertex_of_isoline_intersection(h)
    v1 = edges[1].get_vertex_of_isoline_intersection(h)

    subsegment_left = get_isoline_subsegment(h, edges[0], triangle, triangles_marked)
    subsegment_right = get_isoline_subsegment(h, edges[1], triangle, triangles_marked)

    return list(reversed(subsegment_left)) + [v0, v1] + subsegment_right


def get_isoline(h, triangles):
    h, triangles = filter_triangles(h, triangles)

    triangles_marked = {triangle: 1 for triangle in triangles}

    isoline = []
    while triangles_marked:
        isoline_segment = get_isoline_segment(h, triangles_marked)

        isoline.append(isoline_segment)

    return isoline


vertices, triangles = read_obj_file(obj_filename)

isoline = get_isoline(0.8, triangles)
for segment in isoline:
    for vertex in segment:
        print vertex
    print '-----------------'

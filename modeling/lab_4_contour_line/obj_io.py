from geometry import Vertex, Triangle

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
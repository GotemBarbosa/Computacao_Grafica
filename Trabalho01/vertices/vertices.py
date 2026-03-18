import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_vertices_from_file(filename: str):
    path = os.path.join(BASE_DIR, filename)

    vertices = []
    with open(path, "r") as file:
        for line in file:

            line = line.strip()

            # ignora linhas vazias
            if line == '':
                continue

            parts = line.split()
            x, y, z = map(float, parts)

            vertices.append((x, y, z))

    return vertices 

def get_cube_vertices():
    return load_vertices_from_file("cube.vertices")

def get_semi_sphere_vertices():
    return load_vertices_from_file("semiesfera.vertices")

            

            
"""Utilities to load scene geometry from OBJ files."""


def load_model_from_file(filename):
    vertices = []
    texture_coords = []
    faces = []

    for line in open(filename, "r"):
        if line.startswith("#"):
            continue
        values = line.split()
        if not values:
            continue

        if values[0] == "v":
            vertices.append([float(values[1]), float(values[2]), float(values[3])])

        elif values[0] == "vt":
            texture_coords.append([float(values[1]), float(values[2])])

        elif values[0] == "f":
            face_v = []
            face_t = []
            for item in values[1:]:
                w = item.split("/")
                face_v.append(int(w[0]))
                face_t.append(int(w[1]) if len(w) > 1 and w[1] else 0)
            faces.append((face_v, face_t))

    return {"vertices": vertices, "texture": texture_coords, "faces": faces}


def _triangulate_indices(indices):
    tris = []
    for i in range(1, len(indices) - 1):
        tris.append([indices[0], indices[i], indices[i + 1]])
    return tris


def load_box_geometry(obj_path):
    model = load_model_from_file(obj_path)
    raw_vertices = []
    raw_texcoords = []

    for face_v, face_t in model["faces"]:
        tris_v = _triangulate_indices(face_v)
        tris_t = _triangulate_indices(face_t)

        for tri in tris_v:
            for vid in tri:
                raw_vertices.append(model["vertices"][vid - 1])

        for tri in tris_t:
            for tid in tri:
                raw_texcoords.append(model["texture"][tid - 1])

    return raw_vertices, raw_texcoords
def load_model_from_file(filename):
    vertices = []
    texture_coords = []
    normals = []
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
        elif values[0] == "vn":
            normals.append([float(values[1]), float(values[2]), float(values[3])])
        elif values[0] == "f":
            face_v = []
            face_t = []
            face_n = []
            for item in values[1:]:
                w = item.split("/")
                face_v.append(int(w[0]))
                face_t.append(int(w[1]) if len(w) > 1 and w[1] else 0)
                face_n.append(int(w[2]) if len(w) > 2 and w[2] else 0)
            faces.append((face_v, face_t, face_n))

    return {"vertices": vertices, "texture": texture_coords,
            "normals": normals, "faces": faces}


def _triangulate_indices(indices):
    tris = []
    for i in range(1, len(indices) - 1):
        tris.append([indices[0], indices[i], indices[i + 1]])
    return tris


def _face_normal(p0, p1, p2):
    # Normal geométrica de um triângulo (produto vetorial de duas arestas).
    # Usada como fallback quando o .obj não traz normais (vn).
    ux, uy, uz = p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]
    vx, vy, vz = p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2]
    nx = uy * vz - uz * vy
    ny = uz * vx - ux * vz
    nz = ux * vy - uy * vx
    length = (nx * nx + ny * ny + nz * nz) ** 0.5
    if length == 0.0:
        return [0.0, 1.0, 0.0]
    return [nx / length, ny / length, nz / length]


def load_obj_geometry(obj_path):
    model = load_model_from_file(obj_path)
    raw_vertices = []
    raw_texcoords = []
    raw_normals = []

    has_normals = len(model["normals"]) > 0

    for face_v, face_t, face_n in model["faces"]:
        tris_v = _triangulate_indices(face_v)
        tris_t = _triangulate_indices(face_t)
        tris_n = _triangulate_indices(face_n)

        for tri in tris_v:
            for vid in tri:
                raw_vertices.append(model["vertices"][vid - 1])

        for tri in tris_t:
            for tid in tri:
                raw_texcoords.append(model["texture"][tid - 1])

        # Normais: usa as do arquivo quando existem; caso contrário (ou se o
        # índice estiver ausente) calcula a normal geométrica da face.
        for tri_v, tri_n in zip(tris_v, tris_n):
            face_norm = None
            for vid, nid in zip(tri_v, tri_n):
                if has_normals and nid > 0:
                    raw_normals.append(model["normals"][nid - 1])
                else:
                    if face_norm is None:
                        p0 = model["vertices"][tri_v[0] - 1]
                        p1 = model["vertices"][tri_v[1] - 1]
                        p2 = model["vertices"][tri_v[2] - 1]
                        face_norm = _face_normal(p0, p1, p2)
                    raw_normals.append(face_norm)

    return raw_vertices, raw_texcoords, raw_normals

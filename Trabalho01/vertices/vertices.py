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

def normalize(vertices):
    # separa por eixo
    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    zs = [v[2] for v in vertices]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)

    # evita divisão por zero
    range_x = max_x - min_x if max_x != min_x else 1.0
    range_y = max_y - min_y if max_y != min_y else 1.0
    range_z = max_z - min_z if max_z != min_z else 1.0

    normalized = []
    for x, y, z in vertices:
        nx = (2 * (x - min_x) / range_x) - 1
        ny = (2 * (y - min_y) / range_y) - 1
        nz = (2 * (z - min_z) / range_z) - 1

        normalized.append((nx, ny, nz))

    return normalized

def save_vertices(filename, normalized):
    path = os.path.join(BASE_DIR, filename)

    with open(path, "r") as f:
        original_lines = f.readlines()

    idx = 0
    with open(path, "w") as f:
        for line in original_lines:
            stripped = line.strip()

            if stripped == '':
                f.write("\n")
                continue

            parts = stripped.split()
            if len(parts) == 3:
                x, y, z = normalized[idx]
                f.write(f"{x:.6f} {y:.6f} {z:.6f}\n")
                idx += 1
            else:
                f.write(line)

def get_cube_vertices():
    return load_vertices_from_file("cube.vertices")

def get_semi_sphere_vertices():
    return load_vertices_from_file("semiesfera.vertices")

def get_cilinder_vertices():
    return load_vertices_from_file("cilindro.vertices")


def main():
    import sys

    if len(sys.argv) < 2:
        print("Uso: python script.py <arquivo>")
        sys.exit(1)

    filename = sys.argv[1]
    vertices = load_vertices_from_file(filename)
    normalized = normalize(vertices)
    save_vertices(filename, normalized)

    print(f"Arquivo '{filename}' normalizado com sucesso.")


if __name__ == "__main__":
    main()
            

            
import math

def generate_ring(num_points=36, radius=1.0, y_top=0.1, y_bottom=-0.1):
    """
    Gera os vértices de um anel cilíndrico (setor cilíndrico sem tampas).
    Cada fatia angular vira 2 triângulos.

    num_points : quantos pontos por anel (mais = mais suave)
    radius     : raio do anel
    y_top      : altura do anel superior
    y_bottom   : altura do anel inferior
    """
    vertices = []

    for i in range(num_points):
        angle1 = (2 * math.pi * i) / num_points
        angle2 = (2 * math.pi * (i + 1)) / num_points

        x1 = radius * math.cos(angle1)
        z1 = radius * math.sin(angle1)

        x2 = radius * math.cos(angle2)
        z2 = radius * math.sin(angle2)

        # triângulo 1
        vertices.append((x1, y_top,    z1))
        vertices.append((x2, y_top,    z2))
        vertices.append((x1, y_bottom, z1))

        # triângulo 2
        vertices.append((x2, y_top,    z2))
        vertices.append((x2, y_bottom, z2))
        vertices.append((x1, y_bottom, z1))

    return vertices


def save(filename, vertices):
    with open(filename, "w") as f:
        for x, y, z in vertices:
            f.write(f"{x:.6f} {y:.6f} {z:.6f}\n")
    print(f"{len(vertices)} vértices salvos em '{filename}'")


if __name__ == "__main__":
    verts = generate_ring(num_points=36, radius=1.0, y_top=0.1, y_bottom=-0.1)
    save("ring.vertices", verts)

# Gera e salva os vértices de um disco plano para uso como malha base.

import math

def generate_disk(num_points=36, radius=1.0, y=0.0):
    """
    Gera os vértices de um disco plano preenchido.
    Cada fatia angular vira 1 triângulo: centro + ponto1 + ponto2.

    num_points : quantos pontos na borda (mais = mais suave)
    radius     : raio do disco
    y          : altura do disco no eixo Y
    """
    vertices = []
    cx, cy, cz = 0.0, y, 0.0  # centro

    for i in range(num_points):
        angle1 = (2 * math.pi * i) / num_points
        angle2 = (2 * math.pi * (i + 1)) / num_points

        x1 = radius * math.cos(angle1)
        z1 = radius * math.sin(angle1)

        x2 = radius * math.cos(angle2)
        z2 = radius * math.sin(angle2)

        vertices.append((cx, cy, cz))
        vertices.append((x1, y,  z1))
        vertices.append((x2, y,  z2))

    return vertices


def save(filename, vertices):
    with open(filename, "w") as f:
        for x, y, z in vertices:
            f.write(f"{x:.6f} {y:.6f} {z:.6f}\n")
    print(f"{len(vertices)} vértices salvos em '{filename}'")


if __name__ == "__main__":
    verts = generate_disk(num_points=36, radius=1.0, y=0.0)
    save("disk.vertices", verts)

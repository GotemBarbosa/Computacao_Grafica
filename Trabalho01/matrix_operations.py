import numpy as np
import math

def multiplica_matriz(a,b):
    m_a = a.reshape(4,4)
    m_b = b.reshape(4,4)
    m_c = np.dot(m_a,m_b)
    c = m_c.reshape(1,16)
    return c

def mat_rotacao_x(angulo):
    c, s = math.cos(angulo), math.sin(angulo)
    return np.array([
        1.0, 0.0, 0.0, 0.0,  # X não muda — estamos girando em torno dele
        0.0,   c,  -s, 0.0,  # Y e Z são afetados
        0.0,   s,   c, 0.0,
        0.0, 0.0, 0.0, 1.0,
    ], np.float32)

def mat_rotacao_y(angulo):
    c, s = math.cos(angulo), math.sin(angulo)
    return np.array([
          c, 0.0,   s, 0.0,  # X e Z são afetados
        0.0, 1.0, 0.0, 0.0,  # Y não muda — estamos girando em torno dele
         -s, 0.0,   c, 0.0,
        0.0, 0.0, 0.0, 1.0,
    ], np.float32)


def mat_rotacao_z(angulo):
    c, s = math.cos(angulo), math.sin(angulo)
    return np.array([
        c,  -s, 0.0, 0.0,
        s,   c, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0,
    ], np.float32)

def mat_translacao(tx, ty, tz):
    return np.array([
        1.0, 0.0, 0.0,  tx,
        0.0, 1.0, 0.0,  ty,
        0.0, 0.0, 1.0,  tz,
        0.0, 0.0, 0.0, 1.0,
    ], np.float32)

def mat_identidade():
    return np.eye(4, dtype=np.float32).reshape(1, 16)

def get_centroid(vertices_list, ini, qtde):
    x_sum = 0
    y_sum = 0
    z_sum = 0

    for i in range(ini, ini + qtde):
        x_sum += float(vertices_list[i][0])
        y_sum += float(vertices_list[i][1])
        z_sum += float(vertices_list[i][2])

    c = [x_sum/qtde, y_sum/qtde, z_sum/qtde]

    return c
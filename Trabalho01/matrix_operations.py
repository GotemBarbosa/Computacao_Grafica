# Define operações de matrizes e compõe transformações geométricas usadas na cena.

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

def mat_escala(sx, sy, sz):
    return np.array([
        sx, 0.0, 0.0,  0.0,
        0.0, sy, 0.0,  0.0,
        0.0, 0.0, sz,  0.0,
        0.0, 0.0, 0.0, 1.0,
    ], np.float32)

def mat_identidade():
    return np.array([
        1.0, 0.0, 0.0,  0.0,
        0.0, 1.0, 0.0,  0.0,
        0.0, 0.0, 1.0,  0.0,
        0.0, 0.0, 0.0, 1.0,
    ], np.float32)

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

def transforma_vetor(matriz, vetor):
    x, y, z = vetor
    v = [x, y, z, 1.0]

    resultado = [0.0, 0.0, 0.0, 0.0]

    # matriz está no formato (1,16)
    flat = matriz[0]

    for i in range(4):
        for j in range(4):
            resultado[i] += flat[i*4 + j] * v[j]

    return resultado[:3]

'''
Espera um dicionário no formato:
{
'angle_after_moving': [x_angle, y_angle, z_angle],
'angle_before_moving': [x_angle, y_angle, z_angle],
'scale': [x_scale, y_scale, z_scale],
'final_translation': [x_pos, y_pos, z_pos], --> Destino final da parte do objeto (onde ele ficará na cena)
'part_position': [x_pos, y_pos, z_pos], --> Destino relativo a posição do objeto total (por exemplo, a posição do braço em relação ao corpo total)
'centroid': [x_pos, y_pos, z_pos] --> Caso o objeto não esteja centralizado e seja necessário jogar ele para a origem antes de realizar as operações, utilizando o centroid
}
'''
def final_matrix(d: dict):
    mat_transform = mat_identidade()
    if 'final_translation' in d:
        mat_transform = multiplica_matriz(mat_transform, mat_translacao(d['final_translation'][0], d['final_translation'][1], d['final_translation'][2]))        
    if 'angle_after_moving' in d:
        if d['angle_after_moving'][0]: mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(d['angle_after_moving'][0])))
        if d['angle_after_moving'][1]: mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(math.radians(d['angle_after_moving'][1])))
        if d['angle_after_moving'][2]: mat_transform = multiplica_matriz(mat_transform, mat_rotacao_z(math.radians(d['angle_after_moving'][2])))
    if 'part_position' in d:
        if d['part_position'] != [0, 0, 0]:
            mat_transform = multiplica_matriz(mat_transform, mat_translacao(d['part_position'][0], d['part_position'][1], d['part_position'][2]))
    if 'angle_before_moving' in d:
        if d['angle_before_moving'][0]: mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(d['angle_before_moving'][0])))
        if d['angle_before_moving'][1]: mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(math.radians(d['angle_before_moving'][1])))
        if d['angle_before_moving'][2]: mat_transform = multiplica_matriz(mat_transform, mat_rotacao_z(math.radians(d['angle_before_moving'][2])))
    if 'scale' in d:
        mat_transform = multiplica_matriz(mat_transform, mat_escala(d['scale'][0], d['scale'][1], d['scale'][2]))
    if 'angle_before_scale' in d:
        if d['angle_before_scale'][0]: mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(d['angle_before_scale'][0])))
        if d['angle_before_scale'][1]: mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(math.radians(d['angle_before_scale'][1])))
        if d['angle_before_scale'][2]: mat_transform = multiplica_matriz(mat_transform, mat_rotacao_z(math.radians(d['angle_before_scale'][2])))

    if 'centroid' in d:
        mat_transform = multiplica_matriz(mat_transform, mat_translacao(-d['centroid'][0], -d['centroid'][1], -d['centroid'][2]))                
    
    return mat_transform

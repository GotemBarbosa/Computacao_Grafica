import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from matrix_operations import *
import random
from .utils import *


def create_roblox(loc_color, loc_mat_transform, objects_dict, angulo, pos=[0, 0, 0], scale=1.0):
    cube_centroid = objects_dict['cube']['centroid']
    cilinder_centroid = objects_dict['cilinder']['centroid']

    ini_cube = objects_dict['cube']['ini_index']
    end_cube = objects_dict['cube']['end_index']
    
    ini_cilinder = objects_dict['cilinder']['ini_index']
    end_cilinder = objects_dict['cilinder']['end_index']

    '''
    ===========================================
    DESENHANDO PERNA ESQUERDA
    ===========================================
    '''
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0]*scale, pos[1]*scale, pos[2]*scale))
    # apenas para ele rotacionar em torno dele mesmo
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(-0.11*scale, -0.2*scale, 0.0*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(0.1*scale, 0.2*scale, 0.1*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(-cube_centroid[0], -cube_centroid[1], -cube_centroid[2]))
    #color_vector = [[1] * 4 for _ in range(6)]
    color_vector = [[3/255, 161/255, 8/255, 1.0] for _ in range(6)]
    #color_vector[0] = [1, 0, 0, 1.0] # cor da face 1 --> VERMELHO
    #color_vector[1] = [0, 0, 1, 1.0] # cor da face 2 --> AZUL
    #color_vector[2] = [3/255, 161/255, 8/255, 1.0] # cor da face 3 --> VERDE
    #color_vector[3] = [1, 1, 0, 1.0] # cor da face 4 --> AMARELA
    #color_vector[4] = [0.5, 0.5, 0.5, 1.0] # cor da face 5 --> CINZA
    #color_vector[5] = [0.5, 0, 0, 1.0] # cor da face 6 --> MARROM

    draw_cube(ini_cube, loc_color, loc_mat_transform, mat_transform, color_vector)


    '''
    ===========================================
    DESENHANDO PERNA DIREITA
    ===========================================
    '''
    color_vector[2] = [3/255, 161/255, 8/255, 1.0] 
    
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0]*scale, pos[1]*scale, pos[2]*scale))
    # apenas para ele rotacionar em torno dele mesmo
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0.11*scale, -0.2*scale, 0.0*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(0.1*scale, 0.2*scale, 0.1*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(-cube_centroid[0], -cube_centroid[1], -cube_centroid[2]))
    draw_cube(ini_cube, loc_color, loc_mat_transform, mat_transform, color_vector)


    '''
    ===========================================
    DESENHANDO TRONCO
    ===========================================
    '''
    #color_vector[2] = [3/255, 140/255, 252/255, 1.0] 
    color_vector = [[3/255, 140/255, 252/255, 1.0] for _ in range(6)]
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0]*scale, pos[1]*scale, pos[2]*scale))
    # apenas para ele rotacionar em torno dele mesmo
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0*scale, 0.21*scale, 0.0*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(0.21*scale, 0.2*scale, 0.1*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(-cube_centroid[0], -cube_centroid[1], -cube_centroid[2]))
    draw_cube(ini_cube, loc_color, loc_mat_transform, mat_transform, color_vector)

    '''
    ===========================================
    DESENHANDO O BRAÇO DIREITO
    ===========================================
    '''
    #color_vector[2] = [1, 1, 0, 1.0] 
    color_vector = [[1, 1, 0, 1.0] for _ in range(6)]
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0]*scale, pos[1]*scale, pos[2]*scale))
    # apenas para ele rotacionar em torno dele mesmo
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0.32*scale, 0.21*scale, 0.0*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(0.1*scale, 0.2*scale, 0.1*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(-cube_centroid[0], -cube_centroid[1], -cube_centroid[2]))
    draw_cube(ini_cube, loc_color, loc_mat_transform, mat_transform, color_vector)

    '''
    ===========================================
    DESENHANDO O BRAÇO ESQUERDO
    ===========================================
    '''
    #color_vector[2] = [1, 1, 0, 1.0] 
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0]*scale, pos[1]*scale, pos[2]*scale))
    # apenas para ele rotacionar em torno dele mesmo
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(-0.32*scale, 0.21*scale, 0.0*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(0.1*scale, 0.2*scale, 0.1*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(-cube_centroid[0], -cube_centroid[1], -cube_centroid[2]))
    draw_cube(ini_cube, loc_color, loc_mat_transform, mat_transform, color_vector)

    '''
    ===========================================
    DESENHANDO A CABEÇA
    ===========================================
    '''
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0]*scale, pos[1]*scale, pos[2]*scale))
    # apenas para ele rotacionar em torno dele mesmo
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0*scale, 0.52*scale, 0.0*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(0.1*scale, 0.1*scale, 0.1*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(90)))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(-cilinder_centroid[0], -cilinder_centroid[1], -cilinder_centroid[2]))
    color_vector = []

    for triangle in range(ini_cilinder, end_cilinder,3):
        random.seed( triangle )
        R = random.random()
        G = random.random()
        B = random.random()  
        color_vector.append([R, G, B, 1.0])

    draw_generic_object(ini_cilinder, end_cilinder, loc_color, loc_mat_transform, mat_transform, color_vector)




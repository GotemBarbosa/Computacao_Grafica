
import random

from matrix_operations import *
from .utils import *

def create_pokeball(loc_color, loc_mat_transform, objects_dict, angulo, pos=[0,0,0], scale=1.0, colors_dict=None):
    #primitivas utilizadas:
    semisphere_centroid = objects_dict["semi_sphere"]["centroid"]
    
    ini_semisphere = objects_dict["semi_sphere"]["ini_index"]
    end_semisphere = objects_dict["semi_sphere"]["end_index"]

    ini_ring = objects_dict["ring"]["ini_index"]
    end_ring = objects_dict["ring"]["end_index"]

    ini_disk = objects_dict["disk"]["ini_index"]
    end_disk = objects_dict["disk"]["end_index"]
    disk_centroid = objects_dict["disk"]["centroid"]

    base_rotation = 15

    if colors_dict is None:
        colors_dict = {
            "upBall":    [1.0, 0.0, 0.0, 1.0],
            "downBall":  [1.0, 1.0, 1.0, 1.0],
            "ring":      [0.0, 0.0, 0.0, 1.0],
            "outerDisk": [0.0, 0.0, 0.0, 1.0],
            "innerdisk": [1.0, 1.0, 1.0, 1.0],
        }

    '''
    ===========================================
    DESENHANDO A PARTE DE CIMA DA POKEBOLA
    ===========================================
    '''

    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0]*scale, pos[1]*scale, pos[2]*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(scale, scale, scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(90 - base_rotation)))

    color_vector = [colors_dict["upBall"]] * ((end_semisphere - ini_semisphere) // 3)
    draw_generic_object(ini_semisphere, end_semisphere, loc_color, loc_mat_transform, mat_transform, color_vector)



    '''
    ===========================================
    DESENHANDO A PARTE DE BAIXO DA POKEBOLA
    ===========================================
    '''
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0]*scale, pos[1]*scale, pos[2]*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(scale, scale, scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(-math.radians(90 + base_rotation)))

    color_vector = [colors_dict["downBall"]] * ((end_semisphere - ini_semisphere) // 3)
    draw_generic_object(ini_semisphere, end_semisphere, loc_color, loc_mat_transform, mat_transform, color_vector)


    '''
    ===========================================
    DESENHANDO O ANEL PRETO CENTRAL
    ===========================================
    '''

    ring_scale = 0.5  # ajusta o raio do anel ao raio da semiesfera
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0]*scale, pos[1]*scale, pos[2]*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(ring_scale*scale, ring_scale*scale, ring_scale*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(-math.radians(base_rotation)))

    color_vector = [colors_dict["ring"]] * ((end_ring - ini_ring) // 3)
    draw_generic_object(ini_ring, end_ring, loc_color, loc_mat_transform, mat_transform, color_vector)

    '''
    ===========================================
    DESENHANDO O DISCO PRETO
    ===========================================
    '''
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0]*scale, pos[1]*scale, pos[2]*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0.00*scale, -0.12*scale, -0.49*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(0.15*scale, 0.15*scale, 0.15*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(-math.radians(base_rotation+90)))

    color_vector = [colors_dict["outerDisk"]] * ((end_disk - ini_disk) // 3)
    draw_generic_object(ini_disk, end_disk, loc_color, loc_mat_transform, mat_transform, color_vector)



    '''
    ===========================================
    DESENHANDO O DISCO BRANCO
    ===========================================
    '''
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0]*scale, pos[1]*scale, pos[2]*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0.00*scale, -0.12*scale, -0.50*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(0.08*scale, 0.08*scale, 0.08*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(-math.radians(base_rotation+90)))

    color_vector = [colors_dict["innerdisk"]] * ((end_disk - ini_disk) // 3)
    draw_generic_object(ini_disk, end_disk, loc_color, loc_mat_transform, mat_transform, color_vector)
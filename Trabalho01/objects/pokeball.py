
import random

from matrix_operations import *
from .utils import *

def create_pokeball(loc_color, loc_mat_transform, objects_dict, angulo, pos=[0,0,0], scale=1.0, colors_dict=None, open=False):
    #primitivas utilizadas:
    semisphere_centroid = objects_dict["semi_sphere"]["centroid"]
    
    ini_semisphere = objects_dict["semi_sphere"]["ini_index"]
    end_semisphere = objects_dict["semi_sphere"]["end_index"]

    ini_ring = objects_dict["ring"]["ini_index"]
    end_ring = objects_dict["ring"]["end_index"]

    ini_disk = objects_dict["disk"]["ini_index"]
    end_disk = objects_dict["disk"]["end_index"]
    disk_centroid = objects_dict["disk"]["centroid"]

    base_rotation = 8.59

    if colors_dict is None:
        colors_dict = {
            "upBall":    [1.0, 0.0, 0.0, 1.0],
            "downBall":  [1.0, 1.0, 1.0, 1.0],
            "ring":      [0.0, 0.0, 0.0, 1.0],
            "outerDisk": [0.0, 0.0, 0.0, 1.0],
            "innerdisk": [1.0, 1.0, 1.0, 1.0],
        }

    if not isinstance(open, bool):
        raise TypeError("O parametro 'open' deve ser bool.")

    '''
    ===========================================
    DESENHANDO A PARTE DE CIMA DA POKEBOLA
    ===========================================
    '''

    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2])) # leva para a posição final
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo)) # girar em torno do eixo y
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(base_rotation)))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0, 0.05*scale, 0)) # transladada levemente para CIMA
    mat_transform = multiplica_matriz(mat_transform, mat_escala(scale, scale, scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(90)))

    color_vector = [colors_dict["upBall"]] * ((end_semisphere - ini_semisphere) // 3)
    
    draw_generic_object(ini_semisphere, end_semisphere, loc_color, loc_mat_transform, mat_transform, color_vector)



    '''
    ===========================================
    DESENHANDO A PARTE DE BAIXO DAS POKEBOLA
    ===========================================
    '''
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(base_rotation)))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0, -0.05*scale, 0)) # transladada levemente para BAIXO
    mat_transform = multiplica_matriz(mat_transform, mat_escala(scale, scale, scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(-math.radians(90)))

    color_vector = [colors_dict["downBall"]] * ((end_semisphere - ini_semisphere) // 3)
    
    draw_generic_object(ini_semisphere, end_semisphere, loc_color, loc_mat_transform, mat_transform, color_vector)


    '''
    ===========================================
    DESENHANDO O ANEL PRETO CENTRAL
    ===========================================
    '''

    ring_scale = 0.98  # ajusta o raio do anel ao raio da semiesfera
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(base_rotation)))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(ring_scale*scale, ring_scale*scale, ring_scale*scale))

    color_vector = [colors_dict["ring"]] * ((end_ring - ini_ring) // 3)
    
    draw_generic_object(ini_ring, end_ring, loc_color, loc_mat_transform, mat_transform, color_vector)

    '''
    ===========================================
    DESENHANDO O DISCO PRETO
    ===========================================
    '''
    disk_scale = 0.25
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(base_rotation)))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0, 0, -scale))  # traz para frente da pokebola
    mat_transform = multiplica_matriz(mat_transform, mat_escala(disk_scale*scale, disk_scale*scale, disk_scale*scale))  # ajusta para um tamanho proporcional
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(90)))

    color_vector = [colors_dict["outerDisk"]] * ((end_disk - ini_disk) // 3)
    draw_generic_object(ini_disk, end_disk, loc_color, loc_mat_transform, mat_transform, color_vector)



    '''
    ===========================================
    DESENHANDO O DISCO BRANCO
    ===========================================
    '''
    white_disk_scale = disk_scale*0.65
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(base_rotation)))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0, 0, -scale-0.005)) # traz para a frente da pokebola e poucos pixels a frente do disco preto
    mat_transform = multiplica_matriz(mat_transform, mat_escala(white_disk_scale*scale, white_disk_scale*scale, white_disk_scale*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(90)))

    color_vector = [colors_dict["innerdisk"]] * ((end_disk - ini_disk) // 3)
    draw_generic_object(ini_disk, end_disk, loc_color, loc_mat_transform, mat_transform, color_vector)

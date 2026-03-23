from matrix_operations import *
from .utils import *

def create_healer(loc_color, loc_mat_transform, objects_dict, angulo, pos=[0,0,0], scale=1.0, pokeball_positions=[]):

    ini_cube =objects_dict["cube"]["ini_index"]

    '''
    ===========================================
    DESENHANDO O CORPO DO HEALER
    ===========================================
    '''
    #base superior
    healer_color = [
        [0.9, 0.9, 0.9, 1.0],  # frente  
        [0.8, 0.8, 0.80, 1.0],  # direita
        [0.9, 0.9, 0.9, 1.0],  # trás  
        [1.0, 0.85, 0.90, 1.0],  # esquerda
        [1.0, 1.0,  1.0,  1.0],  # baixo 
        [1.0, 1.0,  1.0,  1.0],  # cima  
    ]

    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(-angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(2.0*scale, 0.4*scale, 3.0*scale))
    draw_cube(ini_cube, loc_color, loc_mat_transform, mat_transform, healer_color)


    #base central
    healer_color = [
        [0.9, 0.2, 0.2, 1.0],
        [0.7, 0.1, 0.1, 1.0],
        [0.9, 0.2, 0.2, 1.0],
        [0.8, 0.15, 0.15, 1.0],
        [1.0, 1.0,  1.0,  1.0],
        [1.0, 1.0,  1.0,  1.0],
    ]

    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0]+0.01, pos[1]-0.14, pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(-angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(1.95*scale, 0.1*scale, 2.90*scale))
    draw_cube(ini_cube, loc_color, loc_mat_transform, mat_transform, healer_color)

    #base inferior
    healer_color = [
        [0.9, 0.9, 0.9, 1.0],  # frente  
        [0.8, 0.8, 0.80, 1.0],  # direita
        [0.9, 0.9, 0.9, 1.0],  # trás  
        [1.0, 0.85, 0.90, 1.0],  # esquerda
        [1.0, 1.0,  1.0,  1.0],  # baixo 
        [1.0, 1.0,  1.0,  1.0],  # cima  
    ]

    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1]-0.30, pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(-angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(2.0*scale, 0.4*scale, 3.0*scale))
    draw_cube(ini_cube, loc_color, loc_mat_transform, mat_transform, healer_color)



    '''
    ===========================================
    DESENHANDO A PARTE DE CIMA DO HEALER
    ===========================================
    '''

    # Placa azul em cima
    blue_color = [
        [0.25, 0.45, 0.95, 1.0],  # frente  
        [0.2, 0.4, 0.9, 1.0],  # direita
        [0.25, 0.45, 0.95, 1.0],  # trás  
        [0.3, 0.5, 1.0, 1.0],  # esquerda
        [0.3, 0.5, 1.0, 1.0],  # baixo 
        [0.3, 0.5, 1.0, 1.0],  # cima  
    ]

    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1]+0.10, pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(-angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0, 0.10*scale, 0))  # sobe pra cima da base
    mat_transform = multiplica_matriz(mat_transform, mat_escala(1.8*scale, 0.05*scale, 2.8*scale))
    draw_cube(ini_cube, loc_color, loc_mat_transform, mat_transform, blue_color)

    '''
    ===========================================
    DISCOS NAS POSIÇÕES DAS POKEBOLAS (SOMBRA FAKE)
    ===========================================
    '''
    ini_disk = objects_dict["disk"]["ini_index"]
    end_disk = objects_dict["disk"]["end_index"]
    disk_color = [[0.05, 0.1, 0.5, 1.0]] * ((end_disk - ini_disk) // 3)

    for pb_pos in pokeball_positions:
        mat_transform = mat_identidade()
        mat_transform = multiplica_matriz(mat_transform, mat_translacao(pb_pos[0], pb_pos[1]-0.08, pb_pos[2]))
        mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(-angulo))
        mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
        mat_transform = multiplica_matriz(mat_transform, mat_escala(0.09, 0.09, 0.09))
        draw_generic_object(ini_disk, end_disk, loc_color, loc_mat_transform, mat_transform, disk_color)
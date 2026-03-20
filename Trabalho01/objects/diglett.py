import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from matrix_operations import *
import random
from .utils import *

def create_diglett(loc_color, loc_mat_transform, objects_dict, angulo, pos=[0, 0, 0], scale=1.0):

    ini_cilinder = objects_dict['cilinder']['ini_index']
    end_cilinder = objects_dict['cilinder']['end_index']

    ini_semisphere = objects_dict['semi_sphere']['ini_index']
    end_semisphere = objects_dict['semi_sphere']['end_index']

    ini_disk = objects_dict["disk"]["ini_index"]
    end_disk = objects_dict["disk"]["end_index"]

    base_rotation = 0

    cor_marrom = [[143/255, 80/255, 19/255, 1.0]] * ((end_cilinder - ini_cilinder)//3)
    '''
    ==========================================
    CRIA CORPO
    ==========================================
    '''

    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(base_rotation)))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0, 1.5*scale, 0))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(scale, scale*1.5, scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(90)))
    draw_generic_object(ini_cilinder, end_cilinder, loc_color, loc_mat_transform, mat_transform, cor_marrom)


    '''
    ==========================================
    CRIA CABEÇA
    ==========================================
    '''
    cor_marrom = [[143/255, 80/255, 19/255, 1.0]] * ((end_semisphere - ini_semisphere)//3)
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(base_rotation)))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0, (scale*1.5) * 2, 0)) # Cabeça translada 2x pq sobe até a altura da cabeça, e dps é regulada com a translação padrao do diglet
    mat_transform = multiplica_matriz(mat_transform, mat_escala(scale, scale, scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(90)))
    draw_generic_object(ini_semisphere, end_semisphere, loc_color, loc_mat_transform, mat_transform, cor_marrom)



    '''
    ==========================================
    CRIA NARIZ
    ==========================================
    '''
    cor_rosa = [[196/255, 112/255, 192/255, 1.0]] * ((end_cilinder - ini_cilinder)//3)

    altura_nariz = scale/5
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(base_rotation)))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0, scale*(1.25+1.5), -scale))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(altura_nariz*2, altura_nariz, altura_nariz/8))
    draw_generic_object(ini_cilinder, end_cilinder, loc_color, loc_mat_transform, mat_transform, cor_rosa)


    distancia_olhos = scale*0.8

    '''
    ==========================================
    CRIA OLHO DIREITO
    ==========================================
    '''
    cor_preta = [[0, 0, 0, 1.0]] * ((end_cilinder - ini_cilinder)//3)
    altura_do_olho = scale/4
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(base_rotation)))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(distancia_olhos/2, scale*(1.8+altura_do_olho+1.5), -scale*0.85))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(altura_do_olho/3, altura_do_olho, altura_do_olho/4))
    draw_generic_object(ini_cilinder, end_cilinder, loc_color, loc_mat_transform, mat_transform, cor_preta)



    '''
    ==========================================
    CRIA ESQUERDO
    ==========================================
    '''
    cor_preta = [[0, 0, 0, 1.0]] * ((end_cilinder - ini_cilinder)//3)
    altura_do_olho = scale/4
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(base_rotation)))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(-distancia_olhos/2, scale*(1.8+altura_do_olho+1.5), -scale*0.85))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(altura_do_olho/3, altura_do_olho, altura_do_olho/4))
    draw_generic_object(ini_cilinder, end_cilinder, loc_color, loc_mat_transform, mat_transform, cor_preta)


    '''
    ==========================================
    CRIA CHÃO
    ==========================================
    '''
    cor_cinza = [[133/255, 133/255, 133/255, 1.0]] * ((end_cilinder - ini_cilinder)//3)
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(base_rotation)))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0, scale* (-1  + 1.5) - 0.01, 0))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(scale*2, scale/2, scale*2))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(90)))

    draw_generic_object(ini_cilinder, end_cilinder, loc_color, loc_mat_transform, mat_transform, cor_cinza)

    '''
    ==========================================
    CRIA DISCO DE SOMBRA NO CHÃO
    ==========================================
    '''
    cor_cinza = [[79/255, 79/255, 79/255, 1.0]] * ((end_disk - ini_disk)//3)
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(base_rotation)))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0, scale*(-1*0.5 + 1.5) - 0.009, 0))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(scale*1.2, scale/2, scale*1.2))

    draw_generic_object(ini_disk, end_disk, loc_color, loc_mat_transform, mat_transform, cor_cinza)


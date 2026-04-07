# Monta e desenha o Diglett com corpo, rosto, chão e sombra.

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from matrix_operations import *
import random
from .utils import *
import state

def create_diglett(angulos=[0, 0, 0], pos=[0, 0, 0], scale=1.0, enterrado=0):

    diglett = state.properties['diglett']
    ini_cilinder = state.objects_dict['cilinder']['ini_index']
    end_cilinder = state.objects_dict['cilinder']['end_index']

    ini_semisphere = state.objects_dict['semi_sphere']['ini_index']
    end_semisphere = state.objects_dict['semi_sphere']['end_index']

    ini_disk = state.objects_dict["disk"]["ini_index"]
    end_disk = state.objects_dict["disk"]["end_index"]

    '''
    ==========================================
    CRIA CORPO
    ==========================================
    '''
    color_vector = [diglett['colors']['body'] for _ in range((end_cilinder - ini_cilinder)//3)]
    body = {
        "scale": [1*scale, 1.5*scale, 1*scale],
        "part_position": [0, (1.5+enterrado)*scale, 0],
        "angle_after_moving": angulos,
        "angle_before_scale": [90, 0, 0],
        "final_translation": [pos[0], pos[1], pos[2]]
    }
    draw_generic_object(ini_cilinder, end_cilinder, final_matrix(body), color_vector)


    '''
    ==========================================
    CRIA CABEÇA
    ==========================================
    '''
    color_vector = [diglett['colors']['head'] for _ in range((end_semisphere - ini_semisphere)//3)]
    head = {
        "scale": [1*scale, 1*scale, 1*scale],
        "part_position": [0, (3+enterrado)*scale, 0],
        "angle_after_moving": angulos,
        "angle_before_moving": [90, 0, 0],
        "final_translation": [pos[0], pos[1], pos[2]]
    }
    draw_generic_object(ini_semisphere, end_semisphere, final_matrix(head), color_vector)



    '''
    ==========================================
    CRIA NARIZ
    ==========================================
    '''
    altura_nariz = scale/5
    color_vector = [diglett['colors']['nose'] for _ in range((end_cilinder - ini_cilinder)//3)]
    nose = {
        "scale": [altura_nariz*2, altura_nariz, altura_nariz/8],
        "part_position": [0, (2.75+enterrado)*scale, -scale],
        "angle_after_moving": angulos,
        "angle_before_moving": [0, 0, 0],
        "final_translation": [pos[0], pos[1], pos[2]]
    }
    draw_generic_object(ini_cilinder, end_cilinder, final_matrix(nose), color_vector)



    '''
    ==========================================
    CRIA OLHO ESQUERDO
    ==========================================
    '''
    distancia_olhos = scale*0.8
    altura_do_olho = scale/4
    color_vector = [diglett['colors']['eye'] for _ in range((end_cilinder - ini_cilinder)//3)]
    left_eye = {
        "scale": [altura_do_olho/3, altura_do_olho, altura_do_olho/4],
        "part_position": [distancia_olhos/2, scale*(1.8+altura_do_olho+1.5+enterrado), -scale*0.85],
        "angle_after_moving": angulos,
        "angle_before_moving": [0, 0, 0],
        "final_translation": [pos[0], pos[1], pos[2]]
    }
    draw_generic_object(ini_cilinder, end_cilinder, final_matrix(left_eye), color_vector)


    '''
    ==========================================
    CRIA OLHO DIREITO
    ==========================================
    '''
    right_eye = {
        "scale": [altura_do_olho/3, altura_do_olho, altura_do_olho/4],
        "part_position": [-distancia_olhos/2, scale*(1.8+altura_do_olho+1.5+enterrado), -scale*0.85],
        "angle_after_moving": angulos,
        "angle_before_moving": [0, 0, 0],
        "final_translation": [pos[0], pos[1], pos[2]]
    }
    draw_generic_object(ini_cilinder, end_cilinder, final_matrix(right_eye), color_vector)


    '''
    ==========================================
    CRIA CHÃO
    ==========================================
    '''
    color_vector = [diglett['colors']['ground'] for _ in range((end_cilinder - ini_cilinder)//3)]
    ground = {
        "scale": [scale*2, scale*3, scale*2],
        "part_position": [0, scale* (-1  + 1.5 - 2.5) - 0.01, 0],
        "angle_after_moving": angulos,
        "angle_before_scale": [90, 0, 0],
        "final_translation": [pos[0], pos[1], pos[2]]
    }
    draw_generic_object(ini_cilinder, end_cilinder, final_matrix(ground), color_vector)

    '''
    ==========================================
    CRIA DISCO DE SOMBRA NO CHÃO
    ==========================================
    '''
    color_vector = [diglett['colors']['shadow'] for _ in range((end_disk - ini_disk)//3)]
    shadow = {
        "scale": [scale*1.2, scale/2, scale*1.2],
        "part_position": [0, scale*(-1*0.5 + 1.5) - 0.009, 0],
        "angle_after_moving": angulos,
        "angle_before_moving": [0, 0, 0],
        "final_translation": [pos[0], pos[1], pos[2]]
    }
    draw_generic_object(ini_disk, end_disk, final_matrix(shadow), color_vector)

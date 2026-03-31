import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from matrix_operations import *
import random
from .utils import *
import state


def create_roblox(angulo=[0, 0, 0], pos=[0, 0, 0], scale=1.0):

    roblox = state.properties['roblox']
    x_angle = roblox['x_angle']
    y_angle = roblox['y_angle']
    z_angle = roblox['z_angle']
    scale = roblox['scale']
    pos = roblox['position']


    ini_cube = state.objects_dict['cube']['ini_index']
    end_cube = state.objects_dict['cube']['end_index']
    
    ini_cilinder = state.objects_dict['cilinder']['ini_index']
    end_cilinder = state.objects_dict['cilinder']['end_index']

    '''
    ===========================================
    DESENHANDO PERNA ESQUERDA
    ===========================================
    '''
    left_leg = {
        "scale": [0.1*scale, 0.2*scale, 0.08*scale],
        "part_position": [-0.11*scale, -0.2*scale, 0.0],
        "angle_after_moving": [x_angle, y_angle, z_angle],
        "final_translation": [pos[0], pos[1], pos[2]]
    }
    color_vector = [roblox['colors']['left_leg'] for _ in range(6)]
    draw_cube(final_matrix(left_leg), color_vector)


    '''
    ===========================================
    DESENHANDO PERNA DIREITA
    ===========================================
    '''
    right_leg = {
        "scale": [0.1*scale, 0.2*scale, 0.08*scale],
        "part_position": [0.11*scale, -0.2*scale, 0.0],
        "angle_after_moving": [x_angle, y_angle, z_angle],
        "final_translation": [pos[0], pos[1], pos[2]]
    }
    color_vector = [roblox['colors']['right_leg'] for _ in range(6)]
    draw_cube(final_matrix(right_leg), color_vector)
    
    '''
    ===========================================
    DESENHANDO TRONCO
    ===========================================
    '''
    chest = {
        "scale": [0.21*scale, 0.2*scale, 0.1*scale],
        "part_position": [0, 0.2*scale, 0],
        "angle_after_moving": [x_angle, y_angle, z_angle],
        "final_translation": [pos[0], pos[1], pos[2]]
    }
    color_vector = [roblox['colors']['chest'] for _ in range(6)]
    draw_cube(final_matrix(chest), color_vector)

    '''
    ===========================================
    DESENHANDO O BRAÇO DIREITO
    ===========================================
    '''
    right_arm = {
        "scale": [0.08*scale, 0.2*scale, 0.08*scale],
        "part_position": [-0.29*scale, 0.2*scale, 0],
        "angle_after_moving": [x_angle, y_angle, z_angle],
        "final_translation": [pos[0], pos[1], pos[2]]
    }
    color_vector = [roblox['colors']['arm'] for _ in range(6)]
    draw_cube(final_matrix(right_arm), color_vector)

    '''
    ===========================================
    DESENHANDO O BRAÇO ESQUERDO
    ===========================================
    '''
    left_arm = {
        "scale": [0.08*scale, 0.2*scale, 0.08*scale],
        "part_position": [0.29*scale, 0.2*scale, 0],
        "angle_after_moving": [x_angle, y_angle, z_angle],
        "final_translation": [pos[0], pos[1], pos[2]]
    }
    draw_cube(final_matrix(left_arm), color_vector)


    '''
    ===========================================
    DESENHANDO A CABEÇA
    ===========================================
    '''
    head = {
        "scale": [0.1*scale, 0.1*scale, 0.1*scale],
        "part_position": [0, 0.5*scale, 0],
        "angle_after_moving": [x_angle, y_angle, z_angle],
        "angle_before_moving": [90, 0, 0],
        "final_translation": [pos[0], pos[1], pos[2]]
    }
    color_vector = [roblox['colors']['head'] for _ in range((end_cilinder - ini_cilinder)//3)]
    draw_generic_object(ini_cilinder, end_cilinder, final_matrix(head), color_vector)


    '''
    ===========================================
    DESENHANDO OLHO DIREITO
    ===========================================
    '''
    right_eye = {
        "scale": [0.01*scale, 0.02*scale, 0.05*scale],
        "part_position": [-0.03*scale, 0.55*scale, -0.05*scale],
        "angle_after_moving": [x_angle, y_angle, z_angle],
        "angle_before_moving": [0, 0, 0],
        "final_translation": [pos[0], pos[1], pos[2]]
    }
    color_vector = [roblox['colors']['eye'] for _ in range((end_cilinder - ini_cilinder)//3)]
    draw_generic_object(ini_cilinder, end_cilinder, final_matrix(right_eye), color_vector)



    '''
    ===========================================
    DESENHANDO OLHO ESQUERDO
    ===========================================
    '''
    left_eye = {
        "scale": [0.01*scale, 0.02*scale, 0.05*scale],
        "part_position": [0.03*scale, 0.55*scale, -0.05*scale],
        "angle_after_moving": [x_angle, y_angle, z_angle],
        "angle_before_moving": [0, 0, 0],
        "final_translation": [pos[0], pos[1], pos[2]]
    }
    color_vector = [roblox['colors']['eye'] for _ in range((end_cilinder - ini_cilinder)//3)]
    draw_generic_object(ini_cilinder, end_cilinder, final_matrix(left_eye), color_vector)


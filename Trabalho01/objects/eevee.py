
from .utils import *
from matrix_operations import *
import state


def create_eevee(angulo=0, pos=[0, 0, 0], scale=1.0):

    eevee_properties = state.properties['eevee']
    eevee_scale = eevee_properties['scale']
    x_angle = eevee_properties['x_angle']
    y_angle = eevee_properties['y_angle']
    z_angle = eevee_properties['z_angle']
    pos = eevee_properties.get('position', pos)

    bs = eevee_scale/10
    '''
    ===========================================
    DESENHANDO O CORPO
    ===========================================
    '''
    body = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'scale': [bs*2, bs*1.5, bs*4],
        'part_position': [0, 0, 0],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    color_vector = [state.properties['eevee']['colors']['body'] for _ in range(6)]
    draw_cube(final_matrix(body), color_vector)  


    '''
    ===========================================
    DESENHANDO A CABEÇA
    // 0.77647, 0.58431, 0.29020
    // 0.9, 0.49804, 0.13725
    ===========================================
    '''
    head = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'scale': [bs*2, bs*2, bs*2],
        'part_position': [0, bs*3.5, -bs*3],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    
    color_vector = [state.properties['eevee']['colors']['head'] for _ in range(6)]
    draw_cube(final_matrix(head), color_vector)  

    #color_vector = [state.properties['eevee']['colors']['cloud'] for _ in range(6)]

    '''
    ===========================================
    DESENHANDO AS 4 PATAS
    ===========================================
    '''
    color_vector = [state.properties['eevee']['colors']['leg'] for _ in range(6)]
    
    front_right_leg = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'scale': [bs*0.5, bs*1, bs*0.5],
        'part_position': [-1.5*bs, -bs*2.5, -bs*2.5],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_cube(final_matrix(front_right_leg), color_vector)  

    front_left_leg = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'scale': [bs*0.5, bs*1, bs*0.5],
        'part_position': [1.5*bs, -bs*2.5, -bs*2.5],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_cube(final_matrix(front_left_leg), color_vector) 

    back_right_leg = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'scale': [bs*0.5, bs*1, bs*0.5],
        'part_position': [-1.5*bs, -bs*2.5, bs*2.5],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_cube(final_matrix(back_right_leg), color_vector) 

    back_left_leg = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'scale': [bs*0.5, bs*1, bs*0.5],
        'part_position': [1.5*bs, -bs*2.5, bs*2.5],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_cube(final_matrix(back_left_leg), color_vector) 


    '''
    ===========================================
    DESENHANDO O ROSTO
    ===========================================
    '''

    # Desenha olho direito
    color_vector = [state.properties['eevee']['colors']['pupil']]
    left_eye = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'scale': [bs*0.8, bs*1.25, 1.0],
        'part_position': [1.2*bs, bs*3.9, -bs*5 - 0.01],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_generic_object(state.objects_dict['square']['ini_index'], state.objects_dict['square']['end_index'], final_matrix(left_eye), color_vector, flag=GL_TRIANGLE_STRIP)

    # Desenha reflexo no olho esquerdo
    color_vector = [state.properties['eevee']['colors']['white_dot']]
    left_dot = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'scale': [bs*0.4, bs*0.4, 1.0],
        'part_position': [1.15*bs, bs*4.3, -bs*5 - 0.02],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_generic_object(state.objects_dict['square']['ini_index'], state.objects_dict['square']['end_index'], final_matrix(left_dot), color_vector, flag=GL_TRIANGLE_STRIP)


    # Desenhando olho esquerdo
    color_vector = [state.properties['eevee']['colors']['pupil']]
    right_eye = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'scale': [bs*0.8, bs*1.25, 1.0],
        'part_position': [-1.2*bs, bs*3.9, -bs*5 - 0.01],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_generic_object(state.objects_dict['square']['ini_index'], state.objects_dict['square']['end_index'], final_matrix(right_eye), color_vector, flag=GL_TRIANGLE_STRIP)

    color_vector = [state.properties['eevee']['colors']['white_dot']]
    left_dot = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'scale': [bs*0.4, bs*0.4, 1.0],
        'part_position': [-1.15*bs, bs*4.3, -bs*5 - 0.02],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_generic_object(state.objects_dict['square']['ini_index'], state.objects_dict['square']['end_index'], final_matrix(left_dot), color_vector, flag=GL_TRIANGLE_STRIP)
  

    # Desenhando nariz
    color_vector = [state.properties['eevee']['colors']['nose']]
    nose = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'scale': [bs*0.4, bs*0.2, 1.0],
        'part_position': [0, bs*3.15, -bs*5 - 0.01],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_generic_object(state.objects_dict['square']['ini_index'], state.objects_dict['square']['end_index'], final_matrix(nose), color_vector, flag=GL_TRIANGLE_STRIP)

    # Desenhando Boca
    color_vector = [state.properties['eevee']['colors']['mouth']]
    mouth = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'scale': [bs*1.2, bs*0.6, 1.0],
        'part_position': [0, bs*2.5, -bs*5 - 0.01],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_generic_object(state.objects_dict['square']['ini_index'], state.objects_dict['square']['end_index'], final_matrix(mouth), color_vector, flag=GL_TRIANGLE_STRIP)
   



    '''
    ===========================================
    DESENHANDO A CAUDA
    ===========================================
    '''
    color_vector = [state.properties['eevee']['colors']['tail'] for _ in range(6)]
    tail = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'angle_before_moving': [-45, 0, 0],
        'scale': [bs*1.5, bs*1.5, bs*2],
        'part_position': [0, bs*2.2, bs*4.5],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_cube(final_matrix(tail), color_vector)

    color_vector = [state.properties['eevee']['colors']['cloud'] for _ in range(6)]
    tail_cloud = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'angle_before_moving': [-45, 0, 0],
        'scale': [bs*1.5-0.01, bs*1.5-0.01, bs*0.4],
        'part_position': [0, bs*3.8, bs*6.1],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_cube(final_matrix(tail_cloud), color_vector)    


    '''
    ===========================================
    DESENHANDO AS ORELHAS
    ===========================================
    '''
    color_vector = [state.properties['eevee']['colors']['ear'] for _ in range(6)]
    left_ear = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'angle_before_moving': [0, 0, -45],
        'scale': [bs*0.8, bs*2, bs*0.2],
        'part_position': [bs*2.5, bs*6, -bs*2],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_cube(final_matrix(left_ear), color_vector)

    right_ear = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'angle_before_moving': [0, 0, 45],
        'scale': [bs*0.8, bs*2, bs*0.2],
        'part_position': [-bs*2.5, bs*6, -bs*2],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_cube(final_matrix(right_ear), color_vector)

    # inner-ear esquerda
    color_vector = [state.properties['eevee']['colors']['inner_ear'] for _ in range(6)]
    left_inner_ear = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'angle_before_moving': [0, 0, -45],
        'scale': [bs*0.7, bs*2.5, 1.0],
        'part_position': [bs*2.5, bs*6, -bs*2-bs*0.2-0.01],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_generic_object(state.objects_dict['square']['ini_index'], state.objects_dict['square']['end_index'], final_matrix(left_inner_ear), color_vector, flag=GL_TRIANGLE_STRIP)
   
    right_inner_ear = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'angle_before_moving': [0, 0, 45],
        'scale': [bs*0.7, bs*2.5, 1.0],
        'part_position': [-bs*2.5, bs*6, -bs*2-bs*0.2-0.01],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_generic_object(state.objects_dict['square']['ini_index'], state.objects_dict['square']['end_index'], final_matrix(right_inner_ear), color_vector, flag=GL_TRIANGLE_STRIP)
   


    '''
    ===========================================
    DESENHANDO AS NUVENS
    ===========================================
    '''

    color_vector = [state.properties['eevee']['colors']['cloud'] for _ in range(6)]
    front_cloud = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'scale': [bs*1.7, bs*1.7, bs*1],
        'part_position': [0, -bs*0.3, -bs*3.8],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_cube(final_matrix(front_cloud), color_vector)  

    left_cloud = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'scale': [bs*0.9, bs*1.9, bs*2.5],
        'part_position': [bs*2.3, bs*0.3, -bs*1.8],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_cube(final_matrix(left_cloud), color_vector) 

    right_cloud = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'scale': [bs*0.9, bs*1.9, bs*2.5],
        'part_position': [-bs*2.3, bs*0.3, -bs*1.8],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_cube(final_matrix(right_cloud), color_vector)  

    back_cloud = {
        'angle_after_moving': [x_angle, y_angle, z_angle],
        'scale': [bs*1.9, bs*0.8, bs*1.5],
        'part_position': [0, bs*1.7, 0],
        'final_translation': [pos[0], pos[1], pos[2]]
    }
    draw_cube(final_matrix(back_cloud), color_vector)  


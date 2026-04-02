from matrix_operations import *
from .utils import *
import state

def create_healer(angulo=None, pos=None, scale=None, pokeball_positions=None, pokeball_scale=None):
    healer = state.properties["healer"]

    if angulo is None:
        angulo = healer["angles"]
    if pos is None:
        pos = healer["position"]
    if scale is None:
        scale = healer["scale"]
    if pokeball_positions is None:
        pokeball_positions = healer.get("pokeball_positions", [])
    if pokeball_scale is None:
        pokeball_scale = 0.4*scale

    x_angle, y_angle, z_angle = healer['angles']
    ini_disk = state.objects_dict["disk"]["ini_index"]
    end_disk = state.objects_dict["disk"]["end_index"]


    middle_base_h = 0.165*scale
    '''
    ===========================================
    DESENHANDO O CORPO DO HEALER
    ===========================================
    '''
    #base superior
    healer_color = healer["colors"]["upper_base"]

    sup_base = {
        "scale": [3*scale, 0.66*scale, 1.78*scale],
        "part_position": [0, 0.66*scale + middle_base_h, 0],
        "angle_after_moving": [angulo[0], angulo[1], angulo[2]],
        "angle_before_scale": [0, 0, 0],
        "final_translation": [pos[0], pos[1], pos[2]]
    }

    draw_cube(final_matrix(sup_base), healer_color)


    #base central
    healer_color = healer["colors"]["middle_base"]

    mid_base = {
        "scale": [2.9*scale, 0.165*scale, 1.65*scale],
        "part_position": [0, 0, 0],
        "angle_after_moving": [angulo[0], angulo[1], angulo[2]],
        "angle_before_scale": [0, 0, 0],
        "final_translation": [pos[0], pos[1], pos[2]]
    }

    draw_cube(final_matrix(mid_base), healer_color)

    #base inferior
    healer_color = healer["colors"]["lower_base"]

    lower_base = {
        "scale": [3*scale, 0.66*scale, 1.78*scale],
        "part_position": [0, -0.66*scale - middle_base_h, 0],
        "angle_after_moving": [angulo[0], angulo[1], angulo[2]],
        "angle_before_scale": [0, 0, 0],
        "final_translation": [pos[0], pos[1], pos[2]]  
    }

    draw_cube(final_matrix(lower_base), healer_color)



    '''
    ===========================================
    DESENHANDO A PARTE DE CIMA DO HEALER
    ===========================================
    '''

    # Placa azul em cima
    blue_color = healer["colors"]["top_plate"]

    blue_shape = {
        "scale": [2.8*scale, 0.088*scale, 1.55*scale],
        "part_position": [0, (0.66*2 + 0.1)*scale + middle_base_h, 0],
        "angle_after_moving": [angulo[0], angulo[1], angulo[2]],
        "angle_before_scale": [0, 0, 0],
        "final_translation": [pos[0], pos[1], pos[2]]  
    }

    draw_cube(final_matrix(blue_shape), blue_color)

    '''
    ===========================================
    DISCOS NAS POSIÇÕES DAS POKEBOLAS (SOMBRA FAKE)
    ===========================================
    '''
    disk_color = [healer["colors"]["pokeball_shadow"]] * ((end_disk - ini_disk) // 3)

    u_center = [0, (0.66*2 + 0.1*2)*scale + middle_base_h + 0.001, 0]

    shadows_positions = [
        [u_center[0] + scale*1.6, u_center[1], u_center[2] + scale*0.7],
        [u_center[0] + scale*1.6, u_center[1], u_center[2] - scale*0.7],
        [u_center[0], u_center[1], u_center[2] + scale*0.7],
        [u_center[0], u_center[1], u_center[2] - scale*0.7],
        [u_center[0] - scale*1.6, u_center[1], u_center[2] + scale*0.7],
        [u_center[0] - scale*1.6, u_center[1], u_center[2] - scale*0.7],
    ]

    pokeball_pos = []

    for s in shadows_positions:
        shadow = {
        "scale": [0.5*scale, 0.5*scale, 0.5*scale],
        "part_position": [s[0], s[1], s[2]],
        "angle_after_moving": [angulo[0], angulo[1], angulo[2]],
        "angle_before_scale": [0, 0, 0],
        "final_translation": [pos[0], pos[1], pos[2]]       
        }
        draw_generic_object(ini_disk, end_disk, final_matrix(shadow), disk_color)

    mat = mat_identidade()
    mat = multiplica_matriz(mat, mat_translacao(pos[0], pos[1], pos[2]))
    mat = multiplica_matriz(mat, mat_rotacao_x(math.radians(angulo[0])))
    mat = multiplica_matriz(mat, mat_rotacao_y(math.radians(angulo[1])))
    mat = multiplica_matriz(mat, mat_rotacao_z(math.radians(angulo[2]))) 
    for s in shadows_positions:
        p = [s[0], s[1]+pokeball_scale, s[2]]
        t = transforma_vetor(mat, p)
        pokeball_pos.append(t)

    return pokeball_pos

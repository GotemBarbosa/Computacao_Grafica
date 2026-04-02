from matrix_operations import *
from .utils import *
import state


def healer_transform(pos, angulo, local_pos, local_scale):
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(-angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(local_pos[0], local_pos[1], local_pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(local_scale[0], local_scale[1], local_scale[2]))
    return mat_transform


def create_healer(angulo=None, pos=None, scale=None, pokeball_positions=None):
    healer = state.properties["healer"]

    if angulo is None:
        angulo = healer["angle"]
    if pos is None:
        pos = healer["position"]
    if scale is None:
        scale = healer["scale"]
    if pokeball_positions is None:
        pokeball_positions = healer.get("pokeball_positions", [])

    ini_disk = state.objects_dict["disk"]["ini_index"]
    end_disk = state.objects_dict["disk"]["end_index"]

    '''
    ===========================================
    DESENHANDO O CORPO DO HEALER
    ===========================================
    '''
    #base superior
    healer_color = healer["colors"]["upper_base"]

    mat_transform = healer_transform(pos, angulo, [0.0, 0.0, 0.0], [2.0*scale, 0.4*scale, 3.0*scale])
    draw_cube(mat_transform, healer_color)


    #base central
    healer_color = healer["colors"]["middle_base"]

    mat_transform = healer_transform(pos, angulo, [0.03*scale, -0.5*scale, 0.0], [1.95*scale, 0.1*scale, 2.90*scale])
    draw_cube(mat_transform, healer_color)

    #base inferior
    healer_color = healer["colors"]["lower_base"]

    mat_transform = healer_transform(pos, angulo, [0.0, -0.9*scale, 0.0], [2.0*scale, 0.4*scale, 3.0*scale])
    draw_cube(mat_transform, healer_color)



    '''
    ===========================================
    DESENHANDO A PARTE DE CIMA DO HEALER
    ===========================================
    '''

    # Placa azul em cima
    blue_color = healer["colors"]["top_plate"]

    mat_transform = healer_transform(pos, angulo, [0.0, 0.43*scale, 0.0], [1.8*scale, 0.05*scale, 2.8*scale])
    draw_cube(mat_transform, blue_color)

    '''
    ===========================================
    DISCOS NAS POSIÇÕES DAS POKEBOLAS (SOMBRA FAKE)
    ===========================================
    '''
    disk_color = [healer["colors"]["pokeball_shadow"]] * ((end_disk - ini_disk) // 3)

    for pb_pos in pokeball_positions:
        mat_transform = mat_identidade()
        mat_transform = multiplica_matriz(mat_transform, mat_translacao(pb_pos[0], pb_pos[1]-0.08, pb_pos[2]))
        mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(-angulo))
        mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo))
        mat_transform = multiplica_matriz(mat_transform, mat_escala(0.09, 0.09, 0.09))
        draw_generic_object(ini_disk, end_disk, mat_transform, disk_color)

from matrix_operations import *
from .utils import *
import state

def base_pokeball_transform(pos, angulos):
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(angulos[0])))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(math.radians(angulos[1])))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_z(math.radians(angulos[2])))
    return mat_transform

def apply_opening_rotation(mat_transform, opening_angle,scale):
    hinge_z = 0.9 * scale

    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0, 0, +hinge_z))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(opening_angle)))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0, 0, -hinge_z))

    return mat_transform

def create_pokeball(angulos=None, pos=None, scale=None, color_name=None, open=None, opening_angle=None, rotation_angle=None):
    pokeball = state.properties["pokeball"]

    
    if angulos is None:
        angulos = pokeball["angles"]
    if pos is None:
        pos = pokeball["position"]
    if scale is None:
        scale = pokeball["scale"]
    if color_name is None:
        colors_model = pokeball["colors"]['normal']
    else: 
        colors_model = pokeball['colors'][color_name]
    if open is None:
        open = pokeball.get("open", False)
    if opening_angle is None:
        opening_angle = 0

    ini_semisphere = state.objects_dict["semi_sphere"]["ini_index"]
    end_semisphere = state.objects_dict["semi_sphere"]["end_index"]

    ini_ring = state.objects_dict["ring"]["ini_index"]
    end_ring = state.objects_dict["ring"]["end_index"]

    ini_disk = state.objects_dict["disk"]["ini_index"]
    end_disk = state.objects_dict["disk"]["end_index"]

    if not isinstance(open, bool):
        raise TypeError("O parametro 'open' deve ser bool.")

    '''
    ===========================================
    DESENHANDO A PARTE DE CIMA DA POKEBOLA
    ===========================================
    '''

    mat_transform = base_pokeball_transform(pos, angulos)
    if rotation_angle: mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(math.radians(rotation_angle)))
    mat_transform = apply_opening_rotation(mat_transform, opening_angle, scale)
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0, 0.05*scale, 0))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(scale, scale, scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(90)))


    color_vector = [colors_model["upBall"]] * ((end_semisphere - ini_semisphere) // 3)
    
    draw_generic_object(ini_semisphere, end_semisphere, mat_transform, color_vector)



    '''
    ===========================================
    DESENHANDO A PARTE DE BAIXO DAS POKEBOLA
    ===========================================
    '''
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(angulos[0])))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(math.radians(angulos[1])))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_z(math.radians(angulos[2])))
    if rotation_angle: mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(math.radians(rotation_angle)))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0, -0.05*scale, 0)) # transladada levemente para BAIXO
    mat_transform = multiplica_matriz(mat_transform, mat_escala(scale, scale, scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(-math.radians(90)))

    color_vector = [colors_model["downBall"]] * ((end_semisphere - ini_semisphere) // 3)
    
    draw_generic_object(ini_semisphere, end_semisphere, mat_transform, color_vector)


    '''
    ===========================================
    DESENHANDO O ANEL PRETO CENTRAL
    ===========================================
    '''

    ring_scale = 0.98  # ajusta o raio do anel ao raio da semiesfera
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(angulos[0])))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(math.radians(angulos[1])))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_z(math.radians(angulos[2])))
    if rotation_angle: mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(math.radians(rotation_angle)))
    mat_transform = multiplica_matriz(mat_transform, mat_escala(ring_scale*scale, ring_scale*scale, ring_scale*scale))

    color_vector = [colors_model["ring"]] * ((end_ring - ini_ring) // 3)
    
    draw_generic_object(ini_ring, end_ring, mat_transform, color_vector)

    '''
    ===========================================
    DESENHANDO O DISCO PRETO
    ===========================================
    '''
    disk_scale = 0.25
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(angulos[0])))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(math.radians(angulos[1])))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_z(math.radians(angulos[2])))
    if rotation_angle: mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(math.radians(rotation_angle)))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0, 0, -scale))  # traz para frente da pokebola
    mat_transform = multiplica_matriz(mat_transform, mat_escala(disk_scale*scale, disk_scale*scale, disk_scale*scale))  # ajusta para um tamanho proporcional
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(90)))

    color_vector = [colors_model["outerDisk"]] * ((end_disk - ini_disk) // 3)
    draw_generic_object(ini_disk, end_disk, mat_transform, color_vector)



    '''
    ===========================================
    DESENHANDO O DISCO BRANCO
    ===========================================
    '''
    white_disk_scale = disk_scale*0.65
    mat_transform = mat_identidade()
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(pos[0], pos[1], pos[2]))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(angulos[0])))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(math.radians(angulos[1])))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_z(math.radians(angulos[2])))
    if rotation_angle: mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(math.radians(rotation_angle)))
    mat_transform = multiplica_matriz(mat_transform, mat_translacao(0, 0, -scale-0.005)) # traz para a frente da pokebola e poucos pixels a frente do disco preto
    mat_transform = multiplica_matriz(mat_transform, mat_escala(white_disk_scale*scale, white_disk_scale*scale, white_disk_scale*scale))
    mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(math.radians(90)))

    color_vector = [colors_model["innerdisk"]] * ((end_disk - ini_disk) // 3)
    draw_generic_object(ini_disk, end_disk, mat_transform, color_vector)

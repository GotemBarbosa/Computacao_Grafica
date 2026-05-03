import glfw
from OpenGL.GL import *
import state
import numpy as np
import glm
import random
#from scene_objects import desenha_caixa, desenha_jeep, desenha_ground, desenha_sky, desenha_house, desenha_fogueira, desenha_planeta, desenha_moon
from scene_objects import *
from utils.coordenates import planet_to_world_coordenates, get_rotation_angle_from_planet

import warnings
from PIL import Image

warnings.simplefilter('ignore', Image.DecompressionBombWarning)


def draw_ground_grid():
    base_x = -4
    base_y = -62.5
    base_z = -8
    scale_x = 2
    scale_y = 2
    scale_z = 2

    # O OBJ do chão mede 5x5; com escala 2, cada peça ocupa 10x10 unidades.
    tile_size = 10
    grid_radius = 4

    for offset_x in range(-grid_radius, grid_radius + 1):
        for offset_z in range(-grid_radius, grid_radius + 1):
            desenha_ground(
                angle=0,
                r_x=0, r_y=1, r_z=0,
                t_x=base_x + offset_x * tile_size,
                t_y=base_y,
                t_z=base_z + offset_z * tile_size,
                s_x=scale_x, s_y=scale_y, s_z=scale_z
            )


def movement():
    state.camera_speed = 10 * state.deltaTime
    right = glm.normalize(glm.cross(state.cameraFront, state.cameraUp))


    if state.keys.get(glfw.KEY_LEFT_SHIFT, False):
        speed_factor = 5
    else: 
        speed_factor = 1

    # Movimento horizontal (sempre roda)
    if state.keys.get(glfw.KEY_W, False):
        if state.flyMode:
            state.cameraPos += state.camera_speed * speed_factor * state.cameraFront
        else:
            state.cameraPos += state.camera_speed * speed_factor * state.planetFoward

    if state.keys.get(glfw.KEY_S, False):
        if state.flyMode:
            state.cameraPos -= state.camera_speed * state.cameraFront
        else:
            state.cameraPos -= state.camera_speed * state.planetFoward

    if state.keys.get(glfw.KEY_A, False):
        if state.flyMode or not state.planetActivated:
            state.cameraPos -= state.camera_speed * speed_factor * right
        else:
            state.cameraPos -= state.camera_speed * speed_factor * state.planetRight

    if state.keys.get(glfw.KEY_D, False):
        if state.flyMode or not state.planetActivated:
            state.cameraPos += state.camera_speed * speed_factor * right
        else:
            state.cameraPos += state.camera_speed * speed_factor * state.planetRight

    if not state.flyMode:


        if not state.masterMode:
            # ==========================================================
            # 1. GRAVIDADE UNIFICADA MISTURADA
            # ==========================================================
            # A gravidade sempre aponta na direção oposta ao planetUp atual (que pode ser suavizado)
            state.gravity = -state.planetUp * state.gravityStrength
            
            # Só aplica essa gravidade se o player não está no chão
            if not state.isOnGround:
                state.velocity += state.gravity * state.deltaTime

            state.cameraPos += state.velocity * state.deltaTime

            # Todo frames nós assumimos que o player está no ar, se ele bater no chão mudamos pra True
            state.isOnGround = False


            # ==========================================================
            # 2. COLISÃO COM O PLANETA (Esfera)
            # ==========================================================
            if glm.dot(state.velocity, state.planetUp) <= 0.0:
                distanceToCenter = glm.length(state.cameraPos - state.planetCenter)
                if distanceToCenter <= state.planetRadius + 0.005:
                    normal = glm.normalize(state.cameraPos - state.planetCenter)
                    state.cameraPos = state.planetCenter + normal * state.planetRadius
                    state.velocity = glm.vec3(0.0, 0.0, 0.0)
                    state.isOnGround = True


            # ==========================================================
            # 3. COLISÃO COM A PLATAFORMA (Plano)
            # ==========================================================
            if state.velocity.y <= 0.0:
                piso_s_x, piso_s_z = 6.15, 10.086
                dx, dy, dz = abs(state.cameraPos.x), abs(state.cameraPos.y), abs(state.cameraPos.z)
                if ((dx < piso_s_x) and (dz < piso_s_z) and (dy < 5)):

                    # Verifica se caímos abaixo da altura da plataforma, 0.005 é só uma margem de tolerância
                    if state.cameraPos.y <= state.groundHeight + 0.005:
                        state.cameraPos.y = state.groundHeight
                        state.velocity = glm.vec3(0.0, 0.0, 0.0)
                        state.isOnGround = True
        
        if state.masterMode:
            state.gravity =  glm.vec3(0.0, -1.0, 0.0) * state.gravityStrength
            state.velocity += state.gravity * state.deltaTime
            state.cameraPos += state.velocity * state.deltaTime
            if state.cameraPos.y <= state.groundHeight:
                state.cameraPos.y = state.groundHeight
                state.velocity = glm.vec3(0.0, 0.0, 0.0)
                state.isOnGround = True 

    

forest_positions = [
            # anel interno (lat 78) — 6 árvores
            (78,   0, 1.0),
            (78,  60, 1.1),
            (78, 120, 0.9),
            (78, 180, 1.0),
            (78, 240, 1.1),
            (78, 300, 0.9),

            # anel do meio (lat 72) — 8 árvores, deslocadas
            (72,  30, 1.2),
            (72,  75, 0.8),
            (72, 120, 1.0),
            (72, 165, 1.1),
            (72, 210, 0.9),
            (72, 255, 1.2),
            (72, 300, 1.0),
            (72, 345, 0.85),

            # anel externo (lat 66) — 6 árvores
            (66,  15, 1.0),
            (66,  75, 1.1),
            (66, 135, 0.9),
            (66, 195, 1.05),
            (66, 255, 1.0),
            (66, 315, 1.1),
        ]



def trilha_forja():
    for pos_p, tile_rot in cache_trilha_forja:
        desenha_rockTiles(
            angle=-60, r_x=0, r_y=1, r_z=0,
            t_x=pos_p.x, t_y=pos_p.y, t_z=pos_p.z,
            s_x=0.7, s_y=0.7, s_z=0.7,
            planet_rotation_matrix=tile_rot
        )


arvores_planeta_positions = [
    # (lat, lon, escala) — espalhadas pelo planeta, evitando polos, casa, forja e trilha
    ( 40,  10, 1.0),
    ( -30, 70, 1.0),
    ( 30, 200, 0.9),
    ( 20, 270, 1.1),
    ( 10, 330, 1.0),
    (  5, 150, 0.85),
    (-10, 250, 1.05),
    (-20, 180, 1.0),
    (-35, 300, 0.95),
    (-45,  20, 1.1),
    (-50, 130, 0.9),
    (-60, 220, 1.0),
    (-25,   0, 0.95),
]


def arvores_planeta():
    # Agora é instantâneo! Sem trigonometria no frame.
    for pos_tree, tree_rot, escala in cache_arvores_planeta:
        desenha_pineTree(
            angle=0, r_x=0, r_y=0, r_z=0,
            t_x=pos_tree.x, t_y=pos_tree.y, t_z=pos_tree.z,
            s_x=escala, s_y=escala, s_z=escala,
            planet_rotation_matrix=tree_rot
        )


def floresta():
    for pos_tree, tree_rot, escala in cache_floresta_arvores:
        desenha_pineTree(
            angle=0, r_x=0, r_y=0, r_z=0,
            t_x=pos_tree.x, t_y=pos_tree.y, t_z=pos_tree.z,
            s_x=escala, s_y=escala, s_z=escala,
            planet_rotation_matrix=tree_rot
        )

    # FOGUEIRA NO CENTRO DA FLORESTA
    pos_fogueira_polo = planet_to_world_coordenates(
        lat=90,
        lon=0,
        radius=state.planetRadius - 1.8,
        center=state.planetCenter
    )
    fogueira_polo_rot = get_rotation_angle_from_planet(pos_fogueira_polo, state.planetCenter)

    desenha_fogueira(
        angle=0,
        r_x=0, r_y=1, r_z=0,
        t_x=pos_fogueira_polo.x, t_y=pos_fogueira_polo.y, t_z=pos_fogueira_polo.z,
        s_x=1, s_y=1, s_z=1,
        planet_rotation_matrix=fogueira_polo_rot
    )

    # TRONCOS AO REDOR DA FOGUEIRA 
    troncos_polo = [
        (86,   0),
        (86, 120),
        (86, 240),
    ]
    for lat_t, lon_t in troncos_polo:
        pos_t = planet_to_world_coordenates(
            lat=lat_t,
            lon=lon_t,
            radius=state.planetRadius - 2.34,
            center=state.planetCenter
        )
        tronco_rot = get_rotation_angle_from_planet(pos_t, state.planetCenter)

        desenha_treeStump(
            angle=0,
            r_x=0, r_y=0, r_z=0,
            t_x=pos_t.x, t_y=pos_t.y, t_z=pos_t.z,
            s_x=0.3, s_y=0.3, s_z=0.3,
            planet_rotation_matrix=tronco_rot
        )

def fogueira_casa():
    pos_fogueira_casa = planet_to_world_coordenates(
        lat=-15,
        lon=100,
        radius=state.planetRadius - 1.8,
        center=state.planetCenter
    )
    fogueira_casa_rot = get_rotation_angle_from_planet(pos_fogueira_casa, state.planetCenter)

    desenha_fogueira(
        angle=0,
        r_x=0, r_y=1, r_z=0,
        t_x=pos_fogueira_casa.x, t_y=pos_fogueira_casa.y, t_z=pos_fogueira_casa.z,
        s_x=1, s_y=1, s_z=1,
        planet_rotation_matrix=fogueira_casa_rot
    )
    #troncos em volta
    troncos_casa = [
        (-13, 100),
        (-16, 98),
        (-16, 102),
    ]
    for lat_tc, lon_tc in troncos_casa:
        pos_tc = planet_to_world_coordenates(
            lat=lat_tc,
            lon=lon_tc,
            radius=state.planetRadius - 2.34,
            center=state.planetCenter
        )
        tronco_casa_rot = get_rotation_angle_from_planet(pos_tc, state.planetCenter)

        desenha_treeStump(
            angle=0,
            r_x=0, r_y=0, r_z=0,
            t_x=pos_tc.x, t_y=pos_tc.y, t_z=pos_tc.z,
            s_x=0.3, s_y=0.3, s_z=0.3,
            planet_rotation_matrix=tronco_casa_rot
        )


def foguete():
    # FOGUETE — sobe/desce com setas até um limite ============================

    #atualiza o offset vertical com base nas flags setadas em key_event
    if state.rocket_going_up:
        state.rocket_offset += state.rocket_speed * state.deltaTime
    if state.rocket_going_down:
        state.rocket_offset -= state.rocket_speed * state.deltaTime

    #nunca abaixo do solo, nem acima do limite
    state.rocket_offset = max(0.0, min(state.rocket_max_height, state.rocket_offset))

    #posição base na superfície do planeta
    pos_base = planet_to_world_coordenates(
        lat=-15,
        lon=115,
        radius=state.planetRadius - 2.1,
        center=state.planetCenter
    )

    #desloca ao longo da normal da superfície (= "pra cima" local)
    normal = glm.normalize(pos_base - state.planetCenter)
    pos_rocket = pos_base + normal * state.rocket_offset

    rocket_rot = get_rotation_angle_from_planet(pos_rocket, state.planetCenter)

    #translação entra na matriz model via t_x/t_y/t_z
    desenha_rocket(
        angle=0,
        r_x=0, r_y=0, r_z=0,
        t_x=pos_rocket.x, t_y=pos_rocket.y, t_z=pos_rocket.z,
        s_x=0.5, s_y=0.5, s_z=0.5,
        planet_rotation_matrix=rocket_rot
    )


def marte():
    # MARTE — escala controlável com E (aumentar) e Q (diminuir) ==================

    if state.mars_scaling_up:
        state.mars_scale += state.mars_scale_speed * state.deltaTime
    if state.mars_scaling_down:
        state.mars_scale -= state.mars_scale_speed * state.deltaTime

    # clamp pra não sumir nem explodir
    state.mars_scale = max(5.0, min(500.0, state.mars_scale))

    desenha_planet(
        angle=0,
        r_x=0, r_y=1, r_z=0,
        t_x=200, t_y=100, t_z=-250,
        s_x=state.mars_scale, s_y=state.mars_scale, s_z=state.mars_scale,
        texture_id=state.mars_texture_id
    )


def telescopio():
    # TELESCÓPIO — gira em torno do eixo "up" local com setas ==================

    # atualiza yaw com base nas flags setadas em key_event
    if state.telescope_turning_left:
        state.telescope_yaw -= state.telescope_yaw_speed * state.deltaTime
    if state.telescope_turning_right:
        state.telescope_yaw += state.telescope_yaw_speed * state.deltaTime

    pos_telescope = planet_to_world_coordenates(
        lat=-30,
        lon=90,
        radius=state.planetRadius - 2.1,
        center=state.planetCenter
    )
    telescope_rot = get_rotation_angle_from_planet(pos_telescope, state.planetCenter)

    # ângulo base (190) + yaw controlado pelo usuário, em torno do eixo Y local
    desenha_telescope(
        angle=190 + state.telescope_yaw,
        r_x=0, r_y=1, r_z=0,
        t_x=pos_telescope.x, t_y=pos_telescope.y, t_z=pos_telescope.z,
        s_x=0.04, s_y=0.04, s_z=0.04,
        planet_rotation_matrix=telescope_rot
    )


def satelite():
    # SATELITE — orbita o planeta variando a longitude com o tempo ================

    # avança o ângulo da órbita
    state.satelite_orbit_angle += state.satelite_orbit_speed * state.deltaTime
    state.satelite_orbit_angle %= 360.0

    # posição na órbita: lat fixa (inclinação), lon = ângulo atual
    pos_satelite = planet_to_world_coordenates(
        lat=state.satelite_orbit_lat,
        lon=state.satelite_orbit_angle,
        radius=state.planetRadius + state.satelite_orbit_radius,
        center=state.planetCenter
    )

    satelite_rot = get_rotation_angle_from_planet(pos_satelite, state.planetCenter)

    desenha_satelite(
        angle=-90,
        r_x=0, r_y=1, r_z=0,
        t_x=pos_satelite.x, t_y=pos_satelite.y, t_z=pos_satelite.z,
        s_x=1, s_y=1, s_z=1,
        planet_rotation_matrix=satelite_rot
    )





# ==========================================================
# CACHE DE OBJETOS ESTÁTICOS
# ==========================================================
cache_arvores_planeta = []
cache_floresta_arvores = []
cache_trilha_forja = []

def init_objetos_estaticos():
    global cache_arvores_planeta, cache_floresta_arvores, cache_trilha_forja
    import math

    # 1. Pré-calcula Árvores do Planeta
    for lat, lon, escala in arvores_planeta_positions:
        pos_tree = planet_to_world_coordenates(lat, lon, state.planetRadius - 2.3, state.planetCenter)
        tree_rot = get_rotation_angle_from_planet(pos_tree, state.planetCenter)
        # Guarda a posição e a matriz pronta numa tupla
        cache_arvores_planeta.append((pos_tree, tree_rot, escala))

    # 2. Pré-calcula Floresta
    for lat, lon, escala in forest_positions:
        pos_tree = planet_to_world_coordenates(lat, lon, state.planetRadius - 2.3, state.planetCenter)
        tree_rot = get_rotation_angle_from_planet(pos_tree, state.planetCenter)
        cache_floresta_arvores.append((pos_tree, tree_rot, escala))

    # 3. Pré-calcula Trilha da Forja
    n_tiles = 30
    lat_ini, lon_ini = -15, 90   
    lat_fim, lon_fim = -30, 45  
    for i in range(n_tiles):
        t = i / (n_tiles - 1)
        lat_base = lat_ini + t * (lat_fim - lat_ini)
        lon_base = lon_ini + t * (lon_fim - lon_ini)
        offset_lat = 2.5 * math.sin(i * 0.9) + 1.2 * math.cos(i * 2.1)
        offset_lon = 3.5 * math.cos(i * 0.7) + 1.5 * math.sin(i * 1.8)
        
        pos_p = planet_to_world_coordenates(lat_base + offset_lat, lon_base + offset_lon, state.planetRadius - 2.1, state.planetCenter)
        tile_rot = get_rotation_angle_from_planet(pos_p, state.planetCenter)
        cache_trilha_forja.append((pos_p, tile_rot))


def draw_scene():
    glfw.swap_interval(1)
    state.lastFrame = glfw.get_time()

    init_objetos_estaticos()
    while not glfw.window_should_close(state.window):


        currentFrame = glfw.get_time()
        state.deltaTime = currentFrame - state.lastFrame
        state.lastFrame = currentFrame


        # --- CÁLCULO DE FPS AQUI ---
        state.nb_frames += 1
        # Se passou 1 segundo (ou mais) desde a última medição...
        if currentFrame - state.last_time >= 1.0: 
            fps = state.nb_frames # O número de frames acumulados é o FPS
            
            # Atualiza o título da janela
            glfw.set_window_title(state.window, f"Meu Motor 3D - FPS: {fps}")
            
            # Reseta os contadores para o próximo segundo
            state.nb_frames = 0
            state.last_time += 1.0



        state.update_move_front_camera()     
        movement()
    
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.15, 0.15, 0.2, 1.0)

        # malha poligonal (P): GL_LINE = só arestas, GL_FILL = preenchido (default)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if state.wireframe_mode else GL_FILL)

        #carrega view
        mat_view = state.view()
        glUniformMatrix4fv(state.loc_view, 1, GL_TRUE, mat_view)

        #carrega projection
        mat_projection = state.projection()
        glUniformMatrix4fv(state.loc_projection, 1, GL_TRUE, mat_projection)

        #posiciona os objetos

        desenha_sky(
            angle=0,
            r_x=0, r_y=0, r_z=0,
            t_x=0, t_y=0, t_z=0,
            s_x=300, s_y=300, s_z=300
        )

        desenha_caixa(state.obj_angle, 
                      r_x=0, r_y=1, r_z=0, 
                      t_x=-5.5, t_y=-60.7, t_z=-5.5, 
                      s_x=0.8, s_y=0.8, s_z=0.8, 
                      texture_id=state.texture_id)
        # Casa ======================================
        pos_cartoonHouse = planet_to_world_coordenates(
            lat=0, 
            lon=90, 
            radius=state.planetRadius-2.3, 
            center=state.planetCenter
        )

        cartoonHouse_rotation_matrix = get_rotation_angle_from_planet(pos_cartoonHouse, state.planetCenter)

        desenha_cartoonHouse(
            angle=0,
            r_x=0, r_y=0, r_z=0,
            t_x=pos_cartoonHouse.x, t_y=pos_cartoonHouse.y, t_z=pos_cartoonHouse.z,
            s_x=1.6, s_y=1.6, s_z=1.6,
            planet_rotation_matrix=cartoonHouse_rotation_matrix
        )

        piso_s_x, piso_s_y, piso_s_z = 6.1, 0.8, 10.086
        margin = 4.0
        #print(state.cameraPos)
        if not state.masterMode:
            dx = abs(state.cameraPos.x)
            dy = abs(state.cameraPos.y)
            dz = abs(state.cameraPos.z)

            if ((dx < piso_s_x) and (dz < piso_s_z) and (dy < 5)):
                state.gravity_weight = 0.0
                #print(f"cam.y: {state.cameraPos.y}, g_height: {state.groundHeight}, state: {state.isOnGround}")

            # saindo da area de suavização de gravidades
            elif (dx > (piso_s_x + margin) or dz > (piso_s_z + margin) or dy > 5):
                state.gravity_weight = 1.0

            # zona de suavização da transição de gravidades.
            # Ele irá fazer uma "mistura" da gravidade do piso com a gravidade do planeta (0.0 a 1.0)
            else:
                weight_x = (dx - piso_s_x) / margin if dx > piso_s_x else 0.0
                weight_z = (dz - piso_s_z) / margin if dz > piso_s_z else 0.0
                raw_weight = max(weight_x, weight_z) # 0.0 a 1.0 --> Fala o quão longe estamos do piso
            
                # Aplica uma curva "Smoothstep" para a transição ficar suave
                # --> Essa curva smoothstep parece ser padrão para suavizar movimentos em jogos (muito melhor que liner)
                # 3x^2 - 2x^3
                state.gravity_weight = raw_weight * raw_weight * (3.0 - 2.0 * raw_weight)


        # PISO ======================================
        desenha_caixa(state.obj_angle, 
                      r_x=0, r_y=1, r_z=0, 
                      t_x=0, t_y=-2.75, t_z=0.78, 
                      s_x=piso_s_x, s_y=piso_s_y, s_z=piso_s_z, 
                      texture_id=state.woodPlanks_texture_id)    
        
        desenha_caixa(state.obj_angle, 
                      r_x=0, r_y=1, r_z=0, 
                      t_x=0, t_y=-3.5, t_z=0.78, 
                      s_x=piso_s_x+0.7, s_y=piso_s_y, s_z=piso_s_z+0.7, 
                      texture_id=state.woodPlanks_texture_id)    

        # JEEP ======================================
        pos_jeep = planet_to_world_coordenates(
            lat=-62.5, 
            lon=-8, 
            radius=state.planetRadius - 2.2, 
            center=state.planetCenter
        )
        
        jeep_rotation_matrix = get_rotation_angle_from_planet(pos_jeep, state.planetCenter)


        desenha_jeep(
            angle=180,
            r_x=0, r_y=1, r_z=0,
            t_x=pos_jeep.x, t_y=pos_jeep.y, t_z=pos_jeep.z,
            s_x=2, s_y=2, s_z=2,
            planet_rotation_matrix=jeep_rotation_matrix
        )

        # ORGANIZANDO ITENS DE INTERESSE NO PLANETA
        trilha_forja()
        floresta()
        fogueira_casa()
        arvores_planeta()


        # FOGUETE  ======================================
        foguete()

        '''
        # MESA ======================================
        pos_table = planet_to_world_coordenates(
            lat=-0, 
            lon=85, 
            radius=state.planetRadius-1.3, 
            center=state.planetCenter
        )

        table_rotation_matrix = get_rotation_angle_from_planet(pos_table, state.planetCenter)
        
        desenha_table(
            angle=90,
            r_x=0, r_y=1, r_z=0,
            t_x=pos_table.x, t_y=pos_table.y, t_z=pos_table.z,
            s_x=0.017, s_y=0.017, s_z=0.017,
            planet_rotation_matrix=table_rotation_matrix
        )
        '''
        # TELESCÓPIO ======================================
        telescopio()

        # FORJA ======================================
        pos_forge = planet_to_world_coordenates(
            lat=-30, 
            lon=45, 
            radius=state.planetRadius-1.8, 
            center=state.planetCenter
        )

        forge_rotation_matrix = get_rotation_angle_from_planet(pos_forge, state.planetCenter)

        desenha_forge(
            angle=-90,
            r_x=0, r_y=1, r_z=0,
            t_x=pos_forge.x, t_y=pos_forge.y, t_z=pos_forge.z,
            s_x=1, s_y=1, s_z=1,
            planet_rotation_matrix=forge_rotation_matrix
        )

        # PISO FORJA ======================================
        pos_piso_forja = planet_to_world_coordenates(
            lat=-30, 
            lon=45, 
            radius=state.planetRadius-6, 
            center=state.planetCenter
        )

        piso_forja_rotation_matrix = get_rotation_angle_from_planet(pos_piso_forja, state.planetCenter)

        
        desenha_caixa(angle = -90, 
                      r_x=0, r_y=1, r_z=0, 
                      t_x=pos_piso_forja.x+3, t_y=pos_piso_forja.y, t_z=pos_piso_forja.z-3, 
                      s_x=4.5, s_y=0.8, s_z=6, 
                      texture_id=state.woodPlanks_texture_id,
                      planet_rotation_matrix=piso_forja_rotation_matrix) 


        # SATELITE ======================================
        satelite() 
        
        # NAVE DO OUTER WILDS ======================================
        pos_outerWilds = planet_to_world_coordenates(
            lat=-60, 
            lon=110, 
            radius=state.planetRadius+0.5, 
            center=state.planetCenter
        )

        outerWilds_rotation_matrix = get_rotation_angle_from_planet(pos_outerWilds, state.planetCenter)

        desenha_outerWilds(angle = 0, 
                      r_x=0, r_y=0, r_z=0, 
                      t_x=pos_outerWilds.x, t_y=pos_outerWilds.y, t_z=pos_outerWilds.z, 
                      s_x=2, s_y=2, s_z=2, 
                      planet_rotation_matrix=outerWilds_rotation_matrix) 
        
        desenha_wallBox(angle = 90, 
                      r_x=0, r_y=1, r_z=0, 
                      t_x=0, t_y=0.35, t_z=7.8, 
                      s_x=0.46, s_y=0.46, s_z=0.46) 


        # LUA ======================================
        desenha_planet(
            angle=180,
            r_x=0, r_y=1, r_z=0,
            t_x=0, t_y=-48, t_z=0,
            s_x=46, s_y=46, s_z=46, texture_id=state.moon_texture_id
        )

        # PLANETA DISTANTE (Marte) ======================================
        marte()

        #draw_ground_grid()

        glfw.swap_buffers(state.window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    draw_scene()

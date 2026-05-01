import glfw
from OpenGL.GL import *
import state
import numpy as np
import glm
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
                piso_s_x, piso_s_z = 5.0, 8.2
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

    

def draw_scene():
    glfw.swap_interval(1)
    state.lastFrame = glfw.get_time()

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
            s_x=1.3, s_y=1.3, s_z=1.3,
            planet_rotation_matrix=cartoonHouse_rotation_matrix
        )

        piso_s_x, piso_s_y, piso_s_z = 5.0, 0.8, 8.2
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
                      t_x=0, t_y=-2.8, t_z=0.5, 
                      s_x=piso_s_x, s_y=piso_s_y, s_z=piso_s_z, 
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

        # FOGUEIRA ======================================

        pos_fogueira = planet_to_world_coordenates(
            lat=-15, 
            lon=90, 
            radius=state.planetRadius-1.8, 
            center=state.planetCenter
        )

        fogueira_rotation_matrix = get_rotation_angle_from_planet(pos_fogueira, state.planetCenter)

        desenha_fogueira(
            angle=180,
            r_x=0, r_y=1, r_z=0,
            t_x=pos_fogueira.x, t_y=pos_fogueira.y, t_z=pos_fogueira.z,
            s_x=1, s_y=1, s_z=1,
            planet_rotation_matrix=fogueira_rotation_matrix
        )

        # ARVORE ======================================
        pos_pineTree = planet_to_world_coordenates(
            lat=-30, 
            lon=90, 
            radius=state.planetRadius-2.3, 
            center=state.planetCenter
        )

        pineTree_rotation_matrix = get_rotation_angle_from_planet(pos_pineTree, state.planetCenter)

        desenha_pineTree(
            angle=0,
            r_x=0, r_y=0, r_z=0,
            t_x=pos_pineTree.x, t_y=pos_pineTree.y, t_z=pos_pineTree.z,
            s_x=1, s_y=1, s_z=1,
            planet_rotation_matrix=pineTree_rotation_matrix
        )

        # FOGUETE  ======================================
        pos_rocket = planet_to_world_coordenates(
            lat=-25, 
            lon=120, 
            radius=state.planetRadius-2.1, 
            center=state.planetCenter
        )

        rocket_rotation_matrix = get_rotation_angle_from_planet(pos_rocket, state.planetCenter)

        desenha_rocket(
            angle=0,
            r_x=0, r_y=0, r_z=0,
            t_x=pos_rocket.x, t_y=pos_rocket.y, t_z=pos_rocket.z,
            s_x=0.5, s_y=0.5, s_z=0.5,
            planet_rotation_matrix=rocket_rotation_matrix
        )

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

        # TELESCÓPIO ======================================
        pos_telescope = planet_to_world_coordenates(
            lat=-30, 
            lon=105, 
            radius=state.planetRadius-2.1, 
            center=state.planetCenter
        )

        telescope_rotation_matrix = get_rotation_angle_from_planet(pos_telescope, state.planetCenter)

        desenha_telescope(
            angle=190,
            r_x=0, r_y=1, r_z=0,
            t_x=pos_telescope.x, t_y=pos_telescope.y, t_z=pos_telescope.z,
            s_x=0.04, s_y=0.04, s_z=0.04,
            planet_rotation_matrix=telescope_rotation_matrix
        )

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

        pos_satelite = planet_to_world_coordenates(
            lat=-30, 
            lon=45, 
            radius=state.planetRadius+30, 
            center=state.planetCenter
        )

        satelite_rotation_matrix = get_rotation_angle_from_planet(pos_satelite, state.planetCenter)

        desenha_satelite(angle = -90, 
                      r_x=0, r_y=1, r_z=0, 
                      t_x=pos_satelite.x, t_y=pos_satelite.y, t_z=pos_satelite.z, 
                      s_x=1, s_y=1, s_z=1, 
                      planet_rotation_matrix=satelite_rotation_matrix) 


        # LUA ======================================
        desenha_planet(
            angle=180,
            r_x=0, r_y=1, r_z=0,
            t_x=0, t_y=-48, t_z=0,
            s_x=46, s_y=46, s_z=46, texture_id=state.moon_texture_id
        )

        #draw_ground_grid()

        glfw.swap_buffers(state.window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    draw_scene()

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
        if state.planetActivated:
            # Calcula a direção da gravidade e atualiza a velocidade/pos do player (pra onde o player anda para baixo)
            gravityDir = glm.normalize(state.planetCenter - state.cameraPos)
            state.gravity = gravityDir * state.gravityStrength
            state.velocity += state.gravity * state.deltaTime
            state.cameraPos += state.velocity * state.deltaTime

            # verifica se entraria dentro do planeta
            distanceToCenter = glm.length(state.cameraPos - state.planetCenter)
            if distanceToCenter <= state.planetRadius:
                # projeta de volta pra superfície
                normal = glm.normalize(state.cameraPos - state.planetCenter) # é contrário a gravidade (normal ao planeta)
                state.cameraPos = state.planetCenter + normal * state.planetRadius # Coloca o player na superficie

                # ajusta a velocidade para zero pois não está mais "caindo"
                state.velocity = glm.vec3(0.0, 0.0, 0.0)
                state.isOnGround = True

            # Está no ar caindo, mantém as modificações de posição calculadas
            else:
                state.isOnGround = False



        # Caso o planeta não esteja ativado entra no modo de "mundo plano"
        else: 
            state.velocity.y += state.gravity.y * state.gravityStrength * state.deltaTime
            state.cameraPos.y += state.velocity.y * state.deltaTime

            if state.cameraPos.y <= state.groundHeight:
                state.cameraPos.y = state.groundHeight
                state.velocity.y = 0.0
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

        pos_house = planet_to_world_coordenates(
            lat=0, 
            lon=90, 
            radius=state.planetRadius - 3, 
            center=state.planetCenter
        )

        house_rotation_matrix = get_rotation_angle_from_planet(pos_house, state.planetCenter)

        desenha_house(
            angle=180,
            r_x=0, r_y=1, r_z=0,
            t_x=pos_house.x, t_y=pos_house.y, t_z=pos_house.z,
            s_x=0.02, s_y=0.02, s_z=0.02,
            planet_rotation_matrix=house_rotation_matrix
        )

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

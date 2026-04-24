import glfw
from OpenGL.GL import *
import state
import numpy as np
import glm
from scene_objects import desenha_caixa

def movement():
    state.camera_speed = 10 * state.deltaTime
    right = glm.normalize(glm.cross(state.cameraFront, state.cameraUp))

    # Movimento horizontal (sempre roda)
    if state.keys.get(glfw.KEY_W, False):
        if state.flyMode:
            state.cameraPos += state.camera_speed * state.cameraFront
        else:
            state.cameraPos += state.camera_speed * state.cameraMoveFront

    if state.keys.get(glfw.KEY_S, False):
        if state.flyMode:
            state.cameraPos -= state.camera_speed * state.cameraFront
        else:
            state.cameraPos -= state.camera_speed * state.cameraMoveFront

    if state.keys.get(glfw.KEY_A, False):
        state.cameraPos -= state.camera_speed * right

    if state.keys.get(glfw.KEY_D, False):
        state.cameraPos += state.camera_speed * right

    if not state.flyMode:
        state.velocityY += state.gravity * state.deltaTime
        state.cameraPos.y += state.velocityY * state.deltaTime

        if state.cameraPos.y <= state.groundHeight:
            state.cameraPos.y = state.groundHeight
            state.velocityY = 0.0
            state.isOnGround = True

def draw_scene():
    while not glfw.window_should_close(state.window):


        movement()
        currentFrame = glfw.get_time()
        state.deltaTime = currentFrame - state.lastFrame
        state.lastFrame = currentFrame

        state.update_move_front_camera()

    
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.15, 0.15, 0.2, 1.0)

        #carrega view
        mat_view = state.view()
        glUniformMatrix4fv(state.loc_view, 1, GL_TRUE, mat_view)

        #carrega projection
        mat_projection = state.projection()
        glUniformMatrix4fv(state.loc_projection, 1, GL_TRUE, mat_projection)

        #posiciona os objetos
        desenha_caixa(state.obj_angle, 0, 1, 0, 0, 0, -4, 1.2, 1.2, 1.2, state.texture_id)

        glfw.swap_buffers(state.window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    draw_scene()
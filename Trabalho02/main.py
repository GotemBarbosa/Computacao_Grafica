import glfw
from OpenGL.GL import *
import state
import numpy as np
import glm
from scene_objects import desenha_caixa

def draw_scene():
    while not glfw.window_should_close(state.window):

        currentFrame = glfw.get_time()
        state.deltaTime = currentFrame - state.lastFrame
        state.lastFrame = currentFrame

    
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
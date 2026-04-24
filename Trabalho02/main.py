import glfw
from OpenGL.GL import *
import state
import numpy as np
import glm
import math


fov = 45.0

def model():
    m = glm.mat4(1.0)
    m = glm.translate(m, glm.vec3(0.0, 0.0, -4.0))
    m = glm.rotate(m, glm.radians(state.obj_angle), glm.vec3(0.0, 1.0, 0.0))
    m = glm.scale(m, glm.vec3(1.2, 1.2, 1.2))
    return np.array(m, dtype=np.float32)

def view():
    v = glm.lookAt(state.cameraPos, state.cameraPos + state.cameraFront, state.cameraUp)
    return np.array(v, dtype=np.float32)

def projection():
    largura, altura = 700.0, 700.0
    p = glm.perspective(glm.radians(fov), largura / altura, 0.1, 100.0)
    return np.array(p, dtype=np.float32)



def draw_scene():
    while not glfw.window_should_close(state.window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.15, 0.15, 0.2, 1.0)

        mat = np.array([
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        ], np.float32)

        mat_model = model()
        mat_view = view()
        mat_projection = projection()

        glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)
        glUniformMatrix4fv(state.loc_view, 1, GL_TRUE, mat_view)
        glUniformMatrix4fv(state.loc_projection, 1, GL_TRUE, mat_projection)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, state.texture_id)

        ini = state.objects_dict["caixa"]["ini_index"]
        fim = state.objects_dict["caixa"]["end_index"]
        glDrawArrays(GL_TRIANGLES, ini, fim - ini)

        glfw.swap_buffers(state.window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    draw_scene()
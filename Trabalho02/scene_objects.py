import glm
import numpy as np
from OpenGL.GL import *
import state


def desenha_caixa(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, texture_id):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)
    
    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    ini = state.objects_dict["caixa"]["ini_index"]
    fim = state.objects_dict["caixa"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_snow_terrain(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.snow_texture_id)

    ini = state.objects_dict["snowTerrain"]["ini_index"]
    fim = state.objects_dict["snowTerrain"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

# Reúne funções auxiliares de desenho para cubos e objetos genéricos no OpenGL.

from OpenGL.GL import *
import state

def draw_cube(mat_transform, color_vector):
    ini_vertice = state.objects_dict['cube']['ini_index']
    end_vertice = state.objects_dict['cube']['end_index']
    loc_color = state.loc_color
    loc_mat_transform = state.loc_mat_transform

    glUniformMatrix4fv(loc_mat_transform, 1, GL_TRUE, mat_transform) 

    glUniform4f(loc_color, *color_vector[0])
    glDrawArrays(GL_TRIANGLE_STRIP, ini_vertice, 4)
    
    glUniform4f(loc_color, *color_vector[1])
    glDrawArrays(GL_TRIANGLE_STRIP, ini_vertice+4, 4)
    
    glUniform4f(loc_color, *color_vector[2])
    glDrawArrays(GL_TRIANGLE_STRIP, ini_vertice+8, 4)
    
    glUniform4f(loc_color, *color_vector[3])
    glDrawArrays(GL_TRIANGLE_STRIP, ini_vertice+12, 4)
    
    glUniform4f(loc_color, *color_vector[4])
    glDrawArrays(GL_TRIANGLE_STRIP, ini_vertice+16, 4)
    
    glUniform4f(loc_color, *color_vector[5])
    glDrawArrays(GL_TRIANGLE_STRIP, ini_vertice+20, 4)

def draw_generic_object(ini_vertice, end_vertice, mat_transform, color_vector, flag=GL_TRIANGLES):

    loc_color = state.loc_color
    loc_mat_transform = state.loc_mat_transform
    glUniformMatrix4fv(loc_mat_transform, 1, GL_TRUE, mat_transform)

    color_idx = 0

    if flag == GL_TRIANGLES:
        for triangle in range(ini_vertice, end_vertice, 3):
            color = color_vector[color_idx]
            glUniform4f(loc_color, *color)
            glDrawArrays(GL_TRIANGLES, triangle, 3)  # desenha 1 triângulo por vez
            color_idx += 1
    elif flag == GL_TRIANGLE_STRIP:
        color = color_vector[color_idx]
        glUniform4f(loc_color, *color)
        glDrawArrays(GL_TRIANGLE_STRIP, ini_vertice, end_vertice)

from OpenGL.GL import *

def draw_cube(ini_vertice, loc_color, loc_mat_transform, mat_transform, color_vector):

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

def draw_generic_object(ini_vertice, end_vertice, loc_color, loc_mat_transform, mat_transform, color_vector, flag=GL_TRIANGLES):
    glUniformMatrix4fv(loc_mat_transform, 1, GL_TRUE, mat_transform)

    color_idx = 0

    for triangle in range(ini_vertice, end_vertice, 3):
        color = color_vector[color_idx]
        glUniform4f(loc_color, *color)
        glDrawArrays(flag, triangle, 3)  # desenha 1 triângulo por vez
        color_idx += 1

import glfw
from OpenGL.GL import *
import numpy as np
import glm
import math
from shaders.shaders import Shader
from vertices.vertices import  get_cube_vertices, get_semi_sphere_vertices
from matrix_operations import *
import random

def create_window():
    # cria janela
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(700, 700, "Programa", None, None)

    if (window == None):
        print("Failed to create GLFW window")
        glfw.terminate()
    glfw.make_context_current(window)
    return window

def allocate_vertices_on_gpu(raw_vertices, loc_position):

    vertices = np.zeros(len(raw_vertices), [("position", np.float32, 3)])
    vertices["position"] = raw_vertices

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)

    stride = vertices.strides[0]
    offset = ctypes.c_void_p(0)
    glEnableVertexAttribArray(loc_position)
    glVertexAttribPointer(loc_position, 3, GL_FLOAT, False, stride, offset)

    return vertices

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


def draw_semi_sphere(ini_vertice, end_vertice, loc_color, loc_mat_transform, mat_transform, color_vector):

    glUniformMatrix4fv(loc_mat_transform, 1, GL_TRUE, mat_transform)

    color_idx = 0

    for triangle in range(ini_vertice, end_vertice, 3):
        color = color_vector[color_idx]
        glUniform4f(loc_color, *color)
        glDrawArrays(GL_TRIANGLES, triangle, 3)  # desenha 1 triângulo por vez
        color_idx += 1

def draw_scene():
    # cria janela
    window = create_window()

    # cria shaders
    ourShader = Shader("./shaders/vertex_shader.vs", "./shaders/fragment_shader.fs")
    ourShader.use()
    program = ourShader.getProgram()

    loc_position = glGetAttribLocation(program, "position")
    loc_color      = glGetUniformLocation(program, "color")
    loc_mat_transform = glGetUniformLocation(program, "mat_transformation")

    # carrega vértices
    raw_vertices = []
    raw_vertices += get_cube_vertices()
    end_cube = len(raw_vertices)
    cube_centroid = get_centroid(raw_vertices, 0, end_cube)

    raw_vertices += get_semi_sphere_vertices()
    end_red_semi_sphere = len(raw_vertices)
    semi_sphere_centroid = get_centroid(raw_vertices, end_cube, end_red_semi_sphere - end_cube)


    vertices = allocate_vertices_on_gpu(raw_vertices, loc_position)

    scale = 0.05
    angulo_rotacao_cubo = 0 
    angulo_esfera = 0.0
    angulo_abertura = 0.0

    glEnable(GL_DEPTH_TEST)
    glfw.show_window(window)
    # while loop --> Lógica de renderização
    while not glfw.window_should_close(window):
        angulo_esfera += 0.01
        angulo_abertura += 0.05
        angulo_rotacao_cubo -= 0.02 # modifica o angulo de rotacao em cada iteracao

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.15, 0.15, 0.2, 1.0)

        
        
        '''
        ===========================================
        DESENHANDO O CUBO
        ===========================================
        '''
        mat_transform = multiplica_matriz(mat_translacao(0.5, 0.5, 0.5), mat_rotacao_z(angulo_rotacao_cubo))
        mat_transform = multiplica_matriz(mat_transform, mat_rotacao_y(angulo_rotacao_cubo))
        mat_transform = multiplica_matriz(mat_transform, mat_rotacao_x(angulo_rotacao_cubo))
        mat_transform = multiplica_matriz(mat_transform, mat_translacao(-cube_centroid[0], -cube_centroid[1], -cube_centroid[2]))

        color_vector = [[1] * 4 for _ in range(6)]
        color_vector[0] = [1, 0, 0, 1.0] # cor da face 1 --> VERMELHO
        color_vector[1] = [0, 0, 1, 1.0] # cor da face 2 --> AZUL
        color_vector[2] = [0, 1, 0, 1.0] # cor da face 3 --> VERDE
        color_vector[3] = [1, 1, 0, 1.0] # cor da face 4 --> AMARELA
        color_vector[4] = [0.5, 0.5, 0.5, 1.0] # cor da face 5 --> CINZA
        color_vector[5] = [0.5, 0, 0, 1.0] # cor da face 6 --> MARROM

        draw_cube(0, loc_color, loc_mat_transform, mat_transform, color_vector)



        '''
        ===========================================
        DESENHANDO A SEMI ESFERA VERMELHA
        ===========================================
        '''
        mat_transform = mat_rotacao_x(math.radians(90 + angulo_abertura))
        mat_transform = multiplica_matriz(mat_rotacao_y(angulo_esfera), mat_transform)
        mat_transform = multiplica_matriz(mat_transform, mat_translacao(0.0, 0.0, -angulo_abertura/150))
        color_vector = []
        for triangle in range(0, len(vertices), 3):
            random.seed(triangle)   # seed fixo por triângulo — a cor não muda entre frames
            G = random.random()
            B = random.random()
            color_vector.append([1.0, B-0.2, G-0.2, 1.0])

        draw_semi_sphere(end_cube, end_red_semi_sphere, loc_color, loc_mat_transform, mat_transform, color_vector)


        '''
        ===========================================
        DESENHANDO A SEMI ESFERA BRANCA
        ===========================================
        '''
        # generates color:
        color_vector = []
        for triangle in range(0, len(vertices), 3):
            random.seed(triangle)   # seed fixo por triângulo — a cor não muda entre frames
            color_vector.append([1.0, 1.0, 1.0, 1.0])
        mat_transform = mat_rotacao_x(math.radians(-90))
        mat_transform = multiplica_matriz(mat_rotacao_y(angulo_esfera), mat_transform)
        mat_transform = multiplica_matriz(mat_transform, mat_translacao(0.0, 0.0, 0.1))

        draw_semi_sphere(end_cube, end_red_semi_sphere, loc_color, loc_mat_transform, mat_transform, color_vector)



        glfw.swap_buffers(window)
        glfw.poll_events() 

    glfw.terminate()





if __name__ == "__main__":
    draw_scene()
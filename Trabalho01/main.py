
import glfw
from OpenGL.GL import *
import numpy as np
import glm
import math
from shaders.shaders import Shader
from vertices.vertices import *
from matrix_operations import *
import random
from objects.roblox import create_roblox
from objects.pokeball import create_pokeball
from objects.diglett import create_diglett
from objects.healer import create_healer

def create_window():
    # cria janela
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

    #para funcionamento em outros OS (CASO 330)
    #glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    #glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    #glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    #glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

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

    objects_dict = {}

    # carrega vértices de cada objeto
    raw_vertices = []

    # Adiciona um cubo / retangulo /semiesfera
    raw_vertices += get_cube_vertices()
    objects_dict["cube"] = {'ini_index': 0, 
                            'end_index': len(raw_vertices), 
                            'centroid': get_centroid(raw_vertices, 0, len(raw_vertices))}


    # Adiciona um cilindro (deitado)
    raw_vertices += get_cilinder_vertices()
    objects_dict['cilinder'] = {'ini_index': objects_dict["cube"]['end_index'], 
                                'end_index': len(raw_vertices),
                                'centroid': get_centroid(raw_vertices, objects_dict["cube"]['end_index'], len(raw_vertices) - objects_dict["cube"]['end_index'])}
    
    raw_vertices += get_semi_sphere_vertices()
    objects_dict['semi_sphere'] = {'ini_index': objects_dict["cilinder"]['end_index'],
                                'end_index': len(raw_vertices),
                                'centroid': get_centroid(raw_vertices, objects_dict["cilinder"]['end_index'], len(raw_vertices) - objects_dict["cilinder"]['end_index'])}

    raw_vertices += get_ring_vertices()
    objects_dict['ring'] = {'ini_index': objects_dict["semi_sphere"]['end_index'],
                            'end_index': len(raw_vertices),
                            'centroid': get_centroid(raw_vertices, objects_dict["semi_sphere"]['end_index'], len(raw_vertices) - objects_dict["semi_sphere"]['end_index'])}

    raw_vertices += get_disk_vertices()
    objects_dict['disk'] = {'ini_index': objects_dict["ring"]['end_index'],
                            'end_index': len(raw_vertices),
                            'centroid': get_centroid(raw_vertices, objects_dict["ring"]['end_index'], len(raw_vertices) - objects_dict["ring"]['end_index'])}


    # Aloca espaço na GPU para todos os vértices criados
    vertices = allocate_vertices_on_gpu(raw_vertices, loc_position)

    angulo_rotacao_roblox = 0

    glEnable(GL_DEPTH_TEST)
    glfw.show_window(window)

    #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    # while loop --> Lógica de renderização
    while not glfw.window_should_close(window):
        angulo_rotacao_roblox += 0.01

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.15, 0.15, 0.2, 1.0)

        #create_roblox(loc_color, loc_mat_transform, objects_dict, angulo_rotacao_roblox, pos=[-0.8, -0.8, 0.0], scale=0.5)

        #create_roblox(loc_color, loc_mat_transform, objects_dict, -angulo_rotacao_roblox, pos=[0.3, 0.3, 0.0], scale=1)

        pokeball_colors = {}

        pokeball_colors = {}
        pokeball_colors["normal"] = {}
        pokeball_colors["normal"]["upBall"] = [1.0, 0.0, 0.0, 1.0]
        pokeball_colors["normal"]["downBall"] = [1.0, 1.0, 1.0, 1.0]
        pokeball_colors["normal"]["ring"] = [0.0, 0.0, 0.0, 1.0]
        pokeball_colors["normal"]["outerDisk"] = pokeball_colors["normal"]["ring"]
        pokeball_colors["normal"]["innerdisk"] = [1.0, 1.0, 1.0, 1.0]

        pokeball_colors["light"] = {}
        pokeball_colors["light"]["upBall"] = [1.0, 1.0, 1.0, 1.0]
        pokeball_colors["light"]["downBall"] = [1.0, 1.0, 1.0, 1.0]
        pokeball_colors["light"]["ring"] = [1.0, 0.0, 0.0, 1.0]
        pokeball_colors["light"]["outerDisk"] = pokeball_colors["light"]["ring"]
        pokeball_colors["light"]["innerdisk"] = [1.0, 1.0, 1.0, 1.0]


        pokeball_colors["green"] = {}
        pokeball_colors["green"]["upBall"] = [98/255, 211/255, 179/255, 1.0]
        pokeball_colors["green"]["downBall"] = [98/255, 211/255, 179/255, 1.0]
        pokeball_colors["green"]["ring"] = [18/255, 120/255, 122/255, 1.0]
        pokeball_colors["green"]["outerDisk"] = pokeball_colors["green"]["ring"]
        pokeball_colors["green"]["innerdisk"] = [1.0, 1.0, 1.0, 1.0]

        

        #OBJETO POKEBOLA:

        pokeballs_pos = {
            "x": [-0.3, 0.08, 0.45],
            "y": [0.07, -0.05, 0.09],
            "z": [0.3, -0.5, 0.1],
        }

        #Pokebola 1
        create_pokeball(loc_color, loc_mat_transform, objects_dict, -angulo_rotacao_roblox+1, pos=[pokeballs_pos["x"][0], pokeballs_pos["y"][0], pokeballs_pos["z"][0]], scale=0.1, colors_dict=pokeball_colors["normal"])
        #create_diglett(loc_color, loc_mat_transform, objects_dict, -angulo_rotacao_roblox, pos=[0, 0, 0], scale=0.4)

        #Pokebola 2
        create_pokeball(loc_color, loc_mat_transform, objects_dict, -angulo_rotacao_roblox+3.2, pos=[pokeballs_pos["x"][1], pokeballs_pos["y"][0], pokeballs_pos["z"][0]], scale=0.1, colors_dict=pokeball_colors["light"])
        #create_diglett(loc_color, loc_mat_transform, objects_dict, -angulo_rotacao_roblox, pos=[0.8, 0.8, 0], scale=0.05)

        #Pokebola 3
        create_pokeball(loc_color, loc_mat_transform, objects_dict, -angulo_rotacao_roblox+0.9, pos=[pokeballs_pos["x"][2], pokeballs_pos["y"][0], pokeballs_pos["z"][0]], scale=0.1, colors_dict=pokeball_colors["green"])
        #create_diglett(loc_color, loc_mat_transform, objects_dict, -angulo_rotacao_roblox, pos=[-0.8, -0.8, 0], scale=0.05)

        #Pokebola 4
        create_pokeball(loc_color, loc_mat_transform, objects_dict, -angulo_rotacao_roblox+2.2,  pos=[pokeballs_pos["x"][0]-0.15, pokeballs_pos["y"][1], pokeballs_pos["z"][1]], scale=0.1, colors_dict=pokeball_colors["light"])

        #Pokebola 5
        create_pokeball(loc_color, loc_mat_transform, objects_dict, -angulo_rotacao_roblox+0.2,  pos=[pokeballs_pos["x"][1]-0.15, pokeballs_pos["y"][1], pokeballs_pos["z"][1]], scale=0.1, colors_dict=pokeball_colors["normal"])

        #Pokebola 6
        create_pokeball(loc_color, loc_mat_transform, objects_dict, -angulo_rotacao_roblox+2.5,  pos=[pokeballs_pos["x"][2]-0.15, pokeballs_pos["y"][1], pokeballs_pos["z"][1]], scale=0.1, colors_dict=pokeball_colors["green"])

        #OBJETO: Healer
        create_healer(loc_color, loc_mat_transform, objects_dict, 0.15 , pos=[0, -0.2, 0], scale=0.3)

        glfw.swap_buffers(window)
        glfw.poll_events() 

    glfw.terminate()


if __name__ == "__main__":
    draw_scene()
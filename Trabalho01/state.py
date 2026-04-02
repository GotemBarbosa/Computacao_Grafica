import glfw
from OpenGL.GL import *
import numpy as np
from shaders.shaders import Shader
from vertices.vertices import *
from matrix_operations import *
import json

def read_json_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the file '{filename}'. Check the file format.")
        return None

properties_path = "./objects/properties.json"
properties = read_json_file(properties_path)
scene_angles = [0, 0, 0]
scene_scale = 0.5
diglett_y_offset = 0.0
pokeball_opening_angle = 45


def key_event(window,key,scancode,action,mods):
    global properties
    global scene_angles
    global scene_scale
    global pokeball_opening_angle
    global diglett_y_offset

    # KEYBOARD PARA ROTACIONAR E ESCALAR O EEVEE (VAMOS MUDAR PARA O QUE QUISERMOS DEPOIS)
    if key == 263: # esquerda
        scene_angles[1] += 1
    if key == 262: # direita
        scene_angles[1] -= 1
    if key == 265: # cima
        diglett_y_offset += 0.05
    if key == 264: # baixo
        diglett_y_offset -= 0.01
    if key == 81:  # Q
        scene_scale -= 0.05
    if key == 69: # E
        scene_scale += 0.05
    if key == 87:
        properties['pokeball']['position'][1] += 0.05 # W
    if key == 83: 
        properties['pokeball']['position'][1] -= 0.05 # S
    if key == 65: # A
        scene_angles[0] -= 1
        #properties['pokeball']['position'][0] -= 0.05 
    if key == 68: # D
        scene_angles[0] += 1
        #properties['pokeball']['position'][0] += 0.05 
    if key == 88: 
        properties['pokeball']['angles'][0] += 0.5 # X
    if key == 90:
        properties['pokeball']['angles'][0] -= 0.5 # X
    if key == 80:  # P - abre a pokebola
        pokeball_opening_angle = min(pokeball_opening_angle + 5, 180)
    if key == 79:  # O - fecha a pokebola
        pokeball_opening_angle = max(pokeball_opening_angle - 5, 0)




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


#raw_vertices += get_curved_cube_vertices()
raw_vertices += get_cube_vertices()
objects_dict['curved_block'] = {'ini_index': objects_dict["disk"]['end_index'],
                            'end_index': len(raw_vertices),
                            'centroid': get_centroid(raw_vertices, objects_dict["disk"]['end_index'], len(raw_vertices) - objects_dict["disk"]['end_index'])}


raw_vertices += get_square_vertices()
objects_dict['square'] = {'ini_index': objects_dict['curved_block']['end_index'],
                          'end_index': len(raw_vertices),
                          'centroid': get_centroid(raw_vertices, objects_dict["disk"]['end_index'], len(raw_vertices) - objects_dict["disk"]['end_index'])}

# Aloca espaço na GPU para todos os vértices criados
vertices = allocate_vertices_on_gpu(raw_vertices, loc_position)

glfw.set_key_callback(window,key_event)

glEnable(GL_DEPTH_TEST)
glfw.show_window(window)
import glfw
from OpenGL.GL import *
import numpy as np
from shaders.shaders import Shader
from matrix_operations import *
import ctypes

from objetos.obj_loader import load_box_geometry

import glm
from PIL import Image

# =========================
# Estado global da cena
# =========================

# Controle de tempo entre frames (atualizado em main.py)
deltaTime = 5.0
lastFrame = 0.0

# Ângulo acumulado para rotação da caixa
obj_angle = 0.0

# Câmera (posição, direção frontal e eixo vertical)
cameraPos = glm.vec3(0.0, 0.0, 0.0)
cameraFront = glm.vec3(0.0, 0.0, -1.0)
cameraUp = glm.vec3(0.0, 1.0, 0.0)


# Estado do mouse para controle
firstMouse = True
yaw = -90.0
pitch = 0.0
lastX = 350.0
lastY = 350.0
fov = 45.0


def model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
    # Matriz model (T * R * S) para transformar o objeto no mundo
    angle = glm.radians(angle)

    m = glm.mat4(1.0)
    m = glm.translate(m, glm.vec3(t_x, t_y, t_z))
    if angle != 0:
        m = glm.rotate(m, angle, glm.vec3(r_x, r_y, r_z))
    m = glm.scale(m, glm.vec3(s_x, s_y, s_z))

    return np.array(m, dtype=np.float32)


def view():
    # Matriz view construída a partir da câmera atual
    v = glm.lookAt(cameraPos, cameraPos + cameraFront, cameraUp)
    return np.array(v, dtype=np.float32)


def projection():
    # Projeção perspectiva (FOV, aspecto, near/far)
    largura, altura = 700.0, 700.0
    p = glm.perspective(glm.radians(fov), largura / altura, 0.1, 100.0)
    return np.array(p, dtype=np.float32)




def key_event(window,key,scancode,action,mods):
    global cameraPos, cameraFront, cameraUp, obj_angle

    # Aceita só tecla pressionada ou repetida
    if action not in (glfw.PRESS, glfw.REPEAT):
        return

    # Encerra aplicação
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    # Movimento da câmera baseado em deltaTime
    camera_speed = 10 * deltaTime

    right = glm.normalize(glm.cross(cameraFront, cameraUp))

    # WASD: navegação da câmera
    if key == glfw.KEY_W:
        cameraPos += camera_speed * cameraFront
    if key == glfw.KEY_S:
        cameraPos -= camera_speed * cameraFront
    if key == glfw.KEY_A:
        cameraPos -= camera_speed * right
    if key == glfw.KEY_D:
        cameraPos += camera_speed * right

    # Q/E: rotação da caixa
    if key == glfw.KEY_Q:
        obj_angle += 5.0
    if key == glfw.KEY_E:
        obj_angle -= 5.0



def mouse_event(window, xpos, ypos):
    global firstMouse, yaw, pitch, lastX, lastY, cameraFront

    # Evita salto inicial de câmera no primeiro evento
    if firstMouse:
        lastX = xpos
        lastY = ypos
        firstMouse = False

    # Offset do mouse desde o último frame
    xoffset = xpos - lastX
    yoffset = lastY - ypos
    lastX = xpos
    lastY = ypos

    sensitivity = 0.1
    xoffset *= sensitivity
    yoffset *= sensitivity

    # Atualiza orientação da câmera
    yaw += xoffset
    pitch += yoffset

    # Limites do pitch para evitar flip vertical
    if pitch > 89.0:
        pitch = 89.0
    if pitch < -89.0:
        pitch = -89.0

    front = glm.vec3()
    front.x = np.cos(glm.radians(yaw)) * np.cos(glm.radians(pitch))
    front.y = np.sin(glm.radians(pitch))
    front.z = np.sin(glm.radians(yaw)) * np.cos(glm.radians(pitch))
    cameraFront = glm.normalize(front)

def scroll_event(window, xoffset, yoffset):
    global fov
    # Zoom via FOV
    fov -= yoffset
    if fov < 1.0: fov = 1.0
    if fov > 90.0: fov = 90.0






def create_window():
    # Inicializa GLFW e cria janela/contexto OpenGL
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

    window = glfw.create_window(700, 700, "Trabalho 2", None, None)

    if(window == None):
        print("Failed to create GLFW window")
        glfw.terminate()
    glfw.make_context_current(window)
    return window

def allocate_positions_on_gpu(raw_vertices, loc_position):
    # Upload de vértices (x,y,z) para VBO e vinculação ao atributo "position"
    vertices = np.zeros(len(raw_vertices), [("position", np.float32, 3)])
    vertices["position"] = raw_vertices

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    stride = vertices.strides[0]
    glEnableVertexAttribArray(loc_position)
    glVertexAttribPointer(loc_position, 3, GL_FLOAT, False, stride, ctypes.c_void_p(0))


def allocate_texcoords_on_gpu(raw_texcoords, loc_texture_coord):
    # Upload de coordenadas de textura (u,v) e vínculo ao atributo "texture_coord"
    textures = np.zeros(len(raw_texcoords), [("position", np.float32, 2)])
    textures["position"] = raw_texcoords

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)

    stride = textures.strides[0]
    glEnableVertexAttribArray(loc_texture_coord)
    glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, stride, ctypes.c_void_p(0))


def load_texture_from_file(texture_id, img_path):
    # Carrega textura da imagem e envia para a GPU
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    img = Image.open(img_path).convert("RGB")
    img_data = img.tobytes("raw", "RGB", 0, -1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

# =========================
# OpenGL/Shader
# =========================
window = create_window()
ourShader = Shader("./shaders/vertex_shader.vs", "./shaders/fragment_shader.fs")
ourShader.use()
program = ourShader.getProgram()

# Localização dos atributos/uniforms no shader
loc_position = glGetAttribLocation(program, "position")
loc_texture_coord = glGetAttribLocation(program, "texture_coord")
loc_model = glGetUniformLocation(program, "model")
loc_view = glGetUniformLocation(program, "view")
loc_projection = glGetUniformLocation(program, "projection")
loc_sampler = glGetUniformLocation(program, "imagem")

raw_vertices, raw_texcoords = load_box_geometry("./objetos/caixa/caixa.obj")

# Faixa de vértices usada para desenhar cada objeto
objects_dict = {
    "caixa": {
        "ini_index": 0,
        "end_index": len(raw_vertices),
    }
}

allocate_positions_on_gpu(raw_vertices, loc_position)
allocate_texcoords_on_gpu(raw_texcoords, loc_texture_coord)

texture_id = glGenTextures(1)
load_texture_from_file(texture_id, "./objetos/caixa/caixa.jpg")

# Sampler "imagem" usa a unidade de textura 0
glActiveTexture(GL_TEXTURE0)
glUniform1i(loc_sampler, 0)

# Callbacks de entrada
glfw.set_key_callback(window, key_event)

glfw.set_scroll_callback(window, scroll_event)

glfw.set_cursor_pos_callback(window, mouse_event)
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)


# Renderização 3D com profundidade
glEnable(GL_DEPTH_TEST)
glfw.show_window(window)

import glfw
from OpenGL.GL import *
import numpy as np
from shaders.shaders import Shader
from matrix_operations import *
import ctypes

from objetos.obj_loader import load_obj_geometry

import glm
from PIL import Image

# =========================
# Estado global da cena
# =========================

# Controle de tempo entre frames (atualizado em main.py)
deltaTime = 5.0
lastFrame = 0.0
last_time = 0
nb_frames = 0

# Ângulo acumulado para rotação da caixa
obj_angle = 0.0

# Câmera (posição, direção frontal e eixo vertical)
cameraPos = glm.vec3(0.0, 0.0, 0.0)
cameraFront = glm.vec3(0.0, 0.0, -1.0)
cameraUp = glm.vec3(0.0, 1.0, 0.0)
cameraMoveFront = glm.vec3(0.0, 0.0, -1.0)

flyMode = False


# Estado do mouse para controle
firstMouse = True
yaw = -90.0
pitch = 0.0
lastX = 350.0
lastY = 350.0
fov = 45.0

# parametros de fisica
velocityY = 0.0
gravity = -20.0
jumpForce = 12.0
isOnGround = True
groundHeight = 0.0


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
    largura, altura = 1920.0, 1080.0
    p = glm.perspective(glm.radians(fov), largura / altura, 0.1, 1000.0)
    return np.array(p, dtype=np.float32)


keys = {} # Mantém o estado de quais teclas estão sendo pressionadas, permite a movimentação na diagonal e deixa o movimento mais fluido

def key_event(window, key, scancode, action, mods):
    global keys, flyMode, velocityY, isOnGround

    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_F and action == glfw.PRESS:
        flyMode = not flyMode

    # Pulo → evento único (isso pode ficar aqui)
    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        if isOnGround:
            velocityY = jumpForce
            isOnGround = False



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

def update_move_front_camera():
    global cameraFront, cameraUp, cameraMoveFront
    cameraMoveFront.x = cameraFront.x
    cameraMoveFront.y = 0
    cameraMoveFront.z = cameraFront.z
    if (cameraMoveFront.x == 0 and cameraMoveFront.z == 0):
        cameraMoveFront = (-1) * cameraUp 
    cameraMoveFront = glm.normalize(cameraMoveFront)
    return






def create_window():
    # Inicializa GLFW e cria janela/contexto OpenGL
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

    window = glfw.create_window(1920, 1080, "Trabalho 2", None, None)

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
loc_use_texture = glGetUniformLocation(program, "use_texture")
loc_base_color = glGetUniformLocation(program, "base_color")


raw_vertices = [] 
raw_texcoords = []

# caixa
box_v, box_t = load_obj_geometry("./objetos/caixa/caixa.obj")
ini_box = len(raw_vertices)
raw_vertices += box_v
raw_texcoords += box_t
fim_box = len(raw_vertices)

# snowTerrain
snow_v, snow_t = load_obj_geometry("./objetos/snowTerrain/SnowTerrain.obj")
ini_snow = len(raw_vertices)
raw_vertices += snow_v
raw_texcoords += snow_t
fim_snow = len(raw_vertices)


# Jeep
jeep_v, jeep_t = load_obj_geometry("./objetos/Jeep/Jeep_Renegade_2016.obj")
ini_jeep = len(raw_vertices)
raw_vertices += jeep_v
raw_texcoords += jeep_t
fim_jeep = len(raw_vertices)

# ground
ground_v, ground_t = load_obj_geometry("./objetos/ground/ground.obj")
ini_ground = len(raw_vertices)
raw_vertices += ground_v
raw_texcoords += ground_t
fim_ground = len(raw_vertices)

# sky
sky_v, sky_t = load_obj_geometry("./objetos/sky/esfera.obj")
ini_sky = len(raw_vertices)
raw_vertices += sky_v
raw_texcoords += sky_t
fim_sky = len(raw_vertices)

# house
house_v, house_t = load_obj_geometry("./objetos/house/forester's_house.obj")
ini_house = len(raw_vertices)
raw_vertices += house_v
raw_texcoords += house_t
fim_house = len(raw_vertices)

# campfire
campfire_v, campfire_t = load_obj_geometry("./objetos/campfire/campfire.obj")
ini_campfire = len(raw_vertices)
raw_vertices += campfire_v
raw_texcoords += campfire_t
fim_campfire = len(raw_vertices)



objects_dict = {
    "caixa": {"ini_index": ini_box, "end_index": fim_box},
    "snowTerrain": {"ini_index": ini_snow, "end_index": fim_snow},
    "jeep": {"ini_index": ini_jeep, "end_index": fim_jeep},
    "ground": {"ini_index": ini_ground, "end_index": fim_ground},
    "sky": {"ini_index": ini_sky, "end_index": fim_sky},
    "house": {"ini_index": ini_house, "end_index": fim_house},
    "campfire": {"ini_index": ini_campfire, "end_index": fim_campfire},
}


allocate_positions_on_gpu(raw_vertices, loc_position)
allocate_texcoords_on_gpu(raw_texcoords, loc_texture_coord)

# Texturas 
texture_id = glGenTextures(1)
load_texture_from_file(texture_id, "./objetos/caixa/caixa.jpg")

snow_texture_id = glGenTextures(1)
load_texture_from_file(snow_texture_id, "./objetos/snowTerrain/686.jpg")

jeep_texture_id = glGenTextures(1)
load_texture_from_file(jeep_texture_id, "./objetos/Jeep/car_jeep_ren.jpg")

ground_texture_id = glGenTextures(1)
load_texture_from_file(ground_texture_id, "./objetos/ground/text_Albedo.png")

sky_texture_id = glGenTextures(1)
load_texture_from_file(sky_texture_id, "./objetos/sky/NightSky4k.jpg")

house_texture_id = glGenTextures(1)
load_texture_from_file(house_texture_id, "./objetos/house/diffuse_forester's_house.tga")

campfire_texture_id = glGenTextures(1)
load_texture_from_file(campfire_texture_id, "./objetos/campfire/campfire.jpg")



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

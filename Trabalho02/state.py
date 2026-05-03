import glfw
from OpenGL.GL import *
import numpy as np
from shaders.shaders import Shader
from matrix_operations import *
import ctypes

from objetos.obj_loader import load_obj_geometry

import glm
from PIL import Image
import warnings

warnings.simplefilter('ignore', Image.DecompressionBombWarning)

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

newPlanetUp = glm.vec3(0.0, 1.0, 0.0)
planetUp = glm.vec3(0.0, 1.0, 0.0)
planetFoward = glm.vec3(0.0, 0.0, -1.0)
planetRight = glm.vec3(1.0, 0.0, 0.0)


planetCenter = glm.vec3(0.0, -48, 0.0)


planetActivated = False
masterMode = False

flyMode = False


# Estado do mouse para controle
firstMouse = True
yaw = -90.0
pitch = 0.0
lastX = 350.0
lastY = 350.0
fov = 45.0

# parametros de fisica
gravity = glm.vec3(0.0, -1.0, 0.0)
jumpForce = 12.0
isOnGround = True
groundHeight = 0.0
velocity = glm.vec3(0.0, 0.0, 0.0)
planetRadius = 48.0
gravityStrength = 30.0

# começa no piso
gravity_weight = 1.0

# foguete
rocket_offset = 0.0          # quanto o foguete está acima da posição base
rocket_max_height = 100.0    # limite máximo de subida
rocket_speed = 15.0          # velocidade de subida/descida (unidades por segundo)

# satelite (orbita)
satelite_orbit_angle = 0.0   # ângulo atual da órbita (graus)
satelite_orbit_speed = 30.0  # velocidade angular (graus por segundo)
satelite_orbit_radius = 30.0 # distância acima da superfície
satelite_orbit_lat = -30.0   # latitude do plano da órbita (inclinação)

# telescópio (yaw controlável)
telescope_yaw = 0.0          # rotação acumulada (graus) — somada ao ângulo base
telescope_yaw_speed = 60.0   # velocidade de rotação (graus por segundo)

# flags de input (setadas em key_event, lidas nas funções de desenho)
rocket_going_up = False
rocket_going_down = False
telescope_turning_left = False
telescope_turning_right = False

# modos de visualização (toggles)
wireframe_mode = False       # P: alterna malha poligonal (GL_LINE) ↔ preenchido (GL_FILL)


def model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, base_rotation=None):
    # Matriz model (T * R * S) para transformar o objeto no mundo
    angle = glm.radians(angle)

    translation = glm.translate(glm.mat4(1.0), glm.vec3(t_x, t_y, t_z))

    if base_rotation is None:
        base_rotation = glm.mat4(1.0)

    extra_rotation = glm.mat4(1.0)
    if angle != 0:
        extra_rotation = glm.rotate(extra_rotation, angle, glm.vec3(r_x, r_y, r_z))

    scale = glm.scale(glm.mat4(1.0), glm.vec3(s_x, s_y, s_z))

    m = translation * base_rotation * extra_rotation * scale

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
    global keys, flyMode, velocity, isOnGround, planetUp, planetActivated, masterMode
    global cameraPos, cameraFront, cameraUp, cameraMoveFront, newPlanetUp, planetFoward, planetRight, gravity, velocity
    global rocket_going_up, rocket_going_down, telescope_turning_left, telescope_turning_right
    global wireframe_mode

    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_F and action == glfw.PRESS:
        flyMode = not flyMode

    if key == glfw.KEY_O and action == glfw.PRESS:
        masterMode = not masterMode
        planetActivated = False
        cameraPos = glm.vec3(0.0, 0.0, 0.0)
        cameraFront = glm.vec3(0.0, 0.0, -1.0)
        cameraUp = glm.vec3(0.0, 1.0, 0.0)
        cameraMoveFront = glm.vec3(0.0, 0.0, -1.0)
        newPlanetUp = glm.vec3(0.0, 1.0, 0.0)
        planetUp = glm.vec3(0.0, 1.0, 0.0)
        planetFoward = glm.vec3(0.0, 0.0, -1.0)
        planetRight = glm.vec3(1.0, 0.0, 0.0)
        gravity = glm.vec3(0.0, -1.0, 0.0)
        velocity = glm.vec3(0.0, 0.0, 0.0)

    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        if isOnGround:
            if not masterMode:
                velocity += planetUp * jumpForce
            else:
                velocity += glm.vec3(0.0, 1.0, 0.0) * jumpForce
            isOnGround = False

    # === FOGUETE: sobe/desce ===
    if key == glfw.KEY_UP:
        if action == glfw.PRESS:   rocket_going_up = True
        if action == glfw.RELEASE: rocket_going_up = False
    if key == glfw.KEY_DOWN:
        if action == glfw.PRESS:   rocket_going_down = True
        if action == glfw.RELEASE: rocket_going_down = False

    # === TELESCÓPIO: gira yaw ===
    if key == glfw.KEY_LEFT:
        if action == glfw.PRESS:   telescope_turning_left = True
        if action == glfw.RELEASE: telescope_turning_left = False
    if key == glfw.KEY_RIGHT:
        if action == glfw.PRESS:   telescope_turning_right = True
        if action == glfw.RELEASE: telescope_turning_right = False

    # === VISUALIZAÇÃO: malha poligonal ===
    if key == glfw.KEY_P and action == glfw.PRESS:
        wireframe_mode = not wireframe_mode




def mouse_event(window, xpos, ypos):
    global firstMouse, lastX, lastY, cameraFront, planetUp, cameraUp, planetRight

    if firstMouse:
        lastX = xpos
        lastY = ypos
        firstMouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos 
    lastX = xpos
    lastY = ypos

    sensitivity = 0.1
    xoffset *= sensitivity
    yoffset *= sensitivity

    # A matemática vetorial lida perfeitamente com gravidade plana ou esférica!
    rotationYaw = glm.rotate(glm.mat4(1.0), glm.radians(-xoffset), planetUp)
    cameraFront = glm.normalize(glm.vec3(rotationYaw * glm.vec4(cameraFront, 0.0)))
    cameraUp = glm.normalize(glm.vec3(rotationYaw * glm.vec4(cameraUp, 0.0)))

    planetRight = glm.normalize(glm.cross(cameraFront, planetUp))
    rotationPitch = glm.rotate(glm.mat4(1.0), glm.radians(yoffset), planetRight)

    newFront = glm.normalize(glm.vec3(rotationPitch * glm.vec4(cameraFront, 0.0)))

    safe_limit_cos = 0.9998
    if abs(glm.dot(newFront, planetUp)) < safe_limit_cos:
        cameraFront = newFront
        cameraUp = glm.normalize(glm.vec3(rotationPitch * glm.vec4(cameraUp, 0.0)))

    cameraUp = glm.normalize(cameraUp - glm.dot(cameraUp, cameraFront) * cameraFront)

def scroll_event(window, xoffset, yoffset):
    global fov
    # Zoom via FOV
    fov -= yoffset
    if fov < 1.0: fov = 1.0
    if fov > 90.0: fov = 90.0

def update_move_front_camera():
    global cameraFront, cameraUp, planetFoward, planetUp, planetCenter, cameraPos, planetRight, newPlanetUp, gravity_weight, masterMode

    # 1. Calcula o "Cima" dos dois tipos de gravidade (planeta e piso inicial)
    purePlanetUp = glm.normalize(cameraPos - planetCenter)
    pureFlatUp = glm.vec3(0.0, 1.0, 0.0)


    # 2. MISTURA (Interpola) os dois vetores suavemente (com base na função Smoothstep da main.py)
    # ===================
    # essa função "mix" cria uma interpolação (suavização) entre esses 3 vetores com base em uma porcentagem
    # quanto mais perto de 0 estiver o gravity_weight, mais perto estará de pureFlatUp
    # quanto mais perto de 1 estiver o gravity_weight, mais perto estará de purePlanetUp
    # ===================
    if not masterMode:
        newPlanetUp = glm.normalize(glm.mix(pureFlatUp, purePlanetUp, gravity_weight))

        
        # ===================
        # verificação para rodar a camera ao longo do planeta com base no quanto voce se moveu
        # a ideia é pegar os vetores normais ao planeta (planetsUps) anterior e novo, e comparar se 
        # o angulo entre eles bate um minimo, se sim, queremos rodar a camera ao redor do planeta 
        # essa mesma quantidade
        # ===================
        cos_theta = glm.dot(planetUp, newPlanetUp)

        if cos_theta < 0.999999:
            cos_theta = np.clip(cos_theta, -1.0, 1.0)
            angle = np.arccos(cos_theta)
            
            # rotationAxis --> é o eixo de rotação que a camera precisa rodar
            # movementRotation --> é a matriz de rotação para rotacionar a camera
            rotationAxis = glm.normalize(glm.cross(planetUp, newPlanetUp))
            movementRotation = glm.rotate(glm.mat4(1.0), angle, rotationAxis)
            
            # rotaciona a camera
            cameraFront = glm.normalize(glm.vec3(movementRotation * glm.vec4(cameraFront, 0.0)))
            cameraUp = glm.normalize(glm.vec3(movementRotation * glm.vec4(cameraUp, 0.0)))
        
        # atualiza os valores que ditam como se movimentar ao longo do planeta
        # exemplo: ao apertar W você deve sempre ir em direção ao planetFoward, não ao que você enxerga
    planetUp = newPlanetUp
    planetRight = glm.normalize(glm.cross(cameraFront, planetUp))
    planetFoward = glm.normalize(glm.cross(planetUp, planetRight))

    cameraUp = glm.normalize(cameraUp - glm.dot(cameraUp, cameraFront) * cameraFront)







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

# campfire
campfire_v, campfire_t = load_obj_geometry("./objetos/campfire/campfire.obj")
ini_campfire = len(raw_vertices)
raw_vertices += campfire_v
raw_texcoords += campfire_t
fim_campfire = len(raw_vertices)

pineTree_v, pineTree_t = load_obj_geometry("./objetos/pineTree/pineTree.obj")
ini_pineTree = len(raw_vertices)
raw_vertices += pineTree_v
raw_texcoords += pineTree_t
fim_pineTree = len(raw_vertices)

rocket_v, rocket_t = load_obj_geometry("./objetos/rocket/rocket2.obj")
ini_rocket = len(raw_vertices)
raw_vertices += rocket_v
raw_texcoords += rocket_t
fim_rocket = len(raw_vertices)

table_v, table_t = load_obj_geometry("./objetos/table/table.obj")
ini_table = len(raw_vertices)
raw_vertices += table_v
raw_texcoords += table_t
fim_table = len(raw_vertices)

cartoonHouse_v, cartoonHouse_t = load_obj_geometry("./objetos/cartoonHouse/cartoonHouse.obj")
ini_cartoonHouse = len(raw_vertices)
raw_vertices += cartoonHouse_v
raw_texcoords += cartoonHouse_t
fim_cartoonHouse = len(raw_vertices)

telescope_v, telescope_t = load_obj_geometry("./objetos/telescope/telescope.obj")
ini_telescope = len(raw_vertices)
raw_vertices += telescope_v
raw_texcoords += telescope_t
fim_telescope = len(raw_vertices)

forge_v, forge_t = load_obj_geometry("./objetos/forge/forge.obj")
ini_forge = len(raw_vertices)
raw_vertices += forge_v
raw_texcoords += forge_t
fim_forge = len(raw_vertices)

satelite_v, satelite_t = load_obj_geometry("./objetos/satelite/satelite.obj")
ini_satelite = len(raw_vertices)
raw_vertices += satelite_v
raw_texcoords += satelite_t
fim_satelite = len(raw_vertices)

rockTiles_v, rockTiles_t = load_obj_geometry("./objetos/rockTiles/rockTiles.obj")
ini_rockTiles = len(raw_vertices)
raw_vertices += rockTiles_v
raw_texcoords += rockTiles_t
fim_rockTiles = len(raw_vertices)

treeStump_v, treeStump_t = load_obj_geometry("./objetos/treeStump/treeStump.obj")
ini_treeStump = len(raw_vertices)
raw_vertices += treeStump_v
raw_texcoords += treeStump_t
fim_treeStump = len(raw_vertices)

outerWilds_v, outerWilds_t = load_obj_geometry("./objetos/outerWilds/outerWilds.obj")
ini_outerWilds = len(raw_vertices)
raw_vertices += outerWilds_v
raw_texcoords += outerWilds_t
fim_outerWilds = len(raw_vertices)




objects_dict = {
    "caixa": {"ini_index": ini_box, "end_index": fim_box},
    "snowTerrain": {"ini_index": ini_snow, "end_index": fim_snow},
    "jeep": {"ini_index": ini_jeep, "end_index": fim_jeep},
    "ground": {"ini_index": ini_ground, "end_index": fim_ground},
    "sky": {"ini_index": ini_sky, "end_index": fim_sky},
    "campfire": {"ini_index": ini_campfire, "end_index": fim_campfire},
    "pineTree": {"ini_index": ini_pineTree, "end_index": fim_pineTree},
    "rocket": {"ini_index": ini_rocket, "end_index": fim_rocket},
    "table": {"ini_index": ini_table, "end_index": fim_table},
    "cartoonHouse": {"ini_index": ini_cartoonHouse, "end_index": fim_cartoonHouse},
    "telescope": {"ini_index": ini_telescope, "end_index": fim_telescope},
    "forge": {"ini_index": ini_forge, "end_index": fim_forge},
    "satelite": {"ini_index": ini_satelite, "end_index": fim_satelite},
    "rockTiles": {"ini_index": ini_rockTiles, "end_index": fim_rockTiles},
    "treeStump": {"ini_index": ini_treeStump, "end_index": fim_treeStump},
    "outerWilds": {"ini_index": ini_outerWilds, "end_index": fim_outerWilds},
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

campfire_texture_id = glGenTextures(1)
load_texture_from_file(campfire_texture_id, "./objetos/campfire/campfire.jpg")

mars_texture_id = glGenTextures(1)
load_texture_from_file(mars_texture_id, "./objetos/planet/mars.jpg")

moon_texture_id = glGenTextures(1)
load_texture_from_file(moon_texture_id, "./objetos/planet/moon.jpg")

#ceres_texture_id = glGenTextures(1)
#load_texture_from_file(ceres_texture_id, "./objetos/planet/ceres.png")

pineTree_texture_id = glGenTextures(1)
load_texture_from_file(pineTree_texture_id, "./objetos/pineTree/pineTree.png")

rocket_texture_id = glGenTextures(1)
load_texture_from_file(rocket_texture_id, "./objetos/rocket/rocket2.png")

table_texture_id = glGenTextures(1)
load_texture_from_file(table_texture_id, "./objetos/table/table.png")

cartoonHouse_texture_id = glGenTextures(1)
load_texture_from_file(cartoonHouse_texture_id, "./objetos/cartoonHouse/cartoonHouse.png")

woodPlanks_texture_id = glGenTextures(1)
load_texture_from_file(woodPlanks_texture_id, "./objetos/caixa/woodPlanks.bmp")

telescope_texture_id = glGenTextures(1)
load_texture_from_file(telescope_texture_id, "./objetos/telescope/telescope.png")

forge_texture_id = glGenTextures(1)
load_texture_from_file(forge_texture_id, "./objetos/forge/forge.png")

satelite_texture_id = glGenTextures(1)
load_texture_from_file(satelite_texture_id, "./objetos/satelite/satelite.png")

rockTiles_texture_id = glGenTextures(1)
load_texture_from_file(rockTiles_texture_id, "./objetos/rockTiles/rockTiles.png")
                       
treeStump_texture_id = glGenTextures(1)
load_texture_from_file(treeStump_texture_id, "./objetos/treeStump/treeStump.png")

outerWilds_texture_id = glGenTextures(1)
load_texture_from_file(outerWilds_texture_id, "./objetos/outerWilds/outerWilds.png")



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

import glfw
from OpenGL.GL import *
import numpy as np
from shaders.shaders import Shader
from matrix_operations import *
import ctypes

from objetos.obj_loader import load_obj_geometry
from utils.coordenates import planet_to_world_coordenates

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

# marte (escala controlável)
mars_scale = 80.0
mars_scale_speed = 30.0      # unidades de escala por segundo
mars_scaling_up = False      # E
mars_scaling_down = False    # Q

# =========================================================================
# ILUMINAÇÃO (Projeto 3)
# =========================================================================

# --- SOL: fonte de luz EXTERNA controlável pelas setas do teclado ---
sun_orbit_angle  = 45.0                          # longitude do sol (graus) — setas ←/→
sun_orbit_lat    = 20.0                           # latitude do sol (graus) — setas ↑/↓
sun_move_speed   = 45.0                           # velocidade de movimento (graus/seg)
sun_orbit_radius = 200.0                          # distância ao centro do planeta
sun_pos          = glm.vec3(200.0, -48.0, 0.0)    # posição (atualizada por frame)
sun_color        = glm.vec3(1.8, 1.7, 1.45)       # branco-amarelado, intenso

# --- VELA: fonte de luz INTERNA 1 (quente, alaranjada) ---
candle_pos   = glm.vec3(-2.1, -0.45, 4.25)      # vela em cima da mesa
candle_color = glm.vec3(1.0, 0.55, 0.10)        # laranja quente

# --- LUMINÁRIA: fonte de luz INTERNA 2 (fria, azul/roxo) ---
lantern_pos   = glm.vec3(2.92, -0.4, 3.7)       # lanterna na prateleira
lantern_color = glm.vec3(0.4, 0.3, 1.0)         # azul/roxo

# --- INTERRUPTORES (cada luz tem o seu) ---
light_sun_enabled     = True
light_candle_enabled  = True
light_lantern_enabled = True
light_ambient_enabled = True

# --- INTENSIDADES AJUSTÁVEIS POR TECLADO ---
ambient_intensity  = 0.9   # luz ambiente   [0.0, 1.0]
diffuse_intensity  = 1.0     # multiplicador difuso  [0.0, 2.0]
specular_intensity = 1.0     # multiplicador especular  [0.0, 2.0]
INTENSITY_STEP     = 0.05

# --- Shadow map (preenchido na inicialização do OpenGL, mais abaixo) ---
SHADOW_WIDTH  = 2048
SHADOW_HEIGHT = 2048
shadow_fbo = None
shadow_map = None


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

    # Guarda a versão glm para calcular a matriz de normais em upload_model()
    global _last_model_glm
    _last_model_glm = m

    return np.array(m, dtype=np.float32)


# Última matriz model (glm) calculada por model(), usada para a matriz de normais
_last_model_glm = glm.mat4(1.0)


def upload_model(mat_model):
    """Envia a matriz model e a matriz de normais (inverse-transpose) ao shader.

    A matriz de normais é calculada na CPU porque o GLSL 120 não tem
    inverse()/transpose(). Necessária para iluminar corretamente objetos
    com escala não-uniforme.
    """
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
    normal_mat = glm.transpose(glm.inverse(glm.mat3(_last_model_glm)))
    glUniformMatrix3fv(loc_normal_matrix, 1, GL_TRUE,
                       np.array(normal_mat, dtype=np.float32))


def set_material(name):
    """Envia os coeficientes de iluminação (Ka/Kd/Ks/shininess) do objeto."""
    from materials import get_material
    m = get_material(name)
    glUniform1f(loc_Ka,        m["Ka"])
    glUniform1f(loc_Kd,        m["Kd"])
    glUniform1f(loc_Ks,        m["Ks"])
    glUniform1f(loc_shininess, m["shi"])


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
    global light_sun_enabled, light_candle_enabled, light_lantern_enabled, light_ambient_enabled
    global ambient_intensity, diffuse_intensity, specular_intensity

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

    # =====================================================================
    # ILUMINAÇÃO (Projeto 3)
    # =====================================================================

    # --- INTERRUPTORES: cada luz liga/desliga de forma independente ---
    if key == glfw.KEY_1 and action == glfw.PRESS:
        light_sun_enabled = not light_sun_enabled          # luz externa (sol)
    if key == glfw.KEY_2 and action == glfw.PRESS:
        light_candle_enabled = not light_candle_enabled    # luz interna (vela)
    if key == glfw.KEY_3 and action == glfw.PRESS:
        light_lantern_enabled = not light_lantern_enabled  # luz interna (luminária)
    if key == glfw.KEY_4 and action == glfw.PRESS:
        light_ambient_enabled = not light_ambient_enabled  # luz ambiente

    # --- LUZ AMBIENTE: incrementa/decrementa  ([ e ]) ---
    if key == glfw.KEY_K and action in (glfw.PRESS, glfw.REPEAT):
        ambient_intensity = max(0.0, ambient_intensity - INTENSITY_STEP)
    if key == glfw.KEY_L and action in (glfw.PRESS, glfw.REPEAT):
        ambient_intensity = min(1.0, ambient_intensity + INTENSITY_STEP)

    # --- REFLEXÃO DIFUSA: incrementa/decrementa  (; e ') ---
    if key == glfw.KEY_H and action in (glfw.PRESS, glfw.REPEAT):
        diffuse_intensity = max(0.0, diffuse_intensity - INTENSITY_STEP)
    if key == glfw.KEY_J and action in (glfw.PRESS, glfw.REPEAT):
        diffuse_intensity = min(2.0, diffuse_intensity + INTENSITY_STEP)

    # --- REFLEXÃO ESPECULAR: incrementa/decrementa  (, e .) ---
    if key == glfw.KEY_N and action in (glfw.PRESS, glfw.REPEAT):
        specular_intensity = max(0.0, specular_intensity - INTENSITY_STEP)
    if key == glfw.KEY_M and action in (glfw.PRESS, glfw.REPEAT):
        specular_intensity = min(2.0, specular_intensity + INTENSITY_STEP)


def update_sun():
    """Move o sol (luz externa) conforme as setas do teclado e atualiza sun_pos.

    Chamada a cada frame. As setas são teclas de pressão contínua, então são
    lidas do dicionário `keys` (preenchido por key_event) em vez de tratadas
    como eventos discretos.
      ←/→ : longitude    ↑/↓ : latitude (limitada a ±89° p/ não cruzar os polos)
    """
    global sun_orbit_angle, sun_orbit_lat, sun_pos

    sun_step = sun_move_speed * deltaTime
    if keys.get(glfw.KEY_RIGHT, False):
        sun_orbit_angle += sun_step        # → move em longitude
    if keys.get(glfw.KEY_LEFT, False):
        sun_orbit_angle -= sun_step        # ←
    if keys.get(glfw.KEY_UP, False):
        sun_orbit_lat += sun_step          # ↑ move em latitude
    if keys.get(glfw.KEY_DOWN, False):
        sun_orbit_lat -= sun_step          # ↓

    # não deixa o sol passar pelos polos (evita instabilidade da matriz da luz)
    sun_orbit_lat = max(-89.0, min(89.0, sun_orbit_lat))

    sun_pos = planet_to_world_coordenates(
        lat=sun_orbit_lat, lon=sun_orbit_angle,
        radius=sun_orbit_radius, center=planetCenter
    )


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

    safe_limit_cos = 0.97
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


def allocate_normals_on_gpu(raw_normals, loc_normal):
    # Upload das normais (nx,ny,nz) para VBO e vínculo ao atributo "normal"
    normals = np.zeros(len(raw_normals), [("position", np.float32, 3)])
    normals["position"] = raw_normals

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)

    stride = normals.strides[0]
    glEnableVertexAttribArray(loc_normal)
    glVertexAttribPointer(loc_normal, 3, GL_FLOAT, False, stride, ctypes.c_void_p(0))


def load_texture_from_file(texture_id, img_path):
    # Configura a textura (já reservada) e envia os pixels da imagem para a GPU
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    img = Image.open(img_path).convert("RGB")
    img_data = img.tobytes("raw", "RGB", 0, -1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)


def load_texture(img_path):
    """Reserva um id de textura, carrega a imagem nele e retorna o id.

    Encapsula o par 'glGenTextures + load_texture_from_file' usado por cada
    objeto, evitando repetição no carregamento das texturas.
    """
    texture_id = glGenTextures(1)
    load_texture_from_file(texture_id, img_path)
    return texture_id


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
loc_normal = glGetAttribLocation(program, "normal")
loc_model = glGetUniformLocation(program, "model")
loc_view = glGetUniformLocation(program, "view")
loc_projection = glGetUniformLocation(program, "projection")
loc_sampler = glGetUniformLocation(program, "imagem")
loc_use_texture = glGetUniformLocation(program, "use_texture")
loc_base_color = glGetUniformLocation(program, "base_color")

# --- Uniforms de iluminação / shadow map (Projeto 3) ---
loc_normal_matrix = glGetUniformLocation(program, "normalMatrix")
loc_light_space   = glGetUniformLocation(program, "lightSpaceMatrix")
loc_depth_pass    = glGetUniformLocation(program, "depthPass")
loc_is_internal   = glGetUniformLocation(program, "is_internal")
loc_unlit         = glGetUniformLocation(program, "unlit")
loc_shadow_map    = glGetUniformLocation(program, "shadowMap")
loc_view_pos      = glGetUniformLocation(program, "viewPos")

loc_Ka        = glGetUniformLocation(program, "Ka")
loc_Kd        = glGetUniformLocation(program, "Kd")
loc_Ks        = glGetUniformLocation(program, "Ks")
loc_shininess = glGetUniformLocation(program, "shininess")

loc_light_ambient_enabled = glGetUniformLocation(program, "light_ambient_enabled")
loc_ambient_intensity     = glGetUniformLocation(program, "ambient_intensity")
loc_diffuse_intensity     = glGetUniformLocation(program, "diffuse_intensity")
loc_specular_intensity    = glGetUniformLocation(program, "specular_intensity")

loc_light_sun_enabled = glGetUniformLocation(program, "light_sun_enabled")
loc_sun_pos           = glGetUniformLocation(program, "sun_pos")
loc_sun_color         = glGetUniformLocation(program, "sun_color")

loc_light_candle_enabled = glGetUniformLocation(program, "light_candle_enabled")
loc_candle_pos           = glGetUniformLocation(program, "candle_pos")
loc_candle_color         = glGetUniformLocation(program, "candle_color")

loc_light_lantern_enabled = glGetUniformLocation(program, "light_lantern_enabled")
loc_lantern_pos           = glGetUniformLocation(program, "lantern_pos")
loc_lantern_color         = glGetUniformLocation(program, "lantern_color")


# =========================================================================
# Carga de geometria — uma lista (chave, caminho) dirige o carregamento.
# raw_normals e' novo no Projeto 3 (necessario para iluminacao).
# =========================================================================
OBJ_FILES = [
    ("caixa",        "./objetos/caixa/caixa.obj"),
    ("snowTerrain",  "./objetos/snowTerrain/SnowTerrain.obj"),
    ("jeep",         "./objetos/Jeep/Jeep_Renegade_2016.obj"),
    ("ground",       "./objetos/ground/ground.obj"),
    ("sky",          "./objetos/sky/esfera.obj"),
    ("campfire",     "./objetos/campfire/campfire.obj"),
    ("pineTree",     "./objetos/pineTree/pineTree.obj"),
    ("rocket",       "./objetos/rocket/rocket2.obj"),
    ("table",        "./objetos/table/table.obj"),
    ("cartoonHouse", "./objetos/cartoonHouse/cartoonHouse.obj"),
    ("telescope",    "./objetos/telescope/telescope.obj"),
    ("forge",        "./objetos/forge/forge.obj"),
    ("satelite",     "./objetos/satelite/satelite.obj"),
    ("rockTiles",    "./objetos/rockTiles/rockTiles.obj"),
    ("treeStump",    "./objetos/treeStump/treeStump.obj"),
    ("outerWilds",   "./objetos/outerWilds/outerWilds.obj"),
    ("wallBox",      "./objetos/walls/wallBox.obj"),
    ("bed",          "./objetos/bed/bed.obj"),
    ("chair",        "./objetos/chair/chair.obj"),
    ("shelf",        "./objetos/shelf/shelf.obj"),
    ("door",         "./objetos/door/door.obj"),
    ("shelfWall",    "./objetos/shelfWall/shelfWall.obj"),
    ("foodCan",      "./objetos/foodCan/foodCan.obj"),
    ("barrel",       "./objetos/barrel/barrel.obj"),
    ("axe",          "./objetos/axe/axe.obj"),
    ("gun",          "./objetos/gun/gun.obj"),
    ("hammer",       "./objetos/hammer/hammer.obj"),
    ("pileOfBooks",  "./objetos/pileOfBooks/pileOfBooks.obj"),
    ("bascket",      "./objetos/bascket/bascket.obj"),
    ("jar",          "./objetos/jar/jar.obj"),
    ("plate",        "./objetos/plate/plate.obj"),
    ("mug",          "./objetos/mug/mug.obj"),
    ("knife",        "./objetos/knife/knife.obj"),
    ("pear",         "./objetos/pear/pear.obj"),
    ("apple",        "./objetos/apple/apple.obj"),
    ("candle",       "./objetos/candle/candle.obj"),
    ("globe",        "./objetos/globe/globe.obj"),
    ("map",          "./objetos/map/map.obj"),
    ("painting",     "./objetos/painting/painting.obj"),
    ("oxygen",       "./objetos/oxygen/oxygen.obj"),
    ("lantern",      "./objetos/lantern/lantern.obj"),
    ("chandelier",   "./objetos/chandelier/chandelier.obj"),
]

raw_vertices = []
raw_texcoords = []
raw_normals = []
objects_dict = {}

for _key, _path in OBJ_FILES:
    _v, _t, _n = load_obj_geometry(_path)
    _ini = len(raw_vertices)
    raw_vertices += _v
    raw_texcoords += _t
    raw_normals += _n
    objects_dict[_key] = {"ini_index": _ini, "end_index": len(raw_vertices)}


allocate_positions_on_gpu(raw_vertices, loc_position)
allocate_texcoords_on_gpu(raw_texcoords, loc_texture_coord)
allocate_normals_on_gpu(raw_normals, loc_normal)

# Texturas — cada id é reservado e carregado por load_texture()
texture_id              = load_texture("./objetos/caixa/caixa.jpg")
snow_texture_id         = load_texture("./objetos/snowTerrain/686.jpg")
jeep_texture_id         = load_texture("./objetos/Jeep/car_jeep_ren.jpg")
ground_texture_id       = load_texture("./objetos/ground/text_Albedo.png")
sky_texture_id          = load_texture("./objetos/sky/NightSky4k.jpg")
campfire_texture_id     = load_texture("./objetos/campfire/campfire.jpg")
mars_texture_id         = load_texture("./objetos/planet/mars.jpg")
moon_texture_id         = load_texture("./objetos/planet/moon.jpg")
pineTree_texture_id     = load_texture("./objetos/pineTree/pineTree.png")
rocket_texture_id       = load_texture("./objetos/rocket/rocket2.png")
table_texture_id        = load_texture("./objetos/table/table.png")
cartoonHouse_texture_id = load_texture("./objetos/cartoonHouse/cartoonHouse.png")
woodPlanks_texture_id   = load_texture("./objetos/caixa/woodPlank.jpeg")
telescope_texture_id    = load_texture("./objetos/telescope/telescope.png")
forge_texture_id        = load_texture("./objetos/forge/forge.png")
satelite_texture_id     = load_texture("./objetos/satelite/satelite.png")
rockTiles_texture_id    = load_texture("./objetos/rockTiles/rockTiles.png")
treeStump_texture_id    = load_texture("./objetos/treeStump/treeStump.png")
outerWilds_texture_id   = load_texture("./objetos/outerWilds/outerWilds.png")
wallBox_texture_id      = load_texture("./objetos/walls/wallBox.png")
bed_texture_id          = load_texture("./objetos/bed/bed.png")
chair_texture_id        = load_texture("./objetos/chair/chair.png")
shelf_texture_id        = load_texture("./objetos/shelf/shelf.png")
door_texture_id         = load_texture("./objetos/door/door.png")
shelfWall_texture_id    = load_texture("./objetos/shelfWall/shelfWall.png")
foodCan_texture_id      = load_texture("./objetos/foodCan/foodCan.png")
barrel_texture_id       = load_texture("./objetos/barrel/barrel.png")
axe_texture_id          = load_texture("./objetos/axe/axe.png")
gun_texture_id          = load_texture("./objetos/gun/gun.png")
hammer_texture_id       = load_texture("./objetos/hammer/hammer.png")
pileOfBooks_texture_id  = load_texture("./objetos/pileOfBooks/pileOfBooks.png")
bascket_texture_id      = load_texture("./objetos/bascket/bascket.png")
jar_texture_id          = load_texture("./objetos/jar/jar.png")
plate_texture_id        = load_texture("./objetos/plate/plate.png")
mug_texture_id          = load_texture("./objetos/mug/mug.png")
knife_texture_id        = load_texture("./objetos/knife/knife.png")
pear_texture_id         = load_texture("./objetos/pear/pear.png")
apple_texture_id        = load_texture("./objetos/apple/apple.png")
candle_texture_id       = load_texture("./objetos/candle/candle.png")
globe_texture_id        = load_texture("./objetos/globe/globe.png")
map_texture_id          = load_texture("./objetos/map/map.png")
painting_texture_id     = load_texture("./objetos/painting/painting.png")
oxygen_texture_id       = load_texture("./objetos/oxygen/oxygen.png")
lantern_texture_id      = load_texture("./objetos/lantern/lantern.png")
chandelier_texture_id   = load_texture("./objetos/chandelier/chandelier.png")


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


# =========================================================================
# SHADOW MAP — FBO de profundidade visto do sol (Projeto 3)
#
# Renderizamos a cena externa do ponto de vista do sol gravando apenas a
# profundidade. Objetos atrás do planeta ficam "mais longe" que a superfície
# já gravada → são detectados como sombra, independentemente da normal.
# =========================================================================
shadow_fbo = glGenFramebuffers(1)
shadow_map = glGenTextures(1)

glBindTexture(GL_TEXTURE_2D, shadow_map)
glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT,
             SHADOW_WIDTH, SHADOW_HEIGHT, 0,
             GL_DEPTH_COMPONENT, GL_FLOAT, None)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR,
                 np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32))
# Amostragem direta da profundidade (sem comparação automática)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_MODE, GL_NONE)

glBindFramebuffer(GL_FRAMEBUFFER, shadow_fbo)
glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT,
                       GL_TEXTURE_2D, shadow_map, 0)
glDrawBuffer(GL_NONE)   # sem buffer de cor
glReadBuffer(GL_NONE)
glBindFramebuffer(GL_FRAMEBUFFER, 0)

# shadowMap fica fixo na unidade de textura 1 (a 0 é a textura dos objetos)
glActiveTexture(GL_TEXTURE1)
glBindTexture(GL_TEXTURE_2D, shadow_map)
glUniform1i(loc_shadow_map, 1)
glActiveTexture(GL_TEXTURE0)


def compute_light_space_matrix():
    """Matriz projeção*view da luz (sol), para gerar e amostrar o shadow map.

    Projeção ortográfica olhando do sol para o centro do planeta, com volume
    grande o bastante para cobrir o planeta (raio ~48) e os objetos em órbita.
    """
    light_dir = glm.normalize(planetCenter - sun_pos)
    # 'up' auxiliar que não seja paralelo à direção da luz
    up = glm.vec3(0.0, 1.0, 0.0)
    if abs(glm.dot(light_dir, up)) > 0.99:
        up = glm.vec3(1.0, 0.0, 0.0)

    light_view = glm.lookAt(sun_pos, planetCenter, up)
    ortho = 130.0
    light_proj = glm.ortho(-ortho, ortho, -ortho, ortho, 1.0, 500.0)
    return np.array(light_proj * light_view, dtype=np.float32)


def send_light_uniforms():
    """Envia, uma vez por frame, todos os uniforms de iluminação ao shader."""
    glUniform3f(loc_view_pos, cameraPos.x, cameraPos.y, cameraPos.z)

    glUniform1i(loc_light_ambient_enabled, int(light_ambient_enabled))
    glUniform1f(loc_ambient_intensity, ambient_intensity)
    glUniform1f(loc_diffuse_intensity, diffuse_intensity)
    glUniform1f(loc_specular_intensity, specular_intensity)

    glUniform1i(loc_light_sun_enabled, int(light_sun_enabled))
    glUniform3f(loc_sun_pos, sun_pos.x, sun_pos.y, sun_pos.z)
    glUniform3f(loc_sun_color, sun_color.x, sun_color.y, sun_color.z)

    glUniform1i(loc_light_candle_enabled, int(light_candle_enabled))
    glUniform3f(loc_candle_pos, candle_pos.x, candle_pos.y, candle_pos.z)
    glUniform3f(loc_candle_color, candle_color.x, candle_color.y, candle_color.z)

    glUniform1i(loc_light_lantern_enabled, int(light_lantern_enabled))
    glUniform3f(loc_lantern_pos, lantern_pos.x, lantern_pos.y, lantern_pos.z)
    glUniform3f(loc_lantern_color, lantern_color.x, lantern_color.y, lantern_color.z)


glfw.show_window(window)

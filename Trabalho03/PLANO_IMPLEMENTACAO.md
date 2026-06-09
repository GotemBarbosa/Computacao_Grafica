# Plano de Implementação — Projeto 3 (Iluminação + Shadow Mapping)

## Diagnóstico do Estado Atual

| Componente | Estado Atual |
|---|---|
| Shaders | `#version 120`, sem iluminação, só textura |
| Normais | **Não existem** — `obj_loader` só extrai posições e UVs |
| Luzes | Nenhuma |
| Sombras | Nenhuma |
| Controles | Foguete (↑↓), Telescópio (←→), Marte (Q/E), Wireframe (P) |

---

## Etapa 1 — Extrair Normais dos OBJs

**Arquivo:** `objetos/obj_loader.py`

- Ler linhas `vn` do arquivo `.obj`
- Ler os índices de normais nos faces (`f v/vt/vn`)
- Retornar uma lista `raw_normals` paralela a `raw_vertices`
- **Fallback:** se o `.obj` não tiver `vn`, calcular normal por face como produto vetorial dos dois primeiros vértices do triângulo

**Arquivo:** `state.py`

- Criar `loc_normal = glGetAttribLocation(program, "normal")`
- Criar função `allocate_normals_on_gpu(raw_normals, loc_normal)` análoga à de posições
- Chamar ao final do bloco de carga de geometria junto com posições e UVs

---

## Etapa 2 — Atualizar Shaders para GLSL 330

**Motivo:** `#version 120` não suporta `in/out`, `layout`, nem `texture()` moderno. Shadow mapping requer `sampler2DShadow` disponível a partir de 130+. A migração para 330 core garante compatibilidade com todas as funcionalidades necessárias.

### `shaders/vertex_shader.vs`

```glsl
#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texture_coord;
layout(location = 2) in vec3 normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 lightSpaceMatrix;   // matriz da perspectiva do sol, para shadow map

out vec2  out_texture;
out vec3  fragPos;               // posição world-space
out vec3  fragNormal;            // normal world-space
out vec4  fragPosLightSpace;     // posição no espaço da luz (para shadow map)

void main() {
    vec4 worldPos    = model * vec4(position, 1.0);
    gl_Position      = projection * view * worldPos;
    out_texture      = texture_coord;
    fragPos          = vec3(worldPos);
    fragNormal       = normalize(mat3(transpose(inverse(model))) * normal);
    fragPosLightSpace = lightSpaceMatrix * worldPos;
}
```

### `shaders/fragment_shader.fs`

```glsl
#version 330 core

in vec2  out_texture;
in vec3  fragPos;
in vec3  fragNormal;
in vec4  fragPosLightSpace;

out vec4 fragColor;

// --- Textura ---
uniform sampler2D imagem;
uniform int       use_texture;
uniform vec4      base_color;

// --- Shadow Map ---
uniform sampler2D shadowMap;

// --- Flags de contexto ---
uniform int is_internal;          // 0 = externo, 1 = interno

// --- Parâmetros de material (por objeto) ---
uniform float Ka;                 // coeficiente ambiente
uniform float Kd;                 // coeficiente difuso
uniform float Ks;                 // coeficiente especular
uniform float shininess;

// --- Câmera ---
uniform vec3 viewPos;

// --- Luzes ---
uniform int   light_ambient_enabled;
uniform float ambient_intensity;
uniform float diffuse_intensity;
uniform float specular_intensity;

// Luz externa (sol)
uniform int  light_sun_enabled;
uniform vec3 sun_pos;
uniform vec3 sun_color;

// Luz interna 1 (vela — quente)
uniform int  light_candle_enabled;
uniform vec3 candle_pos;
uniform vec3 candle_color;

// Luz interna 2 (luminária — fria)
uniform int  light_lantern_enabled;
uniform vec3 lantern_pos;
uniform vec3 lantern_color;

// --- Funções auxiliares ---

float calcShadow(vec4 posLightSpace) {
    vec3 proj = posLightSpace.xyz / posLightSpace.w;
    proj = proj * 0.5 + 0.5;
    if (proj.z > 1.0) return 0.0;          // fora do frustum da luz → sem sombra
    float closest = texture(shadowMap, proj.xy).r;
    float current = proj.z;
    float bias    = max(0.005 * (1.0 - dot(fragNormal, normalize(sun_pos - fragPos))), 0.001);
    return current - bias > closest ? 1.0 : 0.0;  // 1.0 = em sombra
}

vec3 calcPointLight(vec3 lightPos, vec3 lightColor, float shadowFactor) {
    vec3  L         = normalize(lightPos - fragPos);
    float diff      = max(dot(fragNormal, L), 0.0);
    vec3  V         = normalize(viewPos - fragPos);
    vec3  H         = normalize(L + V);
    float spec      = pow(max(dot(fragNormal, H), 0.0), shininess);
    float dist      = length(lightPos - fragPos);
    float atten     = 1.0 / (1.0 + 0.045 * dist + 0.0075 * dist * dist);
    float lit       = 1.0 - shadowFactor;

    vec3 diffuse  = Kd * diffuse_intensity  * diff * lightColor * atten * lit;
    vec3 specular = Ks * specular_intensity * spec * lightColor * atten * lit;
    return diffuse + specular;
}

void main() {
    vec3 texColor = use_texture == 1
        ? vec3(texture(imagem, out_texture))
        : vec3(base_color);

    vec3 result = vec3(0.0);

    // Ambient global
    if (light_ambient_enabled == 1)
        result += Ka * ambient_intensity * texColor;

    if (is_internal == 0) {
        // --- Ambiente EXTERNO: só luz do sol + shadow map ---
        if (light_sun_enabled == 1) {
            float shadow = calcShadow(fragPosLightSpace);
            result += calcPointLight(sun_pos, sun_color, shadow) * texColor;
        }
    } else {
        // --- Ambiente INTERNO: vela + luminária (sem shadow map) ---
        if (light_candle_enabled == 1)
            result += calcPointLight(candle_pos, candle_color, 0.0) * texColor;
        if (light_lantern_enabled == 1)
            result += calcPointLight(lantern_pos, lantern_color, 0.0) * texColor;
    }

    fragColor = vec4(result, 1.0);
}
```

---

## Etapa 3 — Shaders de Profundidade (Depth Pass)

Novos arquivos usados apenas na primeira passada de renderização (geração do shadow map).

### `shaders/depth_vertex.vs`

```glsl
#version 330 core
layout(location = 0) in vec3 position;
uniform mat4 lightSpaceMatrix;
uniform mat4 model;
void main() {
    gl_Position = lightSpaceMatrix * model * vec4(position, 1.0);
}
```

### `shaders/depth_fragment.fs`

```glsl
#version 330 core
// Vazio — OpenGL grava automaticamente a profundidade em gl_FragDepth
void main() {}
```

---

## Etapa 4 — Sistema de Materiais

**Novo arquivo:** `materials.py`

Parâmetros Ka, Kd, Ks e shininess definidos manualmente para cada objeto. **Nenhum valor vem de arquivo `.mtl`.**

```python
# Ka  = coeficiente ambiente   (quão forte a luz ambiente afeta o objeto)
# Kd  = coeficiente difuso     (quão fosco é o objeto)
# Ks  = coeficiente especular  (quão brilhante é o objeto)
# shi = shininess              (foco do brilho — maior = mais pontual)

MATERIALS = {
    # --- Externos ---
    "planeta":       {"Ka": 0.10, "Kd": 0.85, "Ks": 0.05, "shi": 4},
    "sky":           {"Ka": 1.00, "Kd": 0.00, "Ks": 0.00, "shi": 1},   # skybox não recebe luz
    "pineTree":      {"Ka": 0.20, "Kd": 0.90, "Ks": 0.02, "shi": 4},
    "treeStump":     {"Ka": 0.20, "Kd": 0.80, "Ks": 0.05, "shi": 4},
    "rockTiles":     {"Ka": 0.15, "Kd": 0.75, "Ks": 0.10, "shi": 8},
    "cartoonHouse":  {"Ka": 0.20, "Kd": 0.70, "Ks": 0.10, "shi": 8},
    "forge":         {"Ka": 0.10, "Kd": 0.60, "Ks": 0.40, "shi": 32},
    "rocket":        {"Ka": 0.10, "Kd": 0.50, "Ks": 0.70, "shi": 64},
    "telescope":     {"Ka": 0.10, "Kd": 0.50, "Ks": 0.70, "shi": 64},
    "satelite":      {"Ka": 0.10, "Kd": 0.55, "Ks": 0.65, "shi": 48},
    "outerWilds":    {"Ka": 0.10, "Kd": 0.55, "Ks": 0.50, "shi": 32},
    "fogueira":      {"Ka": 0.40, "Kd": 0.60, "Ks": 0.00, "shi": 1},
    "lua":           {"Ka": 0.10, "Kd": 0.85, "Ks": 0.05, "shi": 4},
    "marte":         {"Ka": 0.10, "Kd": 0.85, "Ks": 0.05, "shi": 4},
    "sol":           {"Ka": 1.00, "Kd": 0.00, "Ks": 0.00, "shi": 1},   # emissivo
    "caixa":         {"Ka": 0.20, "Kd": 0.75, "Ks": 0.10, "shi": 8},
    "woodPlanks":    {"Ka": 0.20, "Kd": 0.75, "Ks": 0.05, "shi": 4},

    # --- Internos ---
    "bed":           {"Ka": 0.25, "Kd": 0.75, "Ks": 0.05, "shi": 4},
    "chair":         {"Ka": 0.20, "Kd": 0.70, "Ks": 0.10, "shi": 8},
    "table":         {"Ka": 0.20, "Kd": 0.70, "Ks": 0.15, "shi": 8},
    "shelf":         {"Ka": 0.20, "Kd": 0.70, "Ks": 0.10, "shi": 8},
    "shelfWall":     {"Ka": 0.20, "Kd": 0.70, "Ks": 0.10, "shi": 8},
    "door":          {"Ka": 0.20, "Kd": 0.70, "Ks": 0.10, "shi": 8},
    "barrel":        {"Ka": 0.20, "Kd": 0.65, "Ks": 0.15, "shi": 8},
    "candle":        {"Ka": 0.50, "Kd": 0.50, "Ks": 0.00, "shi": 1},   # emissivo
    "lantern":       {"Ka": 0.50, "Kd": 0.50, "Ks": 0.30, "shi": 16},  # emissivo
    "chandelier":    {"Ka": 0.50, "Kd": 0.50, "Ks": 0.30, "shi": 16},
    "axe":           {"Ka": 0.10, "Kd": 0.50, "Ks": 0.80, "shi": 64},
    "hammer":        {"Ka": 0.10, "Kd": 0.50, "Ks": 0.80, "shi": 64},
    "gun":           {"Ka": 0.10, "Kd": 0.45, "Ks": 0.85, "shi": 96},
    "foodCan":       {"Ka": 0.15, "Kd": 0.50, "Ks": 0.75, "shi": 64},
    "mug":           {"Ka": 0.20, "Kd": 0.60, "Ks": 0.50, "shi": 32},
    "plate":         {"Ka": 0.20, "Kd": 0.55, "Ks": 0.60, "shi": 48},
    "jar":           {"Ka": 0.20, "Kd": 0.60, "Ks": 0.55, "shi": 32},
    "knife":         {"Ka": 0.10, "Kd": 0.40, "Ks": 0.90, "shi": 128},
    "bascket":       {"Ka": 0.20, "Kd": 0.80, "Ks": 0.05, "shi": 4},
    "apple":         {"Ka": 0.20, "Kd": 0.85, "Ks": 0.20, "shi": 16},
    "pear":          {"Ka": 0.20, "Kd": 0.85, "Ks": 0.20, "shi": 16},
    "pileOfBooks":   {"Ka": 0.20, "Kd": 0.75, "Ks": 0.05, "shi": 4},
    "globe":         {"Ka": 0.20, "Kd": 0.65, "Ks": 0.50, "shi": 32},
    "map":           {"Ka": 0.20, "Kd": 0.80, "Ks": 0.05, "shi": 4},
    "painting":      {"Ka": 0.25, "Kd": 0.75, "Ks": 0.05, "shi": 4},
    "oxygen":        {"Ka": 0.10, "Kd": 0.50, "Ks": 0.80, "shi": 64},
}
```

**Em `scene_objects.py`:** helper para enviar o material ao shader:

```python
from materials import MATERIALS

def set_material(name):
    m = MATERIALS[name]
    glUniform1f(state.loc_Ka,        m["Ka"])
    glUniform1f(state.loc_Kd,        m["Kd"])
    glUniform1f(state.loc_Ks,        m["Ks"])
    glUniform1f(state.loc_shininess, m["shi"])
```

Cada `desenha_*` chama `set_material("nome")` antes do `glDrawArrays`.

---

## Etapa 5 — Estado de Iluminação no `state.py`

```python
import glm

# === SOL (luz externa, orbita o planeta) ===
sun_orbit_angle  = 0.0
sun_orbit_speed  = 10.0          # graus/segundo
sun_orbit_radius = 200.0
sun_pos          = glm.vec3(200.0, 0.0, 0.0)   # atualizado todo frame
sun_color        = glm.vec3(1.0, 0.95, 0.8)    # branco-amarelado

# === VELA (luz interna 1 — quente) ===
# posição da vela na mesa (mesma de main.py)
candle_pos   = glm.vec3(-2.1, -0.52, 4.25)
candle_color = glm.vec3(1.0, 0.55, 0.05)       # laranja quente

# === LUMINÁRIA (luz interna 2 — fria) ===
# usar a lantern posicionada na prateleira
lantern_pos   = glm.vec3(2.92, -0.6, 3.7)
lantern_color = glm.vec3(0.35, 0.25, 1.0)      # azul/roxo

# === TOGGLES (cada luz tem seu interruptor) ===
light_sun_enabled     = True
light_candle_enabled  = True
light_lantern_enabled = True
light_ambient_enabled = True

# === INTENSIDADES AJUSTÁVEIS POR TECLADO ===
ambient_intensity  = 0.15   # intervalo sugerido: [0.0, 1.0]
diffuse_intensity  = 1.0    # multiplicador global do Kd
specular_intensity = 1.0    # multiplicador global do Ks

INTENSITY_STEP = 0.05       # quanto cada tecla incrementa/decrementa
```

---

## Etapa 6 — FBO e Shadow Map

No bloco de inicialização do OpenGL em `state.py`, após criar o shader principal:

```python
SHADOW_WIDTH  = 2048
SHADOW_HEIGHT = 2048

shadow_fbo = glGenFramebuffers(1)
shadow_map  = glGenTextures(1)

glBindTexture(GL_TEXTURE_2D, shadow_map)
glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT,
             SHADOW_WIDTH, SHADOW_HEIGHT, 0,
             GL_DEPTH_COMPONENT, GL_FLOAT, None)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR,
                 np.array([1, 1, 1, 1], dtype=np.float32))

glBindFramebuffer(GL_FRAMEBUFFER, shadow_fbo)
glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT,
                       GL_TEXTURE_2D, shadow_map, 0)
glDrawBuffer(GL_NONE)
glReadBuffer(GL_NONE)
glBindFramebuffer(GL_FRAMEBUFFER, 0)

# Shader separado só para o depth pass
depthShader = Shader("./shaders/depth_vertex.vs", "./shaders/depth_fragment.fs")
```

---

## Etapa 7 — Loop de Renderização em Duas Passadas

**Arquivo:** `main.py` — função `draw_scene()`

```python
def draw_scene():
    glfw.swap_interval(1)
    state.lastFrame = glfw.get_time()
    init_objetos_estaticos()

    while not glfw.window_should_close(state.window):
        # --- UPDATE ---
        atualiza_tempo_e_fps()
        state.update_move_front_camera()
        movement()
        atualiza_gravity_weight()

        # Avança órbita do sol e atualiza posição
        state.sun_orbit_angle = (state.sun_orbit_angle
                                  + state.sun_orbit_speed * state.deltaTime) % 360.0
        state.sun_pos = planet_to_world_coordenates(
            lat=20, lon=state.sun_orbit_angle,
            radius=state.sun_orbit_radius,
            center=state.planetCenter
        )

        # Calcula lightSpaceMatrix (ortho centrada no planeta, olhando do sol)
        light_dir   = glm.normalize(state.planetCenter - state.sun_pos)
        light_view  = glm.lookAt(state.sun_pos,
                                  state.sun_pos + light_dir,
                                  glm.vec3(0, 1, 0))
        ortho_size  = 120.0
        light_proj  = glm.ortho(-ortho_size, ortho_size,
                                 -ortho_size, ortho_size,
                                 1.0, 600.0)
        lightSpaceMat = np.array(light_proj * light_view, dtype=np.float32)

        # =============================================
        # PASSADA 1 — Gerar Shadow Map
        # =============================================
        state.depthShader.use()
        glUniformMatrix4fv(state.loc_depth_lightSpace, 1, GL_TRUE, lightSpaceMat)

        glViewport(0, 0, state.SHADOW_WIDTH, state.SHADOW_HEIGHT)
        glBindFramebuffer(GL_FRAMEBUFFER, state.shadow_fbo)
        glClear(GL_DEPTH_BUFFER_BIT)

        desenha_objetos_externos_depth()   # só objetos externos

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # =============================================
        # PASSADA 2 — Renderizar Cena Normal
        # =============================================
        state.ourShader.use()
        glViewport(0, 0, 1920, 1080)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.02, 0.02, 0.05, 1.0)

        # Passar shadow map na unidade de textura 1
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, state.shadow_map)
        glUniform1i(state.loc_shadowMap, 1)
        glActiveTexture(GL_TEXTURE0)

        # Matrizes de câmera
        glUniformMatrix4fv(state.loc_view,       1, GL_TRUE, state.view())
        glUniformMatrix4fv(state.loc_projection, 1, GL_TRUE, state.projection())
        glUniformMatrix4fv(state.loc_lightSpace, 1, GL_TRUE, lightSpaceMat)

        # Uniforms de iluminação
        enviar_uniforms_luz()

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        desenha_cenario_estatico()
        desenha_objetos_planeta()
        desenha_objetos_casa()

        glfw.swap_buffers(state.window)
        glfw.poll_events()

    glfw.terminate()
```

---

## Etapa 8 — Controles de Teclado

Remover de `key_event()`:
- `P` (wireframe)
- `Q` / `E` (escala de Marte)
- `↑` / `↓` (foguete)
- `←` / `→` (telescópio)

Adicionar:

```python
# --- INTERRUPTORES DE LUZ ---
if key == glfw.KEY_1 and action == glfw.PRESS:
    light_sun_enabled = not light_sun_enabled

if key == glfw.KEY_2 and action == glfw.PRESS:
    light_candle_enabled = not light_candle_enabled

if key == glfw.KEY_3 and action == glfw.PRESS:
    light_lantern_enabled = not light_lantern_enabled

if key == glfw.KEY_4 and action == glfw.PRESS:
    light_ambient_enabled = not light_ambient_enabled

# --- LUZ AMBIENTE (+/-) ---
if key == glfw.KEY_LEFT_BRACKET and action in (glfw.PRESS, glfw.REPEAT):
    ambient_intensity = max(0.0, ambient_intensity - INTENSITY_STEP)
if key == glfw.KEY_RIGHT_BRACKET and action in (glfw.PRESS, glfw.REPEAT):
    ambient_intensity = min(1.0, ambient_intensity + INTENSITY_STEP)

# --- REFLEXÃO DIFUSA (+/-) ---
if key == glfw.KEY_SEMICOLON and action in (glfw.PRESS, glfw.REPEAT):
    diffuse_intensity = max(0.0, diffuse_intensity - INTENSITY_STEP)
if key == glfw.KEY_APOSTROPHE and action in (glfw.PRESS, glfw.REPEAT):
    diffuse_intensity = min(2.0, diffuse_intensity + INTENSITY_STEP)

# --- REFLEXÃO ESPECULAR (+/-) ---
if key == glfw.KEY_COMMA and action in (glfw.PRESS, glfw.REPEAT):
    specular_intensity = max(0.0, specular_intensity - INTENSITY_STEP)
if key == glfw.KEY_PERIOD and action in (glfw.PRESS, glfw.REPEAT):
    specular_intensity = min(2.0, specular_intensity + INTENSITY_STEP)
```

---

## Etapa 9 — Sol Visual na Cena

**Arquivo:** `main.py`

```python
def sol():
    # Representação visual do sol (esfera amarela)
    glUniform1i(state.loc_is_internal, 0)
    set_material("sol")   # Ka=1, Kd=0, Ks=0 → aparece sempre iluminado
    desenha_planet(
        angle=0, r_x=0, r_y=1, r_z=0,
        t_x=state.sun_pos.x,
        t_y=state.sun_pos.y,
        t_z=state.sun_pos.z,
        s_x=8, s_y=8, s_z=8,
        texture_id=state.sun_texture_id
    )
```

Adicionar textura do sol em `state.py`:
```python
sun_texture_id = glGenTextures(1)
load_texture_from_file(sun_texture_id, "./objetos/planet/sun.jpg")
```

---

## Checklist de Implementação

```
[ ] Etapa 1 — obj_loader.py: extrair normais + fallback por face
[ ] Etapa 2 — vertex_shader.vs: GLSL 330 + normal + fragPos
[ ] Etapa 2 — fragment_shader.fs: GLSL 330 + Phong + shadow map + isolamento
[ ] Etapa 3 — depth_vertex.vs + depth_fragment.fs (depth pass)
[ ] Etapa 4 — materials.py: Ka/Kd/Ks/shininess para todos os objetos
[ ] Etapa 4 — scene_objects.py: set_material() + is_internal antes de cada draw
[ ] Etapa 5 — state.py: variáveis de estado das luzes e intensidades
[ ] Etapa 6 — state.py: criar FBO + shadow map texture + depthShader
[ ] Etapa 7 — main.py: duas passadas de renderização + sol orbitando
[ ] Etapa 8 — state.py key_event(): novos controles, remover antigos
[ ] Etapa 9 — main.py: desenhar esfera do sol + textura
[ ] Teste — lado escuro do planeta fica escuro quando sol passa atrás
[ ] Teste — toggle 1/2/3/4 muda visivelmente a iluminação
[ ] Teste — [ ] e ] alteram brilho ambiente
[ ] Teste — objetos internos não são afetados pelo sol
[ ] Teste — objetos externos não são afetados pelas velas
```

---

## Ordem de Implementação Recomendada

| Ordem | Etapa | Por quê primeiro |
|---|---|---|
| 1 | Normais no obj_loader | Bloqueia tudo — sem normal não há Phong |
| 2 | Atualizar shaders (330 + Phong básico sem sombra) | Validar iluminação antes de adicionar shadow map |
| 3 | Materials.py + set_material() | Ver diferença visual entre objetos |
| 4 | Estado das luzes + toggles de teclado | Validar interruptores funcionando |
| 5 | FBO + depth shaders + two-pass render | Shadow map em si |
| 6 | Sol orbitando + textura | Fonte de luz externa completa |
| 7 | Isolamento is_internal | Separação externo/interno |
| 8 | Ajuste fino de materiais e intensidades | Polimento visual |

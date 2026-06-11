#version 120

varying vec2 out_texture;
varying vec3 fragPos;
varying vec3 fragNormal;
varying vec4 fragPosLightSpace;

// --- Textura / cor base ---
uniform sampler2D imagem;
uniform int       use_texture;
uniform vec4      base_color;

// --- Shadow map (profundidade vista do sol) ---
uniform sampler2D shadowMap;

// 1 = passada de profundidade; 0 = render normal
uniform int depthPass;

// 0 = objeto externo (recebe o sol); 1 = objeto interno (recebe velas/luminárias)
uniform int is_internal;

// 1 = objeto sem iluminação (skybox, sol): mostra a cor/textura direto
uniform int unlit;

// --- Parâmetros de material (próprios de cada objeto, sem .mtl) ---
uniform float Ka;          // coeficiente ambiente
uniform float Kd;          // coeficiente difuso
uniform float Ks;          // coeficiente especular
uniform float shininess;

// --- Câmera ---
uniform vec3 viewPos;

// --- Intensidades globais ajustáveis por teclado ---
uniform int   light_ambient_enabled;
uniform float ambient_intensity;
uniform float diffuse_intensity;
uniform float specular_intensity;

// --- Luz externa: sol ---
uniform int   light_sun_enabled;
uniform vec3  sun_pos;
uniform vec3  sun_color;
uniform float sun_intensity;   // 1 = sol pleno; 0 = eclipsado por Marte

// --- Luz interna 1: vela (quente) ---
uniform int   light_candle_enabled;
uniform vec3  candle_pos;
uniform vec3  candle_color;
uniform float candle_intensity;   // oscila no tempo (flicker) e dá força à vela

// --- Luz interna 2: luminária (fria) ---
uniform int  light_lantern_enabled;
uniform vec3 lantern_pos;
uniform vec3 lantern_color;

// --- Luzes externas: fogueiras (quentes, com atenuação) ---
uniform int   light_fire_enabled;
uniform vec3  fire_pos[2];
uniform vec3  fire_color[2];
uniform float fire_intensity;   // força da fogueira (separada da cor)


// Fator de sombra do planeta: 1.0 = totalmente na sombra, 0.0 = iluminado.
// Compara a profundidade do fragmento (vista do sol) com a profundidade
// mais próxima gravada no shadow map.
float calcShadow() {
    vec3 proj = fragPosLightSpace.xyz / fragPosLightSpace.w;
    proj = proj * 0.5 + 0.5;

    // Fora do frustum da luz → considera iluminado
    if (proj.z > 1.0 || proj.x < 0.0 || proj.x > 1.0 ||
        proj.y < 0.0 || proj.y > 1.0)
        return 0.0;

    float current = proj.z;

    // Bias proporcional ao ângulo da superfície com o sol, contra "shadow acne"
    vec3  L    = normalize(sun_pos - fragPos);
    float bias = max(0.0025 * (1.0 - dot(normalize(fragNormal), L)), 0.0008);

    // PCF: amostra um kernel 5x5 ao redor e tira a média dos testes.
    // Em vez de um "0 ou 1" duro, isso dá um valor contínuo na borda da
    // sombra (penumbra) → transição suave em vez de serrilhado.
    // O 'spread' alarga a penumbra (mais texels cobertos por amostra).
    float texel  = 1.0 / 4096.0;   // = 1 / SHADOW_WIDTH (manter em sincronia)
    float spread = 2.0;            // aumente para borrar mais
    float shadow = 0.0;
    for (int x = -2; x <= 2; x++) {
        for (int y = -2; y <= 2; y++) {
            vec2  offset  = vec2(float(x), float(y)) * texel * spread;
            float closest = texture2D(shadowMap, proj.xy + offset).r;
            shadow += current - bias > closest ? 1.0 : 0.0;
        }
    }
    return shadow / 25.0;
}


// Iluminação de uma fonte (difusa + especular Blinn-Phong).
// useAtten = 1 aplica atenuação por distância (luzes locais: vela/luminária).
// useAtten = 0 ignora a distância (sol: luz distante, quase direcional).
vec3 calcPointLight(vec3 lightPos, vec3 lightColor, float litFactor, int useAtten) {
    vec3  N    = normalize(fragNormal);
    vec3  L    = normalize(lightPos - fragPos);
    vec3  V    = normalize(viewPos - fragPos);
    vec3  H    = normalize(L + V);

    float diff = max(dot(N, L), 0.0);
    float spec = 0.0;

    // Só ilumina se a normal do fragmento tiver um angulo 0 <= theta <= 90
    if (diff > 0) {
        float cos = max(dot(N, H), 0.0);
        spec = pow(cos, shininess);
    }

    float atten = 1.0;
    if (useAtten == 1) {
        // Atenuação suave: vela / luminária (alcance maior)
        float dist = length(lightPos - fragPos);
        atten = 1.0 / (1.0 + 0.022 * dist + 0.0019 * dist * dist);
    } else if (useAtten == 2) {
        // Atenuação forte: fogueira (cai mais rápido com a distância)
        float dist = length(lightPos - fragPos);
        atten = 1.0 / (1.0 + 0.09 * dist + 0.032 * dist * dist);
    } else if (useAtten == 3) {
        // Vela: "poça" de luz — intensa bem de perto e caindo logo em seguida,
        // formando um halo concentrado em torno da chama.
        float dist = length(lightPos - fragPos);
        atten = 1.0 / (1.0 + 0.22 * dist + 0.20 * dist * dist);
    }

    vec3 diffuse  = Kd * diffuse_intensity  * diff * lightColor;
    vec3 specular = Ks * specular_intensity * spec * lightColor;

    return (diffuse + specular) * atten * litFactor;
}


void main() {
    // Passada de profundidade: o valor de cor é irrelevante (só a profundidade
    // é gravada no FBO). Saímos cedo para economizar trabalho.
    if (depthPass == 1) {
        gl_FragColor = vec4(1.0);
        return;
    }

    vec3 texColor = (use_texture == 1)
        ? vec3(texture2D(imagem, out_texture))
        : vec3(base_color);

    // Objetos não-iluminados (céu, sol) aparecem com brilho total
    if (unlit == 1) {
        gl_FragColor = vec4(texColor, 1.0);
        return;
    }

    vec3 result = vec3(0.0);

    // Componente ambiente (afeta todos os objetos quando ligada)
    if (light_ambient_enabled == 1)
        result += Ka * ambient_intensity * texColor;

    if (is_internal == 0) {
        // === AMBIENTE EXTERNO: sol (sem atenuação, com sombra) + fogueiras ===
        if (light_sun_enabled == 1) {
            float lit = 1.0 - calcShadow();
            result += calcPointLight(sun_pos, sun_color * sun_intensity, lit, 0) * texColor;
        }
        // Fogueiras: luzes locais quentes (com atenuação por distância)
        if (light_fire_enabled == 1) {
            for (int i = 0; i < 2; i++)
                result += calcPointLight(fire_pos[i], fire_color[i] * fire_intensity, 1.0, 2) * texColor;
        }
    } else {
        // === AMBIENTE INTERNO: vela + luminária (com atenuação, sem sombra) ===
        if (light_candle_enabled == 1)
            result += calcPointLight(candle_pos, candle_color * candle_intensity, 1.0, 3) * texColor;
        if (light_lantern_enabled == 1)
            result += calcPointLight(lantern_pos, lantern_color, 1.0, 1) * texColor;
    }

    gl_FragColor = vec4(result, 1.0);
}

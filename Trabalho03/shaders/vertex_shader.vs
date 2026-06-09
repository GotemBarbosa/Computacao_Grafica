#version 120

attribute vec3 position;
attribute vec2 texture_coord;
attribute vec3 normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// Matriz da perspectiva da luz (sol) — usada para o shadow map
uniform mat4 lightSpaceMatrix;

// Matriz de normais (inverse-transpose do model), calculada na CPU
// porque o GLSL 120 não possui as funções inverse()/transpose().
uniform mat3 normalMatrix;

// 1 = passada de profundidade (gera o shadow map); 0 = render normal
uniform int depthPass;

varying vec2 out_texture;
varying vec3 fragPos;            // posição em world-space
varying vec3 fragNormal;         // normal em world-space
varying vec4 fragPosLightSpace;  // posição no espaço da luz

void main() {
    vec4 worldPos = model * vec4(position, 1.0);

    if (depthPass == 1) {
        // Render do ponto de vista do sol: só a profundidade importa.
        gl_Position = lightSpaceMatrix * worldPos;
    } else {
        gl_Position = projection * view * worldPos;
    }

    out_texture       = texture_coord;
    fragPos           = vec3(worldPos);
    fragNormal        = normalize(normalMatrix * normal);
    fragPosLightSpace = lightSpaceMatrix * worldPos;
}

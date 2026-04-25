#version 120
varying vec2 out_texture;
uniform sampler2D imagem;
uniform int use_texture;
uniform vec4 base_color;

void main() {
    if (use_texture == 1) {
        gl_FragColor = texture2D(imagem, out_texture);
    } else {
        gl_FragColor = base_color;
    }
}

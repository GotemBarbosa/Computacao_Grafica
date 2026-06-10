import glm
import numpy as np
from OpenGL.GL import *
import state


# =========================================================================
# Helper genérico de desenho.
#
# Centraliza o que todo objeto faz: monta a matriz model, envia model +
# matriz de normais, envia o material (Ka/Kd/Ks/shininess) do objeto e então
# desenha o intervalo de vértices correspondente no VBO.
#
# A flag is_internal NÃO é definida aqui: ela é controlada por grupo em
# main.py (objetos internos da casa vs. objetos externos), pois determina
# quais luzes afetam o objeto.
# =========================================================================
def _draw(obj_key, mat_name, angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=None, texture_id=None, base_color=None,
          unlit=False, cull=True, invert_cull=False):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z,
                            s_x, s_y, s_z, base_rotation)
    state.upload_model(mat_model)          # model + matriz de normais
    state.set_material(mat_name)           # coeficientes de iluminação
    glUniform1i(state.loc_unlit, 1 if unlit else 0)

    if texture_id is not None:
        glUniform1i(state.loc_use_texture, 1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
    else:
        glUniform1i(state.loc_use_texture, 0)
        if base_color is not None:
            glUniform4f(state.loc_base_color, *base_color)

    ini = state.objects_dict[obj_key]["ini_index"]
    fim = state.objects_dict[obj_key]["end_index"]

    # Skybox (visto por dentro): sem culling, todas as faces precisam aparecer.
    if unlit or not cull:
        glDisable(GL_CULL_FACE)
        glDrawArrays(GL_TRIANGLES, ini, fim - ini)
        glEnable(GL_CULL_FACE)
    # Planeta/luas: reaproveitam a esfera "sky" (winding invertido), então a
    # face externa é "traseira". Cortamos a FRENTE — assim a metade de trás do
    # planeta ainda é descartada (ganho de culling), mas a visível permanece.
    elif invert_cull:
        glCullFace(GL_FRONT)
        glDrawArrays(GL_TRIANGLES, ini, fim - ini)
        glCullFace(GL_BACK)
    else:
        glDrawArrays(GL_TRIANGLES, ini, fim - ini)


# =========================================================================
# Objetos de cenário / externos
# =========================================================================

def desenha_caixa(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z,
                  texture_id, planet_rotation_matrix=None, mat_name="caixa"):
    _draw("caixa", mat_name, angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=texture_id)


def desenha_jeep(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("jeep", "jeep", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.jeep_texture_id)


def desenha_snow_terrain(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("snowTerrain", "snowTerrain", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, texture_id=state.snow_texture_id)


def desenha_ground(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("ground", "ground", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, texture_id=state.ground_texture_id)


def desenha_sky(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
    _draw("sky", "sky", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, texture_id=state.sky_texture_id, unlit=True)


def desenha_house(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    # Mantido por compatibilidade; a casa usada na cena é desenha_cartoonHouse.
    _draw("cartoonHouse", "cartoonHouse", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, texture_id=state.cartoonHouse_texture_id)


def desenha_fogueira(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("campfire", "campfire", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.campfire_texture_id)


def desenha_planet(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, texture_id, mat_name="lua"):
    # Reaproveita a geometria de esfera ("sky") para luas/planetas. Como essa
    # esfera tem winding invertido (feita p/ ser vista por dentro), o planeta
    # — visto por fora — corta a FACE FRONTAL em vez da traseira.
    _draw("sky", mat_name, angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, texture_id=texture_id, invert_cull=True)


def desenha_sol(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
    # Esfera emissiva amarela representando o sol (fonte de luz externa).
    _draw("sky", "sol", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_color=(1.0, 0.95, 0.6, 1.0), unlit=True)


def desenha_marcador_luz_lantern(pos, color, scale=0.02):
    """Esfera minúscula emissiva (unlit) na posição de uma luz — só p/ depurar.

    Mostra visualmente onde a fonte de luz está no espaço. `pos` e `color`
    são glm.vec3; `scale` controla o tamanho (bem pequeno por padrão).
    """
    _draw("sky", "sol", 0, 0, 0, 0,
          pos.x, pos.y+0.65, pos.z,
          scale, scale, scale,
          base_color=(color.x, color.y, color.z, 1.0), unlit=True)
    

def desenha_marcador_luz_candle(pos, color, scale=0.02):
    """Esferinha da chama da vela. A cor acompanha state.candle_intensity:
    chama fraca -> laranja-vermelho escuro; chama forte -> amarelo brilhante.
    """
    # Normaliza a intensidade atual dentro da faixa do flicker [base-amp, base+amp]
    lo = state.candle_base_intensity - state.candle_flicker_amp
    hi = state.candle_base_intensity + state.candle_flicker_amp
    t = (state.candle_intensity - lo) / (hi - lo) if hi > lo else 1.0
    t = max(0.0, min(1.0, t))

    # Interpola entre brasa (fraca) e chama quente (forte) — variação sutil
    cold = (0.85, 0.45, 0.12)
    hot  = (1.0, 0.62, 0.22)
    r = cold[0] + (hot[0] - cold[0]) * t
    g = cold[1] + (hot[1] - cold[1]) * t
    b = cold[2] + (hot[2] - cold[2]) * t

    _draw("sky", "sol", 0, 0, 0, 0,
          pos.x, pos.y+0.3, pos.z,
          scale, scale, scale,
          base_color=(r, g, b, 1.0), unlit=True)


def desenha_pineTree(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    # Folhas são "cards" planos de face única: precisam ser two-sided (sem
    # culling), senão metade das faces some e a copa fica esburacada.
    _draw("pineTree", "pineTree", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix,
          texture_id=state.pineTree_texture_id, cull=False)


def desenha_rocket(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("rocket", "rocket", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.rocket_texture_id)


def desenha_telescope(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("telescope", "telescope", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.telescope_texture_id)


def desenha_forge(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("forge", "forge", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.forge_texture_id)


def desenha_satelite(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("satelite", "satelite", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.satelite_texture_id)


def desenha_rockTiles(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("rockTiles", "rockTiles", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.rockTiles_texture_id)


def desenha_treeStump(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("treeStump", "treeStump", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.treeStump_texture_id)


def desenha_outerWilds(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("outerWilds", "outerWilds", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.outerWilds_texture_id)


def desenha_wallBox(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("wallBox", "wallBox", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.wallBox_texture_id)


# =========================================================================
# Objetos internos (casa)
# =========================================================================

def desenha_table(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("table", "table", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.table_texture_id)


def desenha_cartoonHouse(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("cartoonHouse", "cartoonHouse", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.cartoonHouse_texture_id)


def desenha_bed(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("bed", "bed", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.bed_texture_id)


def desenha_chair(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("chair", "chair", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.chair_texture_id)


def desenha_shelf(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("shelf", "shelf", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.shelf_texture_id)


def desenha_door(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("door", "door", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.door_texture_id)


def desenha_shelfWall(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("shelfWall", "shelfWall", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.shelfWall_texture_id)


def desenha_foodCan(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("foodCan", "foodCan", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.foodCan_texture_id)


def desenha_barrel(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("barrel", "barrel", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.barrel_texture_id)


def desenha_axe(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("axe", "axe", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.axe_texture_id)


def desenha_apple(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("apple", "apple", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.apple_texture_id)


def desenha_bascket(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("bascket", "bascket", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.bascket_texture_id)


def desenha_gun(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("gun", "gun", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.gun_texture_id)


def desenha_hammer(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("hammer", "hammer", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.hammer_texture_id)


def desenha_jar(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("jar", "jar", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.jar_texture_id)


def desenha_knife(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("knife", "knife", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.knife_texture_id)


def desenha_mug(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("mug", "mug", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.mug_texture_id)


def desenha_pear(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("pear", "pear", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.pear_texture_id)


def desenha_pileOfBooks(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("pileOfBooks", "pileOfBooks", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.pileOfBooks_texture_id)


def desenha_plate(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("plate", "plate", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.plate_texture_id)


def desenha_candle(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("candle", "candle", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.candle_texture_id, unlit=False)


def desenha_globe(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("globe", "globe", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.globe_texture_id)


def desenha_map(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("map", "map", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.map_texture_id)


def desenha_painting(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("painting", "painting", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.painting_texture_id)


def desenha_chandelier(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("chandelier", "chandelier", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.chandelier_texture_id)


def desenha_lantern(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("lantern", "lantern", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.lantern_texture_id)


def desenha_oxygen(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix=None):
    _draw("oxygen", "oxygen", angle, r_x, r_y, r_z, t_x, t_y, t_z,
          s_x, s_y, s_z, base_rotation=planet_rotation_matrix, texture_id=state.oxygen_texture_id)

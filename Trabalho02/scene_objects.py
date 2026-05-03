import glm
import numpy as np
from OpenGL.GL import *
import state


def desenha_caixa(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, texture_id, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)
    
    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    ini = state.objects_dict["caixa"]["ini_index"]
    fim = state.objects_dict["caixa"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_jeep(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.jeep_texture_id)

    ini = state.objects_dict["jeep"]["ini_index"]
    fim = state.objects_dict["jeep"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_snow_terrain(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.snow_texture_id)

    ini = state.objects_dict["snowTerrain"]["ini_index"]
    fim = state.objects_dict["snowTerrain"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)




def desenha_ground(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.ground_texture_id)

    ini = state.objects_dict["ground"]["ini_index"]
    fim = state.objects_dict["ground"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_sky(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.sky_texture_id)

    ini = state.objects_dict["sky"]["ini_index"]
    fim = state.objects_dict["sky"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_house(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.house_texture_id)

    ini = state.objects_dict["house"]["ini_index"]
    fim = state.objects_dict["house"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)


def desenha_fogueira(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.campfire_texture_id)

    ini = state.objects_dict["campfire"]["ini_index"]
    fim = state.objects_dict["campfire"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)


def desenha_planet(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, texture_id):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    ini = state.objects_dict["sky"]["ini_index"]
    fim = state.objects_dict["sky"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_pineTree(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.pineTree_texture_id)

    ini = state.objects_dict["pineTree"]["ini_index"]
    fim = state.objects_dict["pineTree"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_rocket(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.rocket_texture_id)

    ini = state.objects_dict["rocket"]["ini_index"]
    fim = state.objects_dict["rocket"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_table(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.table_texture_id)

    ini = state.objects_dict["table"]["ini_index"]
    fim = state.objects_dict["table"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_cartoonHouse(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.cartoonHouse_texture_id)

    ini = state.objects_dict["cartoonHouse"]["ini_index"]
    fim = state.objects_dict["cartoonHouse"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_telescope(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.telescope_texture_id)

    ini = state.objects_dict["telescope"]["ini_index"]
    fim = state.objects_dict["telescope"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_forge(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.forge_texture_id)

    ini = state.objects_dict["forge"]["ini_index"]
    fim = state.objects_dict["forge"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_satelite(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.satelite_texture_id)

    ini = state.objects_dict["satelite"]["ini_index"]
    fim = state.objects_dict["satelite"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_rockTiles(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.rockTiles_texture_id)

    ini = state.objects_dict["rockTiles"]["ini_index"]
    fim = state.objects_dict["rockTiles"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_treeStump(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.treeStump_texture_id)

    ini = state.objects_dict["treeStump"]["ini_index"]
    fim = state.objects_dict["treeStump"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_outerWilds(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.outerWilds_texture_id)

    ini = state.objects_dict["outerWilds"]["ini_index"]
    fim = state.objects_dict["outerWilds"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_wallBox(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.wallBox_texture_id)

    ini = state.objects_dict["wallBox"]["ini_index"]
    fim = state.objects_dict["wallBox"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_bed(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.bed_texture_id)

    ini = state.objects_dict["bed"]["ini_index"]
    fim = state.objects_dict["bed"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_chair(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.chair_texture_id)

    ini = state.objects_dict["chair"]["ini_index"]
    fim = state.objects_dict["chair"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_shelf(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.shelf_texture_id)

    ini = state.objects_dict["shelf"]["ini_index"]
    fim = state.objects_dict["shelf"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_door(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.door_texture_id)

    ini = state.objects_dict["door"]["ini_index"]
    fim = state.objects_dict["door"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_shelfWall(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.shelfWall_texture_id)

    ini = state.objects_dict["shelfWall"]["ini_index"]
    fim = state.objects_dict["shelfWall"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_foodCan(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.foodCan_texture_id)

    ini = state.objects_dict["foodCan"]["ini_index"]
    fim = state.objects_dict["foodCan"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_barrel(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.barrel_texture_id)

    ini = state.objects_dict["barrel"]["ini_index"]
    fim = state.objects_dict["barrel"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_axe(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.axe_texture_id)

    ini = state.objects_dict["axe"]["ini_index"]
    fim = state.objects_dict["axe"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_apple(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.apple_texture_id)

    ini = state.objects_dict["apple"]["ini_index"]
    fim = state.objects_dict["apple"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_bascket(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.bascket_texture_id)

    ini = state.objects_dict["bascket"]["ini_index"]
    fim = state.objects_dict["bascket"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_gun(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.gun_texture_id)

    ini = state.objects_dict["gun"]["ini_index"]
    fim = state.objects_dict["gun"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_hammer(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.hammer_texture_id)

    ini = state.objects_dict["hammer"]["ini_index"]
    fim = state.objects_dict["hammer"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_jar(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.jar_texture_id)

    ini = state.objects_dict["jar"]["ini_index"]
    fim = state.objects_dict["jar"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_knife(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.knife_texture_id)

    ini = state.objects_dict["knife"]["ini_index"]
    fim = state.objects_dict["knife"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_mug(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.mug_texture_id)

    ini = state.objects_dict["mug"]["ini_index"]
    fim = state.objects_dict["mug"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_pear(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.pear_texture_id)

    ini = state.objects_dict["pear"]["ini_index"]
    fim = state.objects_dict["pear"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_pileOfBooks(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.pileOfBooks_texture_id)

    ini = state.objects_dict["pileOfBooks"]["ini_index"]
    fim = state.objects_dict["pileOfBooks"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

def desenha_plate(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix = None):
    mat_model = state.model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z, planet_rotation_matrix)
    glUniformMatrix4fv(state.loc_model, 1, GL_TRUE, mat_model)

    glUniform1i(state.loc_use_texture, 1)
    glBindTexture(GL_TEXTURE_2D, state.plate_texture_id)

    ini = state.objects_dict["plate"]["ini_index"]
    fim = state.objects_dict["plate"]["end_index"]
    glDrawArrays(GL_TRIANGLES, ini, fim - ini)

import glfw
from OpenGL.GL import *
from shaders.shaders import Shader
from vertices.vertices import *
from matrix_operations import *
from objects.roblox import create_roblox
from objects.pokeball import create_pokeball
from objects.diglett import create_diglett
from objects.healer import create_healer
from objects.eevee import create_eevee 
import state


def draw_scene():


    #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    # while loop --> Lógica de renderização
    while not glfw.window_should_close(state.window):

        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.15, 0.15, 0.2, 1.0)

        pokeball_colors = {}

        pokeball_colors = {}
        pokeball_colors["normal"] = {}
        pokeball_colors["normal"]["upBall"] = [1.0, 0.0, 0.0, 1.0]
        pokeball_colors["normal"]["downBall"] = [1.0, 1.0, 1.0, 1.0]
        pokeball_colors["normal"]["ring"] = [0.0, 0.0, 0.0, 1.0]
        pokeball_colors["normal"]["outerDisk"] = pokeball_colors["normal"]["ring"]
        pokeball_colors["normal"]["innerdisk"] = [1.0, 1.0, 1.0, 1.0]

        pokeball_colors["light"] = {}
        pokeball_colors["light"]["upBall"] = [1.0, 1.0, 1.0, 1.0]
        pokeball_colors["light"]["downBall"] = [1.0, 1.0, 1.0, 1.0]
        pokeball_colors["light"]["ring"] = [1.0, 0.0, 0.0, 1.0]
        pokeball_colors["light"]["outerDisk"] = pokeball_colors["light"]["ring"]
        pokeball_colors["light"]["innerdisk"] = [1.0, 1.0, 1.0, 1.0]


        pokeball_colors["green"] = {}
        pokeball_colors["green"]["upBall"] = [98/255, 211/255, 179/255, 1.0]
        pokeball_colors["green"]["downBall"] = [98/255, 211/255, 179/255, 1.0]
        pokeball_colors["green"]["ring"] = [18/255, 120/255, 122/255, 1.0]
        pokeball_colors["green"]["outerDisk"] = pokeball_colors["green"]["ring"]
        pokeball_colors["green"]["innerdisk"] = [1.0, 1.0, 1.0, 1.0]


        create_eevee()
        #create_roblox()

        angle = state.properties['diglett']['angles']
        position = state.properties['diglett']['position']
        scale = state.properties['diglett']['scale']/10
        create_diglett(angulo=angle, pos=position,scale=scale)

        #OBJETO POKEBOLA:

        pokeballs_pos = {
            "x": [-0.3, 0.08, 0.45],
            "y": [0.07, -0.05, 0.09],
            "z": [0.3, -0.5, 0.1],
        }

        #Pokebola 1
        #create_pokeball(state.loc_color, state.loc_mat_transform, state.objects_dict, -state.angulo+1, pos=[pokeballs_pos["x"][0], pokeballs_pos["y"][0], pokeballs_pos["z"][0]], scale=state.scale, colors_dict=pokeball_colors["normal"])
        #create_diglett(loc_color, loc_mat_transform, objects_dict, -angulo_rotacao_roblox, pos=[0, 0, 0], scale=0.4)

        #Pokebola 2
        #create_pokeball(loc_color, loc_mat_transform, objects_dict, -angulo_rotacao_roblox+3.2, pos=[pokeballs_pos["x"][1], pokeballs_pos["y"][0], pokeballs_pos["z"][0]], scale=0.1, colors_dict=pokeball_colors["light"])
        #create_diglett(loc_color, loc_mat_transform, objects_dict, -angulo_rotacao_roblox, pos=[0.8, 0.8, 0], scale=0.05)

        #Pokebola 3
        #create_pokeball(loc_color, loc_mat_transform, objects_dict, -angulo_rotacao_roblox+0.9, pos=[pokeballs_pos["x"][2], pokeballs_pos["y"][0], pokeballs_pos["z"][0]], scale=0.1, colors_dict=pokeball_colors["green"])
        #create_diglett(loc_color, loc_mat_transform, objects_dict, -angulo_rotacao_roblox, pos=[-0.8, -0.8, 0], scale=0.05)

        #Pokebola 4
        #create_pokeball(loc_color, loc_mat_transform, objects_dict, -angulo_rotacao_roblox+2.2,  pos=[pokeballs_pos["x"][0]-0.15, pokeballs_pos["y"][1], pokeballs_pos["z"][1]], scale=0.1, colors_dict=pokeball_colors["light"])

        #Pokebola 5
        #create_pokeball(loc_color, loc_mat_transform, objects_dict, -angulo_rotacao_roblox+0.2,  pos=[pokeballs_pos["x"][1]-0.15, pokeballs_pos["y"][1], pokeballs_pos["z"][1]], scale=0.1, colors_dict=pokeball_colors["normal"])

        #Pokebola 6
        #create_pokeball(loc_color, loc_mat_transform, objects_dict, -angulo_rotacao_roblox+2.5,  pos=[pokeballs_pos["x"][2]-0.15, pokeballs_pos["y"][1], pokeballs_pos["z"][1]], scale=0.1, colors_dict=pokeball_colors["green"])


        pokeball_positions = [
            [pokeballs_pos["x"][0],       pokeballs_pos["y"][0]+0.006, pokeballs_pos["z"][0]],
            [pokeballs_pos["x"][1],       pokeballs_pos["y"][0]+0.006, pokeballs_pos["z"][0]],
            [pokeballs_pos["x"][2],       pokeballs_pos["y"][0]+0.006, pokeballs_pos["z"][0]],
            [pokeballs_pos["x"][0]-0.15,  pokeballs_pos["y"][1], pokeballs_pos["z"][1]],
            [pokeballs_pos["x"][1]-0.15,  pokeballs_pos["y"][1], pokeballs_pos["z"][1]],
            [pokeballs_pos["x"][2]-0.15,  pokeballs_pos["y"][1], pokeballs_pos["z"][1]],
        ]

        #create_healer(loc_color, loc_mat_transform, objects_dict, 0.15, pos=[0, -0.2, 0], scale=0.3, pokeball_positions=pokeball_positions)

        #OBJETO: Healer
        #create_healer(loc_color, loc_mat_transform, objects_dict, 0.15 , pos=[0, -0.2, 0], scale=0.3)

        glfw.swap_buffers(state.window)
        glfw.poll_events() 

    glfw.terminate()


if __name__ == "__main__":
    draw_scene()

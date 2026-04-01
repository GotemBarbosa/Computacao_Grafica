
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
from objects.scenario import create_scenario
import state


def draw_scene():


    #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    # while loop --> Lógica de renderização
    while not glfw.window_should_close(state.window):

        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glClearColor(0.15, 0.15, 0.2, 1.0)
        glClearColor(0.56, 0.75, 0.87, 1.0)

        pokeball_colors = {
            "normal": {
                "upBall": [1.0, 0.0, 0.0, 1.0],
                "downBall": [1.0, 1.0, 1.0, 1.0],
                "ring": [0.0, 0.0, 0.0, 1.0],
                "outerDisk": [0.0, 0.0, 0.0, 1.0],
                "innerdisk": [1.0, 1.0, 1.0, 1.0],
            },
            "light": {
                "upBall": [1.0, 1.0, 1.0, 1.0],
                "downBall": [1.0, 1.0, 1.0, 1.0],
                "ring": [1.0, 0.0, 0.0, 1.0],
                "outerDisk": [1.0, 0.0, 0.0, 1.0],
                "innerdisk": [1.0, 1.0, 1.0, 1.0],
            },
            "green": {
                "upBall": [98/255, 211/255, 179/255, 1.0],
                "downBall": [98/255, 211/255, 179/255, 1.0],
                "ring": [18/255, 120/255, 122/255, 1.0],
                "outerDisk": [18/255, 120/255, 122/255, 1.0],
                "innerdisk": [1.0, 1.0, 1.0, 1.0],
            },
        }

        pokeballs_pos = {
            "x": [-0.3, 0.08, 0.45],
            "y": [0.07, -0.05],
            "z": [0.3, -0.5],
        }

        pokeball_configs = [
            {"angulo": state.properties["pokeball"]["angle"] + 1.0, "pos": [pokeballs_pos["x"][0], pokeballs_pos["y"][0], pokeballs_pos["z"][0]], "colors": pokeball_colors["normal"]},
            {"angulo": state.properties["pokeball"]["angle"] + 3.2, "pos": [pokeballs_pos["x"][1], pokeballs_pos["y"][0], pokeballs_pos["z"][0]], "colors": pokeball_colors["light"]},
            {"angulo": state.properties["pokeball"]["angle"] + 0.9, "pos": [pokeballs_pos["x"][2], pokeballs_pos["y"][0], pokeballs_pos["z"][0]], "colors": pokeball_colors["green"]},
            {"angulo": state.properties["pokeball"]["angle"] + 2.2, "pos": [pokeballs_pos["x"][0] - 0.15, pokeballs_pos["y"][1], pokeballs_pos["z"][1]], "colors": pokeball_colors["light"]},
            {"angulo": state.properties["pokeball"]["angle"] + 0.2, "pos": [pokeballs_pos["x"][1] - 0.15, pokeballs_pos["y"][1], pokeballs_pos["z"][1]], "colors": pokeball_colors["normal"]},
            {"angulo": state.properties["pokeball"]["angle"] + 2.5, "pos": [pokeballs_pos["x"][2] - 0.15, pokeballs_pos["y"][1], pokeballs_pos["z"][1]], "colors": pokeball_colors["green"]},
        ]

        state.properties["healer"]["pokeball_positions"] = [
            [pokeballs_pos["x"][0], pokeballs_pos["y"][0] + 0.006, pokeballs_pos["z"][0]],
            [pokeballs_pos["x"][1], pokeballs_pos["y"][0] + 0.006, pokeballs_pos["z"][0]],
            [pokeballs_pos["x"][2], pokeballs_pos["y"][0] + 0.006, pokeballs_pos["z"][0]],
            [pokeballs_pos["x"][0] - 0.15, pokeballs_pos["y"][1], pokeballs_pos["z"][1]],
            [pokeballs_pos["x"][1] - 0.15, pokeballs_pos["y"][1], pokeballs_pos["z"][1]],
            [pokeballs_pos["x"][2] - 0.15, pokeballs_pos["y"][1], pokeballs_pos["z"][1]],
        ]

        create_scenario()
        create_eevee()
        create_roblox()
        create_healer()
        state.properties["pokeball"]["angle"] += 0.01

        for index, pokeball_config in enumerate(pokeball_configs):
            create_pokeball(
                angulo=pokeball_config["angulo"],
                pos=pokeball_config["pos"],
                scale=0.1,
                colors_dict=pokeball_config["colors"],
                opening_angle= 45 if index == 3 else 0
            )

        

        glfw.swap_buffers(state.window)
        glfw.poll_events() 

    glfw.terminate()


if __name__ == "__main__":
    draw_scene()


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

        
        #create_eevee()
        #create_roblox()

        angle = state.properties['diglett']['angles']
        position = state.properties['diglett']['position']
        scale = state.properties['diglett']['scale']/10
        #create_diglett(angulo=angle, pos=position,scale=scale)

        #OBJETO POKEBOLA:
        state.properties["pokeball"]["angle"] += 0.01
        create_pokeball(opening_angle=45)

        #create_healer(loc_color, loc_mat_transform, objects_dict, 0.15, pos=[0, -0.2, 0], scale=0.3, pokeball_positions=pokeball_positions)

        #OBJETO: Healer
        create_healer()

        glfw.swap_buffers(state.window)
        glfw.poll_events() 

    glfw.terminate()


if __name__ == "__main__":
    draw_scene()

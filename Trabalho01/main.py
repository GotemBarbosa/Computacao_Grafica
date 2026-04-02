
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


    rot_angle = 0
    #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    # while loop --> Lógica de renderização
    while not glfw.window_should_close(state.window):

        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glClearColor(0.15, 0.15, 0.2, 1.0)
        glClearColor(0.56, 0.75, 0.87, 1.0)

        rot_angle += 1.5
        rr = [15.0, 20.0, -10.0, 10.0, -15.0, 12.0]


        s_angles = state.scene_angles
        s_scale = state.scene_scale

        healer_scale = s_scale/4
        pokeball_scale = s_scale/8
        eevee_scale = s_scale*0.8
        roblox_scale = s_scale*1.5
        diglett_scale = s_scale*0.2

        create_scenario()

        create_roblox(pos=[0.2, -0.15, +0.5],
                      angulos=[s_angles[0]-15, s_angles[1]+70, s_angles[2]],
                      scale=roblox_scale)
        
        create_eevee(pos=[-0.7, -0.5, -0.4],
                     angulos=[s_angles[0]-15, s_angles[1]-20, s_angles[2]], 
                     scale=eevee_scale)
        

        diglett_height = 3.5 * diglett_scale  # altura total: do disco até o topo da cabeça
        diglett_offset = max(-diglett_height, min(diglett_height, state.diglett_y_offset))
        create_diglett(pos=[0.6, -0.7 + diglett_offset, 0.0],
                    angulos=[s_angles[0]-15, s_angles[1]+50, s_angles[2]],
                    scale=diglett_scale)
        

        '''
         create_healer() devolve as posições que cada pokebola deve ser posicionada em cima dele. 
         São 6 posições retornada, cada uma com seus valores x,y,z.
             --> pokeball_positions = [pos1, pos2, pos3, pos4, pos5, pos6]
             --> pos_n = [x, y, z]
        '''
        pokeball_positions = create_healer(angulo=[s_angles[0]-15, s_angles[1]-110, s_angles[2]], 
                                           pos=[-0.2, -0.3, 0.3],
                                           scale=healer_scale)




        '''
        ===========================
        POKEBOLAS EM CIMA DO HEALER
        ===========================
        '''
        colors = ["light", "green", "normal", "green", "light", "normal"]
        create_pokeball(angulos=[s_angles[0]+rr[5], s_angles[1], s_angles[2]],
                        pos=[pokeball_positions[5][0], pokeball_positions[5][1], pokeball_positions[5][2]],
                        open=True,
                        opening_angle=state.pokeball_opening_angle,
                        color_name=colors[5], 
                        scale=pokeball_scale,
                        rotation_angle=rot_angle)

        for i in range(5):
            create_pokeball(angulos=[s_angles[0]+rr[i], s_angles[1], s_angles[2]], 
                            pos=[pokeball_positions[i][0], pokeball_positions[i][1], pokeball_positions[i][2]], 
                            open=False, 
                            opening_angle=0, 
                            color_name=colors[i], 
                            scale=pokeball_scale,
                            rotation_angle=rot_angle)
            

        '''
        ===========================
        POKEBOLAS DENTRO DA POKEBOLA
        ===========================
        '''
        pokemon_scale = pokeball_scale * 0.8  # Nova escala do pokemon

        create_eevee(
        pos=[
            pokeball_positions[5][0],
            pokeball_positions[5][1],  # desce para ficar na metade inferior
            pokeball_positions[5][2]
        ],
        angulos=[s_angles[0] + rr[5], s_angles[1] + rot_angle, s_angles[2]],
        scale=pokemon_scale
)
        
        glfw.swap_buffers(state.window)
        glfw.poll_events() 

    glfw.terminate()


if __name__ == "__main__":
    draw_scene()

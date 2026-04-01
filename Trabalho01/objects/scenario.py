from matrix_operations import *
from .utils import *
import state


def create_scenario():
    scenario = state.properties["scenario"]

    ground = {
        "scale": scenario["ground"]["scale"],
        "angle_after_moving": [
            scenario["x_angle"],
            scenario["y_angle"],
            scenario["z_angle"],
        ],
        "final_translation": scenario["position"],
    }

    ground_color = [scenario["ground"]["color"] for _ in range(6)]
    draw_cube(final_matrix(ground), ground_color)

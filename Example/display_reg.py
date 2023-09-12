import matplotlib.pyplot as plt
from Simulations.Math.config import *
from Example.kinematics import kinematics
from ipywidgets import *

plt.rcParams["figure.dpi"] = 150

k = kinematics(
    RIGHT_FRONT,
    RIGHT_BACK,
    LEFT_FRONT,
    LEFT_BACK,
)

def update(roll, pitch, yaw, x, y, z, rot_x, rot_y, rot_z):
    k.plot_robot(
        xyz=[[x, y, z], [x, y, z], [x, y, z], [x, y, z]],
        rot=[roll, pitch, yaw],
        is_radians=False,
        center_offset=[rot_x, rot_y, rot_z],
    )

    # plot the robot with the sliders for adjusting the rotation and center_offset
interact(
    update,
    roll=widgets.FloatSlider(value=0, min=-20, max=20, step=1),
    pitch=widgets.FloatSlider(value=0, min=-20, max=20, step=1),
    yaw=widgets.FloatSlider(value=0, min=-20, max=20, step=1),
    x=widgets.FloatSlider(value=0, min=-0.10, max=0.10, step=0.01),
    y=widgets.FloatSlider(value=0, min=-0.10, max=0.10, step=0.01),
    z=widgets.FloatSlider(value=-0.15, min=-0.25, max=-0.10, step=0.01),
    rot_x=widgets.FloatSlider(value=0, min=-0.25205 / 2, max=0.25205 / 2, step=0.01),
    rot_y=widgets.FloatSlider(value=0, min=-0.105577 / 2, max=0.105577 / 2, step=0.01),
    rot_z=widgets.FloatSlider(value=0, min=-0.25, max=0.25, step=0.01),
)

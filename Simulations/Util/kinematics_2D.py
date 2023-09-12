import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as la
from util import *
from config import config

# class kinematics_2D:
    # def __init__(self):
    #     self.target = np.array([5,0])
    #     self.base = np.array([5,5])
    #     self.diff_vector = None

    #     self.top_limb = config.top_limb_length
    #     self.bottom_limb = config.bottom_limb_length

    #     self.current_pos = self.inverse_kinmatics(self.target)
        # self.update_coord()

def forward_kinematics(top_limb, bottom_limb, theta_1, delta_1):
    joint_1 = [0, 0]
    joint_2 = polar_to_cartesian(top_limb, theta_1)
    joint_3 = determine_pos(joint_2, delta_1, bottom_limb)
    return np.array([
        joint_1,
        joint_2,
        joint_3
    ]) 
    
def inverse_kinmatics(target, base, top_limb, bottom_limb):
    diff_vector = np.subtract(target, base)
    diff_angle = cartesian_to_polar(diff_vector)
    abs_length_m = abs(top_limb - bottom_limb)
    total_limb_length = top_limb + bottom_limb
    dist = la.norm(diff_vector)
    max_distance = max(abs_length_m, min(total_limb_length, dist))

    E_x = round(math.cos(diff_angle) * max_distance, 2)
    E_y = round(math.sin(diff_angle) * max_distance, 2)
    m = E_x ** 2 + E_y ** 2

    top_limb_sq = top_limb ** 2
    bottom_limb_sq = bottom_limb ** 2

    try:
        theta_1 = (math.acos((top_limb_sq - bottom_limb_sq + m) / (2 * top_limb * math.sqrt(m))) + diff_angle)
    except:
        print("This is not physically possible")
        return
    theta_2 = math.acos((top_limb_sq + bottom_limb_sq - m)/ (2 * top_limb * bottom_limb))

    j_2x = math.cos(theta_1) * top_limb + base[0]
    j_2y = math.sin(theta_1) * top_limb + base[1]
    j_3x = j_2x + (math.cos(math.pi-(-theta_2-theta_1)) * bottom_limb)
    j_3y = j_2y + (math.sin(math.pi-(2*math.pi - theta_2 - theta_1)) * bottom_limb)

    joint_2 = [j_2x, j_2y]
    joint_3 = [j_3x, j_3y]
    return np.array([base, joint_2, joint_3])

# def update_coord(self):
#     self.joint_posx, self.joint_posy = coordinates_to_list(self.current_pos[0], self.current_pos[1], self.current_pos[2])


# def get_current_target(self):
#     return self.target

# def get_pos(self):
#     return self.joint_posx, self.joint_posy

    
# def plot_leg(self):
#     plt.clf()
#     plt.grid(color='purple', linestyle='-', linewidth=1)
#     plt.plot(self.joint_posx, self.joint_posy, color='red')
#     plt.show()


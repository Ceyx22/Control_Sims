import math
from numpy.linalg import norm
import numpy as np

def coordinates_to_list(joint_1, joint_2, joint_3):
    x_pos = [joint_1[0], joint_2[0], joint_3[0]]
    y_pos = [joint_1[1], joint_2[1], joint_3[1]]
    return (x_pos, y_pos)

def get_joint_pos(x_pos, y_pos, joint_num):
    return (x_pos[joint_num], y_pos[joint_num])

def distance_formula(joint_pos1, joint_pos2):
    (x1, y1) = (joint_pos1[0], joint_pos1[1])
    (x2, y2) = (joint_pos2[0], joint_pos2[1])
    return math.sqrt((x2 - x1)**2 + (y2-y1)**2)

def normalize_vector(vector):
    distance = norm(vector)
    return np.divide(vector, distance)

#returns in radians
def cartesian_to_polar(joint_pos):
    #rad = 
    # if rad < 0:
    #     degrees = degrees + 360
    return np.arctan2(joint_pos[1], joint_pos[0])

def polar_to_cartesian(r, theta):
    x = r * np.cos( np.deg2rad(theta) )
    y = r * np.sin(np.deg2rad(theta))
    return np.array([x,y])

def determine_pos(start, theta, length):
    x = start[0]
    y = start[1]
    x2 = x + length * np.cos(np.deg2rad(theta))
    y2 = y + length * np.sin(np.deg2rad(theta))
    return [x2, y2]

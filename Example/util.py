from math import atan, pi, radians, cos, sin
import numpy as np


# converts 2D cartesian points to polar angles in range 0 - 2pi
def point_to_rad(start, end):
    if start > 0 and end >= 0:
        return atan(end / (start))
    elif start == 0 and end >= 0:
        return pi / 2
    elif start < 0 and end >= 0:
        return -abs(atan(end / start)) + pi
    elif start < 0 and end < 0:
        return atan(end / start) + pi
    elif start > 0 and end < 0:
        return -abs(atan(end / start)) + 2 * pi
    elif start == 0 and end < 0:
        return pi * 3 / 2
    elif start == 0 and end == 0:
        return pi * 3 / 2  # edge case


def RotMatrix3D(rotation=[0, 0, 0], is_radians=True, order="xyz"):
    roll, pitch, yaw = rotation[0], rotation[1], rotation[2]

    # convert to radians is the input is in degrees
    if not is_radians:
        roll = radians(roll)
        pitch = radians(pitch)
        yaw = radians(yaw)

    # rotation matrix about each axis
    # [1, 0, 0]
    # [0, cos(roll), -sin(roll)]
    # [0, sin(roll), cos(roll)]
    rotX = np.matrix([[1, 0, 0], [0, cos(roll), -sin(roll)], [0, sin(roll), cos(roll)]])
    # [cos(pitch), 0, sin(pitch)]
    # [0, 1, 0]
    # [-sin(pitch), 0, cos(pitch)]
    rotY = np.matrix(
        [[cos(pitch), 0, sin(pitch)], [0, 1, 0], [-sin(pitch), 0, cos(pitch)]]
    )
    # [cos(yaw), -sin(yaw), 0]
    # [sin(yaw), cos(yaw), 0]
    # [0, 0, 1]
    rotZ = np.matrix([[cos(yaw), -sin(yaw), 0], [sin(yaw), cos(yaw), 0], [0, 0, 1]])

    # rotation matrix order (default: pitch -> roll -> yaw)
    if order == "xyz":
        rotationMatrix = rotZ * rotY * rotX
    elif order == "xzy":
        rotationMatrix = rotY * rotZ * rotX
    elif order == "yxz":
        rotationMatrix = rotZ * rotX * rotY
    elif order == "yzx":
        rotationMatrix = rotX * rotZ * rotY
    elif order == "zxy":
        rotationMatrix = rotY * rotX * rotZ
    elif order == "zyx":
        rotationMatrix = rotX * rotY * rotZ

    return rotationMatrix  # roll pitch and yaw rotation

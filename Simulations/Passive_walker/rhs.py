from constants import walker
import numpy as np
import math 

def rhs(t,z):
    theta_1 = z[0]
    omega1 = z[1]
    theta_2 = z[2]
    omega2 = z[3]

    I = walker.I
    m = walker.m
    M = walker.M
    c = walker.c
    l = walker.l
    gravity = walker.gravity
    gamma = walker.gamma
    A11 = 2.0*I + M*l**2 + m*(c - l)**2 + m*(c**2 - 2*c*l*math.cos(theta_2) + l**2)
    A12 = 1.0*I + c*m*(c - l*math.cos(theta_2))
    A21 = 1.0*I + c*m*(c - l*math.cos(theta_2))
    A22 = 1.0*I + c**2*m
    A_ss = np.array([[A11, A12], [A21, A22]])
    
    b1 = -1.0*M*gravity*l*math.sin(gamma - theta_1) + 1.0*c*gravity*m*math.sin(gamma - theta_1) - 1.0*c*gravity*m*math.sin(-gamma + theta_1 + theta_2) - 2.0*c*l*m*omega1*omega2*math.sin(theta_2) - 1.0*c*l*m*omega2**2*math.sin(theta_2) - 2.0*gravity*l*m*math.sin(gamma - theta_1)
    b2 = 1.0*c*m*(-gravity*math.sin(-gamma + theta_1 + theta_2) + l*omega1**2*math.sin(theta_2))
    b_ss = np.array([[b1], [b2]])

    alpha = np.linalg.lstsq(A_ss, b_ss, rcond=None)[0]

    theta1ddot = alpha[0][0]
    theta2ddot = alpha[1][0]
    return np.array([omega1, theta1ddot, omega2, theta2ddot])
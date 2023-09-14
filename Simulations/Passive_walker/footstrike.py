from constants import walker
import numpy as np
import math

def foot_strike(zminus):

    theta1_n = zminus[0]; 
    omega1_n = zminus[1];
    theta2_n = zminus[2]; 
    omega2_n = zminus[3];
    

    I = walker.I;
    m = walker.m;
    M = walker.M;
    c = walker.c;
    l = walker.l;

    J11 = 1
    J12 = 0
    J13 = l*(math.cos(theta1_n + theta2_n)- math.cos(theta1_n))
    J14 = l*math.cos(theta1_n + theta2_n)
    J21 = 0
    J22 = 1
    J23 = l*(-math.sin(theta1_n) + math.sin(theta1_n + theta2_n))
    J24 = l*math.sin(theta1_n + theta2_n)
    J = np.array([[J11, J12, J13, J14], [J21, J22, J23, J24]])
    
    A11 = 1.0*M + 2.0*m
    A12 = 0
    A13 = -1.0*M*l*math.cos(theta1_n) + 1.0*m*(c - l)*math.cos(theta1_n) + m*(c*math.cos(theta1_n + theta2_n) - l*math.cos(theta1_n))
    A14 = 1.0*c*m*math.cos(theta1_n + theta2_n)
    A21 = 0
    A22 = 1.0*M + 2.0*m
    A23 = -1.0*M*l*math.sin(theta1_n) + 1.0*m*(c - l)*math.sin(theta1_n) + m*(c*math.sin(theta1_n + theta2_n) - l*math.sin(theta1_n))
    A24 = 1.0*c*m*math.sin(theta1_n + theta2_n)
    A31 = -1.0*M*l*math.cos(theta1_n) + 1.0*m*(c - l)*math.cos(theta1_n) + m*(c*math.cos(theta1_n + theta2_n) - l*math.cos(theta1_n))
    A32 = -1.0*M*l*math.sin(theta1_n) + 1.0*m*(c - l)*math.sin(theta1_n) + m*(c*math.sin(theta1_n + theta2_n) - l*math.sin(theta1_n))
    A33 = 2.0*I + M*l**2 + m*(c - l)**2 + m*(c**2 - 2*c*l*math.cos(theta2_n) + l**2)
    A34 = 1.0*I + c*m*(c - l*math.cos(theta2_n))
    A41 = 1.0*c*m*math.cos(theta1_n + theta2_n)
    A42 = 1.0*c*m*math.sin(theta1_n + theta2_n)
    A43 = 1.0*I + c*m*(c - l*math.cos(theta2_n))
    A44 = 1.0*I + c**2*m
    A_n_hs = np.array([[A11, A12, A13, A14], [A21, A22, A23, A24], [A31, A32, A33, A34], [A41, A42, A43, A44]])
    

    X_n_hs = np.array([[0], [0], [omega1_n], [omega2_n]])
    b_hs = np.append(np.matmul(A_n_hs,X_n_hs), [[0], [0]], axis=0)
    temp = np.append(A_n_hs, np.transpose(-J), axis=1)
    temp2 = np.append(J, [[0, 0], [0, 0]], axis=1)
    A_hs = np.append(temp, temp2, axis=0)
    X_hs = np.linalg.lstsq(A_hs, b_hs, rcond=None)[0]
    omega = np.array([X_hs[2]+ X_hs[3], -X_hs[3]])
    theta1 = theta1_n + theta2_n
    theta2 = -theta2_n

    return np.array([theta1, omega[0][0], theta2, omega[1][0]]);
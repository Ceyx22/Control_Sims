import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from scipy.integrate import RK45
from rhs import rhs
from footstrike import foot_strike
from SimUtil import to_CSV
from constants import walker
import numpy as np
import math
from decimal import *


def contact(t, z):
    theta1 = z[1];
    theta2 = z[3];
    val = theta2 + 2*theta1
    if theta1 > -0.1:
        isTerminal = False; #continue
    else:
        isTerminal = True; #stop integration
    
    return [val, isTerminal]

def formatData(t, y):
    sub = []
    sub.append(t)
    for i in range(len(y)):
        sub.append(y[i])
    return sub


def custom_ode(func, t0, z0, dt, event):
    simulator = RK45(func, t0, z0, dt, atol=1e-13, rtol=1e-13)
    t = simulator.t
    full_val = []
    stop = False
    while stop == False:
        simulator.step() 
        t = simulator.t
        sub = formatData(t, simulator.y)
        val, isTerminal = event(t, sub)
        if val <= 0:
            if isTerminal:
                stop = True
        elif t >= dt:
            stop = True
        if stop is not True:
            full_val.append(sub)
    return full_val

def one_step(t0, z0, num):
    dt = 8
    data = custom_ode(rhs, t0, z0, dt, contact)
    to_CSV("CSV/PassiveWalkerData.csv", data, ["Time", "theta1", "theta1dot", "theta2", "theta2dot"])
    zminus = data[-1][1:] # gets last element and does not include time
    if num == 1:
        return foot_strike(zminus)
    else:
        return data
    

def fixedpt(z):
    t0 = 0
    zplus = one_step(t0,z, 1)
    return z-zplus
    #trying to set F = 0 

# to Test stability
def partialder(func,z):
    pert = 0.00001 #1e-5
    n = len(z)
    # J = np.zeros((n,n))

    ### Using central difference, accuracy quadratic ###
    J = []
    for i in range(n):
        ztemp1=z 
        ztemp2=z
        # print(ztemp1[i])
        # print(ztemp1[i]+ pert)
        # print((ztemp1[i]+ pert) - ztemp1[i])
        ztemp1[i]= ztemp1[i]+ pert 
        ztemp2[i]= ztemp2[i]-pert 
        # 0 is for t0
        temp3 = func(0, ztemp1, 1)
        temp4 = func(0, ztemp2, 1)
        print(temp3)
        print(temp4)
        new = []
        for i in range(len(temp3)):
            new.append(Decimal(temp3[i])-Decimal(temp4[i]))
        #print(new)
        J.append(func(0, ztemp1, 1) - func(0, ztemp2, 1))
    # print(J)
    #return J/(2*pert)

def seperateData(data):
    # data is list of lists
    # [time, theta1, theta1dot, theta2, theta2dot]
    time = []
    x_h = []
    y_h = []
    theta1 = []
    theta1dot = []
    theta2 = []
    theta2dot = []
    for lis in data:
        time.append(lis[0])
        x_h.append(walker.l*math.sin(lis[1]))
        y_h.append(walker.l*math.cos(lis[1]))
        theta1.append(lis[1])
        theta1dot.append(lis[2])
        theta2.append(lis[3])
        theta2dot.append(lis[4])
    
    angles = [theta1, theta1dot, theta2, theta2dot, x_h, y_h]
    return time, angles



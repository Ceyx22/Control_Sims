import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from scipy.integrate import RK45
from rhs import rhs
from footstrike import foot_strike
from SimUtil import to_CSV
import numpy as np


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

def one_step(t0, z0):
    dt = 8
    data = custom_ode(rhs, t0, z0, dt, contact)
    # to_CSV("CSV/PassiveWalkerData.csv", data, ["Time", "theta1", "theta1dot", "theta2", "theta2dot"])
    zminus = data[-1][1:] # gets last element and does not include time
    return foot_strike(zminus)
    

def fixedpt(z):
    t0 = 0
    zplus = one_step(t0,z)
    return z-zplus
    #trying to set F = 0 

def partialder(func,z,walker):
    pert=1e-5
    n = len(z)
    J = np.zeros(n,n)
    #### Using forward difference, accuracy linear ####
    # y0=feval(func,z,walker) 
    # # zTemp
    # for i in range(n)
    #     ztemp=z
    #     ztemp[i]=ztemp[i]+pert 
    #     J(:,i)=(feval(FUN,0,ztemp,walker)-y0) 
    # end
    # J=(J/pert)

    ### Using central difference, accuracy quadratic ###
    # for i in range(n):
    #     ztemp1=z 
    #     ztemp2=z
    #     ztemp1[i]=ztemp1[i]+pert 
    #     ztemp2[i]=ztemp2[i]-pert 
    #     # 0 is for t0
    #     J[:,i]=(feval(func,0,ztemp1,walker)-feval(func,0,ztemp2,walker)) 

    return J/(2*pert)

    
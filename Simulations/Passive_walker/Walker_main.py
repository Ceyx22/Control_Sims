import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from helper import fixedpt, one_step, seperateData, partialder
import numpy as np
from scipy.optimize import least_squares, root
from animate import animate
from SimUtil import create_fig


######## Init Guess #######
theta1 = 0.18 
theta1dot = -0.25
theta2 = -2*theta1 
theta2dot = 0.1
z0 = np.array([theta1, theta1dot, theta2, theta2dot])

######## root finding #######
#t = [0.162605640661018,  -0.231877363279977,  -0.325211281332871,   0.037983418653201]
# usage of this does not work properly because of tolerance control
sol = least_squares(fixedpt, z0, ftol=1e-12, xtol=1e-12) 
zstar = sol.x
partialder(one_step, zstar)
######## Data #######
t0 = 0
data = one_step(t0,z0, 2)
time, z_all = seperateData(data)
animate(time, z_all)
create_fig(time, z_all[0], 2, "Radians", "Time", "images/AnglesOfLegs.png", case="passive walker", y2axis=z_all[2])


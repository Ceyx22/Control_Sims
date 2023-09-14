from helper import fixedpt, one_step
import numpy as np
from scipy.optimize import fsolve, root, minimize, show_options, least_squares





# ####### root finding #######
# options = optimoptions('fsolve','Display','iter','TolFun',1e-12)
# [zstar,fval,exitflag] = fsolve(@(x) fixedpt(x,walker),z0,options)
# exitflag
# zstar
# fval
theta1 = 0.18 
theta1dot = -0.25
theta2 = -2*theta1 
theta2dot = 0.1
z0 = np.array([theta1, theta1dot, theta2, theta2dot])
#t = [0.162605640661018,  -0.231877363279977,  -0.325211281332871,   0.037983418653201]
#print(z0)
#sol = root(fixedpt, x0=z0, method='lm', options={'ftol':1e-12, 'xtol':1e-12})
# sol = least_squares(fixedpt, z0, ftol=1e-12, xtol=1e-12)
#sol = minimize(fixedpt, z0, method='l-bfgs-b',options={'ftol': 1e-12, 'disp': True})
# print(sol)
t0 = 0
step = one_step(t0,z0);

#print(show_options(solver="root", method='lm'))

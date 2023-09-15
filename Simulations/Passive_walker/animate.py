import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from constants import walker
import numpy as np
from scipy.interpolate import interp1d
import math

######## Animation #######
def animate(time, z_all):
    tstart = time[0]
    tend = time[-1]
    t_inter = np.linspace(start=tstart, stop=tend, num=round(walker.ani_fps*(tend - tstart)))
    z_inter = []
    
    for i in range(len(z_all)):
        f = interp1d(time, z_all[i])
        z_inter.append(f(t_inter))

    theta1 = z_inter[0] 
    theta2 = z_inter[2] 
    xh = z_inter[4]
    yh = z_inter[5]
    fig, ax = plt.subplots()
    ax.set_xlim(-1, 2)
    ax.set_ylim(-0.1, 1.5)
    ax.axhline(y=0, color='blue', linestyle='-')
    def anim(i):
        ax.cla()
        ax.axhline(y=0, color='blue', linestyle='-')
        x_C1 = xh[i] + walker.l*math.sin(theta1[i]);
        y_C1 = yh[i] - walker.l*math.cos(theta1[i]);
        x_C2 = xh[i] + walker.l*math.sin(theta1[i]+theta2[i]);
        y_C2 = yh[i] - walker.l*math.cos(theta1[i]+theta2[i]);
        ax.plot([xh[i], x_C1], [yh[i], y_C1], color="blue")
        ax.plot([xh[i], x_C2], [yh[i], y_C2], color="red")

    
    ani = FuncAnimation(fig, anim, frames=len(t_inter), interval=60)
    ani.save('images/passive_walker.mp4', writer = 'ffmpeg', fps = 30)

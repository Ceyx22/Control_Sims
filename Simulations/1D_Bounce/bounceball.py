import numpy as np
import pandas as pd
from Simulations.SimUtil import to_CSV, create_fig
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp
import csv


gravity = 9.8
# coefficient of resistance
ball_e = 0.9
ground = 0

y0 = 0
y0dot = 10
t0 = 0
t_end = 10
t_start = 0
eval = [0.0013, 0.0025,0.0038,0.005, 0.0114,0.0177, 0.024,0.0303, 0.0618, 0.0934,0.1249,0.1565,0.2815,0.4065,0.5315,0.6565,0.7815,0.9065, 1.0315,1.1565,1.2815,1.4065,1.5315,1.6565,1.7526,1.8486,1.9447,2.0408 ] #
time = []
position = []
velocity = []
data = [[1, 0, 0, 10]]

def contact(t, y):
    return y[0] - ground

contact.terminal = True
contact.direction = -1

def model(t, y):
    ydot = y[1]
    yddot = -gravity
    return [ydot, yddot]

def one_bounce(t0, ystart, lineNum):
    
    true_range = []
    for i in range(len(eval)):
        true_range.append(eval[i] + t0)
    dt = 5
    sol = solve_ivp(model, [t0, t0+dt], ystart, dense_output=False, events=contact, rtol=1e-6, atol=1e-6, t_eval=true_range )
    for i in range(len(sol.y[0])):
        if i != 0:
            lineNum = lineNum + 1
            data.append([lineNum, sol.t[i], sol.y[0][i], sol.y[1][i]])
            if i == (len(sol.y[0]) -1):
                data.append([lineNum, sol.t_events[0][0], round(sol.y_events[0][0][0], 3), -ball_e*round(sol.y_events[0][0][1], 3)])
                


def seperateData(formatted_data):
    for item in formatted_data:
        time.append(item[1])
        position.append(item[2])
        velocity.append(item[3])

start = [y0, y0dot]
line_num = 1
while t0 < t_end:
    one_bounce(t0, start, line_num)
    t0 = data[-1][1]
    start = [data[-1][2], data[-1][3]]
    line_num = data[-1][0]


to_CSV("CSV/Bounce_Ball_Data.csv", data, ["Line Number", "Time", "Position", "Velocity"])
seperateData(data)
create_fig(time, position, 1, "Position", "Time", "images/Position.png" )
create_fig(time, velocity, 2, "Velocity", "Time", "images/Velocity.png" )

fig, ax = plt.subplots()
ln, = ax.plot([], [], 'ro')
ax.axhline(y=-0.175, color='blue', linestyle='-')

def init():
    ax.set_xlim(0, 10)
    ax.set_ylim(-1, 10)
    return ln,

def update(frame):
    ln.set_data([5], [data[frame][2]])
    return ln,

ani = FuncAnimation(fig, update, frames=len(data),
                    init_func=init, blit=True, interval = 30)
plt.show()
   
ani.save('images/bouncingBall.mp4', 
          writer = 'ffmpeg', fps = 30)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp


gravity = 9.8
# coefficient of resistance
ball_e = 0.9
ground = 0

y0 = 0
y0dot = 10
y_start = [y0, y0dot]

t0 = 0
t_end = 20
t_start = 0

t_all = t_start
y_all = y_start
eval = [0.0013, 0.0025,0.0038,0.005, 0.0114,0.0177, 0.024,0.0303, 0.0618, 0.0934,0.1249,0.1565,0.2815,0.4065,0.5315,0.6565,0.7815,0.9065, 1.0315,1.1565,1.2815,1.4065,1.5315,1.6565,1.7526,1.8486,1.9447,2.0408 ] #
print(len(eval))
t_full = []
y0_full = []
y0dot_full = []

def contact(t, y):
    return y[0] - ground

contact.terminal = True
contact.direction = -1

real_data = []
def model(t, y):
    ydot = y[1]
    yddot = -gravity
    return [ydot, yddot]

def one_bounce(t0, ystart):
    true_range = []
    for i in range(len(eval)):
        true_range.append(eval[i] + t0)
    dt = 5
    sol = solve_ivp(model, [t0, t0+dt], ystart, dense_output=False, events=contact, rtol=1e-6, atol=1e-6, t_eval=true_range)
    # coefficient of restitutiuon
    #print(sol)
    for i in range(len(sol.y[0])):
        y0_full.append(sol.y[0][i])
        if i == len(sol.y[0]) - 1:
            y0dot_full.append(-ball_e*sol.y[1][i])
        else:
            y0dot_full.append(sol.y[1][i])
    #y0_full.append(sol.y[0][:])
    #y0_full.append(round(sol.y[0][-1], 5))
    # print(-ball_e*sol.y[1][-1])
    t_full.extend(sol.t[:])
    #print(len(t_full))
    #print(f"Index of time: {t_full[0]}")

while t0 < t_end:
    one_bounce(t0, y_start)
    t0 = t_full[-1]
    y_start = [y0_full[-1], y0dot_full[-1]]


print(len(y0dot_full))
print(f"Time: {t_full}")
print(f"y0 full: {y0_full}")
print(f"y0dot full: {y0dot_full}")
#print(real_data)




# plt.plot(5, y0_full[0])
# plt.xlabel("time")
# plt.ylabel("y(t)")
# plt.show()
fig, ax = plt.subplots()
xdata, ydata = [], []
ln = ax.plot([], [], 'ro')

def init():
    ax.set_xlim(0, 10)
    ax.set_ylim(-1, 10)
    return ln,

def update(frame):
    ln.set_data([5], y0_full[frame])
    return ln,

ani = FuncAnimation(fig, update, frames=len(t_full),
                    init_func=init, blit=True, interval = 30)
plt.show()
   
ani.save('bouncingBall.mp4', 
          writer = 'ffmpeg', fps = 30)
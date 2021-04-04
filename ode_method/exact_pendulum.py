#!/usr/bin/env python
# coding: utf-8

# Simple pendulum simulation

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation
# from IPython.display import HTML
# get_ipython().run_line_magic('matplotlib', 'nbagg')
# get_ipython().run_line_magic('matplotlib', 'inline')

grav = 9.81
longest_pendulum = 9.81
time = 55
number_pendulums = 5

# The solution to the original differential equaiton can be
# obtained this way:


def solution(g, l, t, init_angle, init_velocity):

    # The model function is the differential equation
    # corresponding to this problem
    def model(u, t):
        return (u[1], - (g / l) * np.sin(u[0] * np.pi / 180))

    # Initial angle, and initial angular velocity
    theta0 = [init_angle, init_velocity]

    # Desired time interval
    time_steps = np.arange(0, time, 0.1)

    # Solution per time-step
    solution = odeint(model, theta0, time_steps)

    return solution[:, 0]


def positions(g, l, t, init_angle, init_velocity, n_pendulums):
    data = []

    for i in range(1, n_pendulums + 1):
        data.append(solution(g, l * i / n_pendulums,
                             t, init_angle, init_velocity))

    data = np.array(data)
    x_temp = np.sin(data * np.pi / 180)
    y_temp = - np.cos(data * np.pi / 180)

    for i in range(0, n_pendulums):
        x_temp[i] = (l * (i + 1) / n_pendulums) * x_temp[i]
        y_temp[i] = (l * (i + 1) / n_pendulums) * y_temp[i]

    return x_temp, y_temp


x, y = positions(grav,
                 longest_pendulum,
                 time,
                 -17.5,
                 0,
                 number_pendulums)

print(len(x[0]))

x_min = x[-1].min()
x_max = x[-1].max()
y_min = y[-1].min()

# Now, this part generates the animation of the pendulum!
fig, ax = plt.subplots()
ax = plt.axes(xlim=(x_min - 0.5, x_max + 0.5),
              ylim=(y_min - 0.5, 0))

points = []

# Original answer for my question
# for j, (col, mar) in enumerate(zip(["green", "blue", "red"], ["o", "x", "s"])):
#     newpoint, = ax.plot(x_temp[j][0], y_temp[j][0], color=col, marker=mar)
#     points.append(newpoint)

# Adapting the answer for my needs
markers_list = ['o' for i in range(number_pendulums)]
color_list = ['green' for i in range(number_pendulums)]

for j, (col, mar) in enumerate(zip(color_list, markers_list)):
    newpoint, = ax.plot(x[j][0], y[j][0], color=col, marker=mar)
    points.append(newpoint)

# This is the function I was having problems with


def animation_frames(i):
    for j in range(0, number_pendulums):
        points[j].set_data(x[j][i], y[j][i])

    point, = ax.plot([], [], 'go', lw=3)


# Creating and saving the animaiton in a gif on the
# notebook's path
animation = FuncAnimation(fig, animation_frames,
                          frames=len(x[-1]), interval=30)
animation.save('simple_pendulum.gif', writer='imagemagick')

# plt.close()
plt.show()

# Finaly! It was a little complicated to do the visualization.
# I was in the right path with the animation function.
# I had to ask, though.

# HTML(animation.to_html5_video())
# HTML(animation.to_jshtml())

# Note: the commented lines depend on wether the usr is in
# a jupyter notebook or not. Uncomment them if so.

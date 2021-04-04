#!/usr/bin/env python
# coding: utf-8

# Pendulum simulation with the Newton's approach to solve
# the differential equation.
# Some changes were done because I was using Atom with
# the hydrogen extension (jupyter-like interface).

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

gravity = 9.81
length = 9.81
theta0 = -5.0
omega0 = 0
time = 100
dt = 0.001
total_bobs = 15

ghosting = 'False'


def newton_method(init_theta, init_omega, time, dt, g, l):
    iterations = np.int(time / dt)

    # time_temp = np.linspace(0, time, iterations)

    theta = np.zeros(iterations)
    omega = np.zeros(iterations)

    theta[0] = init_theta * np.pi / 180
    omega[0] = init_omega

    for i in range(iterations - 1):

        theta[i + 1] = theta[i] + omega[i] * dt
        omega[i + 1] = omega[i] - (g / l) * np.sin(theta[i]) * dt

    return theta

# Function to automatically generate the positions of the bobs
# dividing the maximum length between the number of bobs.
# Can not see awsome patterns!


def positions(init_theta, init_omega, time, dt, g, l, bobs):
    angle_data = []

    for i in range(1, bobs + 1):
        angle_data.append(newton_method(init_theta,
                                        init_omega,
                                        time,
                                        dt,
                                        g,
                                        l * i / bobs))

    x_data = np.sin(angle_data)
    y_data = - np.cos(angle_data)

    for i in range(0, bobs):
        x_data[i] = (l * (i + 1) / bobs) * x_data[i]
        y_data[i] = (l * (i + 1) / bobs) * y_data[i]

    return x_data, y_data, angle_data

# The key to the patterns is to minimize the length difference
# between bobs.


def postions_new(init_theta, init_omega, time, dt, g, l, dl, bobs):
    angle_data = []

    for i in range(bobs):
        angle_data.append(newton_method(
            init_theta, init_omega, time, dt, g, l - dl * i))

    x_data = np.sin(angle_data)
    y_data = - np.cos(angle_data)

    for i in range(bobs):
        x_data[i] = (l - dl * i) * x_data[i]
        y_data[i] = (l - dl * i) * y_data[i]

    return x_data, y_data, angle_data


# (x, y, angle) = positions(theta0,
#                           omega0,
#                           time,
#                           dt,
#                           gravity,
#                           length,
#                           total_bobs)

x, y, angle = postions_new(theta0, omega0,
                           time, dt,
                           gravity, length,
                           0.5, total_bobs)

# For animation purposes it is not important to draw ALL
# the bobs' positions. If not, the animations becomes slugish.

nth_element = 100

x = [x[i][::nth_element] for i in range(len(x))]
y = [y[i][::nth_element] for i in range(len(y))]

x_min = x[0].min()
x_max = x[0].max()
y_min = y[0].min()


# Creating the figure
fig, ax = plt.subplots()
ax = plt.axes(xlim=(x_min - 0.5, x_max + 0.5),
              ylim=(y_min - 0.5, 0))
plt.axis('off')

points = []

markers_list = ['D' for i in range(total_bobs)]
color_list = ['purple' for i in range(total_bobs)]

# Assigning markers and colors
for j, (col, mar) in enumerate(zip(color_list, markers_list)):
    newpoint, = ax.plot(
        x[j][0], y[j][0],
        linestyle='None',
        color=col,
        marker=mar,
        markerfacecolor='None')
    points.append(newpoint)

# This is the function I was having problems with


def animation_frames(i):
    # Ghosting shows a trace for every bob
    if ghosting == 'True':
        for j in range(0, total_bobs):
            points[j].set_data(x[j][i:i+total_bobs],
                               y[j][i:i+total_bobs])
    else:
        for j in range(0, total_bobs):
            points[j].set_data(x[j][i],
                               y[j][i])

    point, = ax.plot([], [])


# Creating and saving the animaiton in a gif on the script's
# directory
animation = FuncAnimation(fig, animation_frames,
                          frames=len(x[-1]), interval=45)
animation.save('newton_pendulum.gif', writer='imagemagick')

# plt.close()

plt.show()

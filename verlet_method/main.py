# blank line

import numpy as np
import matplotlib.pyplot as plt

time = 5
dt = 0.01
theta0 = -17.5
omega0 = 0
g = 9.81
l = 9.81

# iterations = np.int(time / dt)
# time_list = np.linspace(0, time, iterations)

# angle_n+2 = angle_n+1 - angle_n - (g / l) * dt * sin(angle_n+1)


def verlet_method(init_theta, init_omega, time, dt, g, l):

    iterations = np.int(time / dt)
    # time_list = np.linspace(0, time, iterations)

    theta = np.zeros(iterations)
    theta[0] = init_theta * np.pi / 180

    theta[1] = theta[0] + dt * init_omega + \
        (dt**2 / 2) * (g / l) * np.sin(theta[0])

    for i in range(len(theta)-2):
        theta[i+2] = 2 * theta[i+1] - theta[i] - \
            (g / l) * dt**2 * np.sin(theta[i+1])

    return theta

 # theta = verlet_method(theta0, omega0, time, dt, g, l)


def positions(init_theta, init_omega, time, dt, g, l, dl, bobs):
    angle_data = []

    for i in range(1, bobs+1):
        angle_data.append(verlet_method(
            init_theta, init_omega, time, dt, g, l - dl * i))

    x_data = np.sin(angle_data)
    y_data = - np.cos(angle_data)

    for i in range(bobs):
        x_data[i] = (l - dl * i) * x_data[i]
        y_data[i] = (l - dl * i) * y_data[i]

    return x_data, y_data


x, y = positions(theta0, omega0, time, dt, g, l, 0.2, 3)

# Nice trick with list comprehension...! Maybe it is slower than
# a simple for-loop, though.
[plt.plot(x[i], y[i], '.') for i in range(len(x))]
plt.show()

# Would it be a good idea to change the for loops to
# list comprehension ?

# list = [1, 2, 3, 4, 5]

# new = [list[i] * (l - dt * i) for i in range(3)]

# print(new)

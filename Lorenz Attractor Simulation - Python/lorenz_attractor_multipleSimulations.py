# -------  Importing Libraries ------- #

import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation

from scipy.integrate import odeint

# -------  Defining the Constants of the system ------- #

n_simulations = 100
random_start = 1000 # the range across which we want to generate the starting point of our simulation

sigma = 10
beta = 8/3
rho = 28

# -------  Function for solving the System Numerically ------- #

def system_of_odes(vector, t, sigma, beta, rho):
    x, y, z = vector

    d_vector = [
        sigma*(y - x),
        x*(rho - z) - y,
        x*y - beta*z
    ]
    return d_vector 


def get_solutions():
    x_sols = []
    y_sols = []
    z_sols = []

    lorenz_plots = []

    for i in range(n_simulations):

        init_position = random_start*np.random.rand(3)

        # Solving for the system
        positions = odeint(system_of_odes, init_position, time_points, args=(sigma, beta, rho))
        x_sol, y_sol, z_sol = positions[:, 0], positions[:, 1], positions[:, 2]
        lorenz_plt, = ax.plot(x_sol, y_sol, z_sol, color='black')

        x_sols.append(x_sol)
        y_sols.append(y_sol)
        z_sols.append(z_sol)

        lorenz_plots.append(lorenz_plt)

    return x_sols, y_sols, z_sols, lorenz_plots


time_points = np.linspace(0, 40, 3001) # Creating our vector of time points

# -------  Setting the plots ------- #

fig, ax = plt.subplots(subplot_kw={'projection':'3d'})
ax.set_title(f"Having {n_simulations} simulations, choosing x, y, z randomly between [0, {random_start})")

# -------  Solving the System Numerically ------- #

x_sols, y_sols, z_sols, lorenz_plots = get_solutions()


# -------  Animating the solutions ------- #

def update(frame):

    lower_lim = max(0, frame - 100)

    for i in range(n_simulations):
        # Displaying only 100 elements of our solution array, that automatically updates with `frame` for each solution
        x_current_1 = x_sols[i][lower_lim:frame+1]
        y_current_1 = y_sols[i][lower_lim:frame+1]
        z_current_1 = z_sols[i][lower_lim:frame+1]

        lorenz_plots[i].set_data(x_current_1, y_current_1)
        lorenz_plots[i].set_3d_properties(z_current_1)

    ax.view_init(elev=10., azim=0.5*frame) 

    return lorenz_plots

animation = FuncAnimation(fig, update, frames=len(time_points), interval=25, blit=False)
plt.show()
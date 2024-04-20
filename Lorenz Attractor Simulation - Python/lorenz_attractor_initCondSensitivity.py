# -------  Importing Libraries ------- #

import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation

from scipy.integrate import odeint

# -------  Defining the Constants of the system ------- #

N_time_points = 2001

sigma = 10
beta = 8/3
rho = 28

# -------  Solving the System Numerically ------- #

def system_of_odes(vector, t, sigma, beta, rho):
    x, y, z = vector

    d_vector = [
        sigma*(y - x),
        x*(rho - z) - y,
        x*y - beta*z
    ]

    return d_vector 


position_0_1 = [0.0, 1.0, 1.0] # Represents the 1st position at t = 0
position_0_2 = [0.0, 1 + 1.1, 1.0] # Represents the 2nd position at t = 0

time_points = np.linspace(0, 40, N_time_points) # Creating our vector of time points

# Solving for the 1st system
positions_1 = odeint(system_of_odes, position_0_1, time_points, args=(sigma, beta, rho))
x_sol_1, y_sol_1, z_sol_1 = positions_1[:, 0], positions_1[:, 1], positions_1[:, 2]

# Solving for the 2nd system
positions_2 = odeint(system_of_odes, position_0_2, time_points, args=(sigma, beta, rho))
x_sol_2, y_sol_2, z_sol_2 = positions_2[:, 0], positions_2[:, 1], positions_2[:, 2]

# -------  Plotting the solutions ------- #

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection':'3d'})

lorenz_plt_1, = ax.plot(x_sol_1, y_sol_1, z_sol_1, 'red', label=f'Position 0 of 1st: {position_0_1}')
lorenz_plt_2, = ax.plot(x_sol_2, y_sol_2, z_sol_2, 'blue',label=f'Position 0 of 2nd: {position_0_2}')

plt.legend()

# -------  Animating the solutions ------- #

def update(frame):

    # Displaying only 100 elements of our solution array, that automatically updates with `frame`
    lower_lim = max(0, frame - 100)

    x_current_1 = x_sol_1[lower_lim:frame+1]
    y_current_1 = y_sol_1[lower_lim:frame+1]
    z_current_1 = z_sol_1[lower_lim:frame+1]

    x_current_2 = x_sol_2[lower_lim:frame+1]
    y_current_2 = y_sol_2[lower_lim:frame+1]
    z_current_2 = z_sol_2[lower_lim:frame+1]


    # Updating the plot with our new data
    lorenz_plt_1.set_data(x_current_1, y_current_1)
    lorenz_plt_1.set_3d_properties(z_current_1) 


    lorenz_plt_2.set_data(x_current_2, y_current_2)
    lorenz_plt_2.set_3d_properties(z_current_2)  

    #ax.view_init(elev=10., azim=0.5*frame) 

    # Update the title
    ax.set_title(f'time: {40*frame/N_time_points:.2f} [unit of time]')

    return lorenz_plt_1, lorenz_plt_2

# Running the simulation
animation = FuncAnimation(fig, update, frames=len(time_points), interval=25, blit=False)
plt.show()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from scipy import linalg, interpolate, io

#Write explaination and equations for the utility function defined
#by consumption and lesisure in Romer. 

def u(C, L): #Defining the utility function
    if theta == 1.0:
        consumption = np.log(C)
    else:
        consumption = (C**(1-theta)-1/(1-theta))

    if omega == 1.0:
        leisure = np.log(1-L)
    else:
        leisure = ((1-L)**(1-omega)-1/(1-omega))

    #Flow utility is defined as:
    utility = consumption + b*leisure

    return utility

b, omega, theta = 2.0, 1.0, 1.0 #set some parameter values

u(np.exp(1),0) #Checking if the function is working properly. If result is 1, it works.

#We will now plot the utility function we just found defined, in a 3-dimensional plot:

#create the plot
fig = plt.figure(figsize=(10,10))

#create the axis
ax = fig.gca(projection="3d", elev=30, azim=310)

#Create grid of values for consumption and leisure:
Consumption = np.linspace(0,20,200)
Leisure = np.linspace(0,2,20)
L, C = np.meshgrid(Leisure, Consumption) #Make N-D coordinate arrays for vectorized evaluations of N-D scalar/vector fields over N-D grids, given one-dimensional coordinate arrays.

#We choose arbitrary parameter values:
b, omega, theta = 5.0, 1.0, 1.0 

#We define the utility function: 
utility = u(C,L)

#We define the surface:
utility_surface = ax.plot_surface(L, C, utility, rstride = 1, cstride = 1, 
                                  cmap = mpl.cm.terrain, linewidth = 0, vmin=-10, 
                                  vmax = np.max(utility), antialiased=False)

#We will now fix axis, labels, colors, legedens, etc:
ax.set_xlim(0, 1)
ax.set_ylim(0, 10)
ax.set_xlabel(r'Labor, $L_{t}$', fontsize=15, family='serif')
ax.set_ylabel(r'Consumption, $C_{t}$', fontsize=15, family='serif')
ax.set_title(r'$u(C,\ L)$ for $b=%.2f, \theta=%.2f, \omega=%.2f$' %(b, theta, omega), 
             fontsize=20, family='serif')
fig.colorbar(utility_surface, shrink=0.75, aspect=10)

#Display
plt.show()
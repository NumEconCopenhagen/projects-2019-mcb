import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from scipy import linalg, interpolate, io

#Write explaination and equations for the utility function defined
#by consumption and lesisure in Romer. 

#Theta is the coefficient describing an individuals relative risk aversion. This is greater than 1.
#Delta is the inverse intertemporal elasticity of substitution between current and future leisure.
#b is a parameter determinding the importanance for leisure for the individuals. 

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

u(np.exp(1),0) #Checking if the function is working properly. If result is 1, it works!

#We will now plot the utility function we just found defined, in a 3-dimensional plot:

#create the plot
fig = plt.figure(figsize=(8,6))

# create a 3D Axes object
ax = fig.gca(projection='3d', elev=30, azim=310)

# create a grid of (x,y) values which we will pass to function
consumption = np.linspace(0, 10, 200)
labor = np.linspace(0, 1, 20)
L, C = np.meshgrid(labor, consumption)

# Choose parameter values
b, theta, omega = 5.0, 1.0, 1.0

# we will actually plot output
utility = u(C, L)

# note the use of the new plot command!
utility_surface = ax.plot_surface(L, C, utility, rstride=1, cstride=1, cmap="YlGnBu", 
                                  linewidth=0, vmin=-10, vmax=np.max(utility), 
                                  antialiased=False)

# axes, labels, title, colorbar etc.
ax.set_xlim(0, 1)
ax.set_ylim(0, 10)
ax.set_xlabel(r'Labor, $L_{t}$', fontsize=15, family='serif')
ax.set_ylabel(r'Consumption, $C_{t}$', fontsize=15, family='serif')
ax.set_title(r'$u(C,\ L)$ for $b=%.2f, \theta=%.2f, \omega=%.2f$' %(b, theta, omega), 
             fontsize=20, family='serif')
fig.colorbar(utility_surface, shrink=0.75, aspect=10)

# display the plot!
plt.show()

#We will now look at the effects of the parameters, by locking consumption and leisure
L_lock, C_lock = 0.5, 1.0

fig, axes = plt.subplots(1, 2, sharey=True, figsize=(15,10)) #We make the two plots share the same y-axis
ax1, ax2 = axes

for b in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
    #Here we lock leisure, and plot consumption and a set leisure level while varying b
    ax1.plot(consumption, u(consumption, L_lock), label = "b=%g" %b) 

    #Axes, labels, etc
    ax1.set_xlabel("Consumption, $C_t$", family="serif")
    ax1.set_ylabel(r"u$(C_t, \bar{L})$", rotation = "vertical")
    ax1.set_title("Slicing through $u(C_{t}, L_{t})$ at $L_{t}=%.2f$" %L_lock, family="serif")

    #Next we do the same, but hold consumption locked. 
    ax2.plot(labor, u(C_lock, labor), label = "b=%g" %b)

    #Axes, labels, etc
    ax2.set_xlabel("Labor, $L_t$", family="serif")
    ax2.set_title("Slicing through $u(C_{t}, L_{t})$ at $L_{t}=%.2f$" %L_lock, family = "serif")

ax2.legend(loc=0, frameon=False, prop={'family':'serif'})

plt.tight_layout()
plt.suptitle('Slicing for various b', y=1.05, fontsize=20, family='serif')
plt.show()

#The results show, the more an individual values leisure (the greater b is), the less utility the indivual has 
#for a given level of consumption. Furthermore, the marginal utility of for an extra unit of labor is much more negative
#for a higher b. 

#We can do the same analysis for theta (risk-aversion): 
# fix l_bar and c_bar
L_lock, C_lock = 0.5, 1

# create a new figure object!
fig, axes = plt.subplots(1, 2, sharey=True, figsize=(12,6))
ax1, ax2 = axes

for theta in [0.5, 1.0, 1.5, 2.0]:
    
    # first subplot will fix l at some constant l_bar and plot u(C, l_bar)
    ax1.plot(consumption, u(consumption, L_lock), label=r'$\theta=%g$' %theta)

    # axes, labels, title. legend, etc
    ax1.set_xlabel('Consumption, $C_{t}$', family='serif')
    ax1.set_ylabel(r'$u(C_{t}, \bar{L})$', rotation='vertical')
    ax1.set_title('A slice through $u(C_{t}, L_{t})$ at $L_{t}=%.2f$' %L_lock,
                  family='serif')

    # first subplot will fix l at some constant l_bar and plot u(C, l_bar)
    ax2.plot(labor, u(C_lock, labor), label=r'$\theta=%g$' %theta)

    # axes, labels, title. legend, etc
    ax2.set_xlabel('Labor, $L_{t}$', family='serif')
    ax2.set_title('A slice through $u(C_{t}, L_{t})$ at $C_{t}=%.2f$' %C_lock,
                  family='serif')
    
ax2.legend(loc=0, frameon=False, prop={'family':'serif'})

# tighten things up and add a title
plt.tight_layout()
plt.suptitle(r'Utility slices for various $\theta$', y=1.05, fontsize=20, family='serif') 

plt.show()

#For theta we have chosen to only include 0-2 because exceeding 2.0 messes with the y-axis

#And for omega

# fix l_lock and c_lock
L_lock, C_lock = 0.5, 1

# create a new figure object!
fig, axes = plt.subplots(1, 2, sharey=True, figsize=(12,6))
ax1, ax2 = axes

for omega in [0.5, 1.0, 1.5, 2.0]:
    
    # first subplot will fix l at some constant l_bar and plot u(C, l_bar)
    ax1.plot(consumption, u(consumption, L_lock), label=r'$\omega=%g$' %omega)

    # axes, labels, title. legend, etc
    ax1.set_xlabel('Consumption, $C_{t}$', family='serif')
    ax1.set_ylabel(r'$u(C_{t}, \bar{L})$', rotation='vertical')
    ax1.set_title('A slice through $u(C_{t}, L_{t})$ at $L_{t}=%.2f$' %L_lock,
                  family='serif')

    ax2.plot(labor, u(C_lock, labor), label=r'$\omega=%g$' %omega)

    # axes, labels, title. legend, etc
    ax2.set_xlabel('Labor, $L_{t}$', family='serif')
    ax2.set_title('A slice through $u(C_{t}, L_{t})$ at $C_{t}=%.2f$' %C_lock,
                  family='serif')
    
ax2.legend(loc=0, frameon=False, prop={'family':'serif'})

# tighten things up and add a title
plt.tight_layout()
plt.suptitle(r'Utility slices for various $\omega$', y=1.05, fontsize=20, family='serif') 

plt.show()

#Looking at the trade-off between leisure and consumption. 

fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(111)

# Force logarithmic preferences!
b, theta, omega = 2.0, 0.5, 0.5 #arbitrarily chosen. 

# we will actually plot output
utility = u(C, L) #we plot the function from earlier 

# create the contour plot
im = ax.imshow(utility, interpolation='gaussian', origin='lower', cmap=mpl.cm.terrain, 
               vmin=-10, vmax=np.max(utility), extent=(0, 1, 0, 10), aspect=0.10)

# demarcate the contours...
CS = ax.contour(L, C, utility, np.linspace(-8, np.max(utility), 10), colors=np.repeat('k', 10), 
                linewidths=1, linestyles='solid')
ax.clabel(CS, inline=1, fmt='%1.2f')

# axes, labels, title, colorbar etc.
ax.set_xlim(0, 1)
ax.set_ylim(0, 10)
ax.set_xlabel(r'Labor, $L_{t}$', fontsize=15, family='serif')
ax.set_ylabel(r'Consumption, $C_{t}$', fontsize=15, family='serif')
ax.set_title(r'$u(C,\ L)$ for $b=%.2f, \theta=%.2f, \omega=%.2f$' %(b, theta, omega), 
             fontsize=20, family='serif')
fig.colorbar(utility_surface, shrink=0.75, aspect=10)

plt.show()

#2. PERIOD MODEL - Explain the model in the notebook.
# We choose arbitrary parameter values. 
b, beta, theta, omega = 2.0, 0.50, 1.0, 1.0
 
# Specify some arbitrary prices which the household will take as given. 
W0, W1, r1 = 5, 5, 0.025

# Calculate endowment given prices.
endowment = W0 + (1 / (1 + r1)) * W1

print("Labor endowment is:", endowment)

# is the non-negativity constraint on l0 satisfied by your chosen prices?
(1 / (1 + r1)) * (W1 / W0) < ((((1 + b) * (1 + beta)) / b) - 1) #result is true - Constraint is satisfied. 

#Define the two matrixes derived from the model
A = np.array([[b, 0, W0, 0], 
              [beta * (1 + r1), -1, 0, 0], 
              [0, b, 0, W1], 
              [1, 1 / (1 + r1), -W0, -(1 / (1 + r1)) * W1]])

d = np.array([[W0], 
              [0], 
              [W1], 
              [0]])

# Solve the system of equations and assign the optimal choices for consumption and labor
C_0 = linalg.solve(A, d)[0,0]
C_1 = linalg.solve(A, d)[1,0] 
L_0 = linalg.solve(A, d)[2,0]
L_1 = linalg.solve(A, d)[3,0]
u_0 = u(C_star0, L_star0)
u_1 = u(C_star1, L_star1)

print("Optimal C in period 0,1:", (C_0, C_1)) 
print("Optimal l in period 0,1:", (L_0, L_1)) 
print("Flow in period 0,1:   ", (u_0, u_1))

print("Optimal C, t=0:", (1 / ((1 + b) * (1 + beta))) * (W0 + (1 / (1 + r1)) * W1))
print("Optimal C, t=1:", ((1 + r1) / (1 + b)) * (beta / (1 + beta)) * (W0 + (1 / (1 + r1)) * W1))
print("Optimal L, t=0:", 1 - (b / W0) * (1 /((1 + b) * (1 + beta))) * (W0 + (1 / (1 + r1)) * W1))
print("Optimal L, t=1:", 1 - ((b * beta * (1 + r1)) / W1) * (1 /((1 + b) * (1 + beta))) * (W0 + (1 / (1 + r1)) * W1))
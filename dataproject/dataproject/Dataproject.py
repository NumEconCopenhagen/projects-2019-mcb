# Run this shit mah niggas in your terminal (no #)
# Source: https://pypi.org/project/IneqPy/
# git clone https://github.com/mmngreco/IneqPy.git
# cd IneqPy
# pip install .

# Docstring
""" Hello and welcome to my Minecraft video. Remember to like, subscribe and smash that bell button!"""

# Importing packages
import pandas as pd
import numpy as np
import ineqpy
import matplotlib.pyplot as plt

# ensure your arr is sorted from lowest to highest values first!
arr = np.array([1,4,6,9,100])

def gini(arr):
    count = arr.size
    coefficient = 2 / count
    indexes = np.arange(1, count + 1)
    weighted_sum = (indexes * arr).sum()
    total = arr.sum()
    constant = (count + 1) / count
    return coefficient * weighted_sum / total - constant

def lorenz(arr):
    # this divides the prefix sum by the total sum
    # this ensures all the values are between 0 and 1.0
    scaled_prefix_sum = arr.cumsum() / arr.sum()
    # this prepends the 0 value (because 0% of all people have 0% of all wealth)
    return np.insert(scaled_prefix_sum, 0, 0)

# show the gini index!
print(gini(arr))

lorenz_curve = lorenz(arr)

# we need the X values to be between 0.0 to 1.0
plt.plot(np.linspace(0.0, 1.0, lorenz_curve.size), lorenz_curve)
# plot the straight line perfect equality curve
plt.plot([0,1], [0,1])

plt.show()
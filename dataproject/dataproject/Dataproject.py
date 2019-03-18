
# DOCSTRING:
"""
Group: NVF696, RXW556, MFQ992
Source: https://pypi.org/project/IneqPy/
Run the following code in your terminal
to install the requires IneqPy package: 
git clone https://github.com/mmngreco/IneqPy.git
cd IneqPy
pip install .
""" 

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
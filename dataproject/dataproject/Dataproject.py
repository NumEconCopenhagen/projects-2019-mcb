# DOCSTRING:
"""
Group: NVF696, RXW556, MFQ992
Source: https://pypi.org/project/IneqPy/
Run the following code in your terminal
to install the requires IneqPy package: 
git clone https://github.com/mmngreco/IneqPy.git
cd IneqPy
pip install .
pip install git+https://github.com/elben10/pydst
"""
# Importing packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ineqpy
import pydst
import ipywidgets as widgets

# Defining the Gini-coefficient
def G(v):
    bins = np.linspace(0., 100., 11)
    total = float(np.sum(v))
    yvals = []
    for b in bins:
        bin_vals = v[v <= np.percentile(v, b)]
        bin_fraction = (np.sum(bin_vals) / total) * 100.0
        yvals.append(bin_fraction)
    # perfect equality area
    pe_area = np.trapz(bins, x=bins)
    # lorenz area
    lorenz_area = np.trapz(yvals, x=bins)
    gini_val = (pe_area - lorenz_area) / float(pe_area)
    return bins, yvals, gini_val



# Fetching data from Denmarks Statistic's
Dst = pydst.Dst(lang='da')
#Dst.get_data(table_id = "INDKP109")

#indkp_vars
#indkp_vars["values"]
indkp_vars = Dst.get_data(table_id="INDKP109", variables={"REGLAND":["000"], "TID":["2015"], "ENHED":["*"], "KOEN":["*"], "ALDER1":["*"], "HERKOMST":["*"]})


# Fetching data list
# x = np.random.rand(500)
#v = np.log(indkp_vars[['INDHOLD'], ['TID'=2015]]) #.values
#v = indkp_vars['INDHOLD']
v = np.log(indkp_vars['INDHOLD']) #.values
vx = (indkp_vars['INDHOLD']) #.values

print(vx)
print(vx.max()) #oh shit


# Plotting figure
bins, result, gini_val = G(v)
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(bins, result, label="observed")
plt.plot(bins, bins, '--', label="perfect equality")
plt.xlabel("fraction of population")
plt.ylabel("fraction of wealth")
plt.title("GINI: %.4f" %(gini_val))
plt.legend()
plt.subplot(2, 1, 2)
plt.hist(v, bins=20)

def interactive_lorenz("REGLAND", "TID", "ENHED", "KOEN", "ALDER1", "HERKOMST")
    
    
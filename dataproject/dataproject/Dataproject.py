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
import numpy as np
import ineqpy
import pydst

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

Dst = pydst.Dst(lang='da')
Dst.get_data(table_id = "INDKP109")

indkp_vars = Dst.get_variables(table_id="INDKP109") 
indkp_vars

indkp_vars["values"]



v = np.random.rand(500)
bins, result, gini_val = G(v)
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(bins, result, label="observed")
plt.plot(bins, bins, '--', label="perfect eq.")
plt.xlabel("fraction of population")
plt.ylabel("fraction of wealth")
plt.title("GINI: %.4f" %(gini_val))
plt.legend()
plt.subplot(2, 1, 2)
plt.hist(v, bins=20)


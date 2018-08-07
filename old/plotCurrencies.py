# Libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import kde

from database.dbGet import *

ncols=3
nrows=3
# Create a figure with plot areas
fig, axes = plt.subplots(ncols=ncols, nrows=nrows)

def plot(ncol, nrow, axes, currency, nbins):
    data = DbGet().getCompanyToPlotSVM(currency)

    prof_total = []
    rate = []

    for j in range(0, len(data)):
        rate.append( data [j][0])
        prof_total.append(data [j][1])

    # 2D Histogram
    axes[ncol, nrow].set_title(currency)
    counts, xedges, yedges, im = axes[ncol, nrow].hist2d(rate, prof_total, bins=nbins, cmap=LinearSegmentedColormap.from_list("custom_colors",[(1,1,1),(1,0,0)],N=nbins))
    axes[ncol, nrow].set_xlim(50,100)
    axes[ncol, nrow].set_ylim(99,108)
    plt.colorbar(im, ax=axes[ncol, nrow])


# Plot
currencies = ["USD", "JPY", "EUR", "CAD", "AUD", "HKD", "INR", "GBX", "CNY"]
nbins = [105, 71, 95, 95, 90, 75, 75, 90, 40]

k=0
for j in range(nrows):
    for i in range(ncols):
        plot(i, j, axes, currencies[k], nbins[k])
        k+=1

plt.subplots_adjust(left=0.05, right=0.98, bottom=0.04, top=0.95, wspace=0.13, hspace=0.27)
plt.show()

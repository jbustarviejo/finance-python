# Libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import kde

from database.dbGet import *

ncols=5
nrows=2
# Create a figure with plot areas
fig, axes = plt.subplots(ncols=ncols, nrows=nrows)

def plot(ncol, nrow, axes, sector, nbins):
    data = DbGet().getCompanyToPlotSector(sector)

    prof_total = []
    rate = []

    for j in range(0, len(data)):
        rate.append( data [j][0])
        prof_total.append(data [j][1])

    # 2D Histogram
    axes[ncol, nrow].set_title(sector)
    counts, xedges, yedges, im = axes[ncol, nrow].hist2d(rate, prof_total, bins=nbins, cmap=LinearSegmentedColormap.from_list("custom_colors",[(1,1,1),(1,0,0)],N=nbins))
    axes[ncol, nrow].set_xlim(50,100)
    axes[ncol, nrow].set_ylim(99,108)
    plt.colorbar(im, ax=axes[ncol, nrow])


# Plot
sectors = ["Financials", "Industrials", "Basic Materials", "Consumer Goods", "Consumer Services", "Technology", "Health Care", "Oil & Gas", "Utilities", "Telecommunications"]
nbins = [100, 100, 100, 95, 100, 105, 90, 90, 80, 55]

k=0
for j in range(nrows):
    for i in range(ncols):
        plot(j, i, axes, sectors[k], nbins[k])
        k+=1

plt.subplots_adjust(left=0.03, right=0.99, bottom=0.03, top=0.965, wspace=0.32)
plt.show()

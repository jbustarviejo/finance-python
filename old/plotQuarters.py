# Libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import kde

from database.dbGet import *

ncols=5
nrows=3
# Create a figure with plot areas
fig, axes = plt.subplots(ncols=ncols, nrows=nrows)

def plot(ncol, nrow, axes, sector, label, nbins):
    data = DbGet().getCompanyToPlotQ(sector)

    prof_total = []
    rate = []

    for j in range(0, len(data)):
        rate.append( data [j][0])
        prof_total.append(data [j][1])

    # 2D Histogram
    axes[ncol, nrow].set_title(label)
    counts, xedges, yedges, im = axes[ncol, nrow].hist2d(rate, prof_total, bins=nbins, cmap=LinearSegmentedColormap.from_list("custom_colors",[(1,1,1),(1,0,0)],N=nbins))
    axes[ncol, nrow].set_xlim(50,100)
    axes[ncol, nrow].set_ylim(99,108)
    plt.colorbar(im, ax=axes[ncol, nrow])


# Plot
sectors = ["2017-07-01", "2017-04-01", "2017-01-01", "2016-10-01", "2016-07-01", "2016-04-01", "2016-01-01", "2015-10-01", "2015-07-01", "2015-04-01", "2015-01-01", "2014-10-01", "2014-07-01", "2014-04-01", "2014-01-01"]
labels = ["2017Q3", "2017Q2", "2017Q1", "2016Q4", "2016Q3", "2016Q2", "2016Q1", "2015Q4", "2015Q3", "2015Q2", "2015Q1", "2014Q4", "2014Q3", "2014Q2", "2014Q1"]
nbins = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]

k=0
for j in range(nrows):
    for i in range(ncols):
        plot(j, i, axes, sectors[k], labels[k], nbins[k])
        k+=1

plt.subplots_adjust(left=0.03, right=0.98, bottom=0.03, top=0.965, wspace=0.32, hspace=0.25)
plt.show()

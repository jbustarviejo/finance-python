# Libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import kde
from matplotlib.colors import ListedColormap

from database.dbGet import *

def plot(axes, nbins):
    data = DbGet().getCompaniesToPlotDiff()
    plot_data(axes, nbins, data, LinearSegmentedColormap('BlueRed1', {
        'red':     ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'green': ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0))
        }))

def plot_data(axes, nbins, data, cmap):
    prof_total = []
    rate = []

    for j in range(0, len(data)):
        rate.append( data [j][0])
        prof_total.append(data [j][1])

    # Get the colormap colors
    my_cmap = cmap(np.arange(cmap.N))
    # Set alpha
    my_cmap[:,-1] = np.linspace(0, 1, cmap.N)
    # Create new colormap
    my_cmap = ListedColormap(my_cmap)

    # 2D Histogram
    counts, xedges, yedges, im = axes.hist2d(rate, prof_total, bins=nbins, cmap=my_cmap)
    axes.set_xlim(50, 100)
    axes.set_ylim(-200, 300)
    plt.colorbar(im, ax=axes)

ncols=1
nrows=1

# Create a figure with plot areas
fig, axes = plt.subplots(ncols=ncols, nrows=nrows)

# Plot
plot(axes, [115,1500000])

plt.subplots_adjust(left=0.03, right=0.97, bottom=0.04, top=0.91, wspace=0.32)
# plt.show()
fig = plt.gcf()
DPI = fig.get_dpi()
fig.set_size_inches(1536.0/float(DPI),768.0/float(DPI))
plt.savefig("imgs/alldiff.png")

# Libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import kde
from matplotlib.colors import ListedColormap

from database.dbGet import *

def plot(ncol, nrow, axes, sector, nbins):
    data = DbGet().getCompanyToPlotCurrencyDiff(sector)
    plot_data(ncol, nrow, axes, sector, nbins[0], data, LinearSegmentedColormap('BlueRed1', {
        'red':     ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'green': ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0))
        }))

def plot_data(ncol, nrow, axes, sector, nbins, data, cmap):
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
    axes[ncol, nrow].set_title(sector)
    counts, xedges, yedges, im = axes[ncol, nrow].hist2d(rate, prof_total, bins=nbins, cmap=my_cmap)
    axes[ncol, nrow].set_xlim(50, 100)
    axes[ncol, nrow].set_ylim(-200, 300)
    plt.colorbar(im, ax=axes[ncol, nrow])

ncols=3
nrows=3


# Create a figure with plot areas
fig, axes = plt.subplots(ncols=ncols, nrows=nrows)

# Plot
currencies = ["USD", "JPY", "EUR", "CAD", "AUD", "HKD", "INR", "GBX", "CNY"]
nbins = [
    [[120,300000]], #USD
    [[70,8000]], #JPY
    [[80,20000]], #EUR
    [[80,20000]], #CAD
    [[80,10000]], #AUD
    [[70,50000]], #HKD
    [[80,8000]], #INR
    [[50,600]], #GBX
    [[50,1000]], #CNY
    ]

k=0
for j in range(nrows):
    for i in range(ncols):
        plot(j, i, axes, currencies[k], nbins[k])
        k+=1

plt.subplots_adjust(left=0.03, right=0.97, bottom=0.04, top=0.91, wspace=0.32)
# plt.show()
fig = plt.gcf()
DPI = fig.get_dpi()
fig.set_size_inches(1536.0/float(DPI),768.0/float(DPI))
plt.savefig("imgs/currenciesdiff.png")

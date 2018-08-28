# Libraries
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import kde
from matplotlib.colors import ListedColormap
from database.dbGet import *
from math import log

def plot(axes):
    data = DbGet().getCompaniesToPlotPercentage()
    plot_data(axes=axes, nbins=[120,500], data=data, cmap=LinearSegmentedColormap('BlueRed1', {
        'red':     ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'green': ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0))
        }), color='blue')
    data = DbGet().getCompaniesToPlotAlg()
    plot_data(axes=axes, nbins=[120,120], data=data, cmap=LinearSegmentedColormap('BlueRed1', {
        'red':     ((0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0)),

         'green': ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0))
        }), color='red')
    data = DbGet().getCompaniesToPlotEMS()
    plot_data(axes=axes, nbins=[120,250], data=data, cmap=LinearSegmentedColormap('BlueRed1', {
        'red':     ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'green': ((0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0)),

         'blue':  ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0))
        }), color="green")

def plot_data(axes, nbins, data, cmap, color):
    prof_total = []
    rate = []

    for j in range(0, len(data)):
        rate.append( data [j][0])
        prof_total.append(data [j][1])

    prof_total = [log(p) for p in prof_total]
    # Get the colormap colors
    my_cmap = cmap(np.arange(cmap.N))
    # Set alpha
    my_cmap[:,-1] = np.linspace(0, 1, cmap.N)
    # Create new colormap
    my_cmap = ListedColormap(my_cmap)

    # 2D Histogram
    counts, xedges, yedges, im = axes.hist2d(rate, prof_total, bins=nbins, cmap=my_cmap)
    axes.set_xlim(0.4, 1)
    axes.set_ylim(-2.5, 2.5)
    plt.colorbar(im, ax=axes)

    print(rate,prof_total)
    # Paint linear regressions

    slope, intercept, r_value, p_value, std_err = stats.linregress(rate, prof_total)
    x = np.arange(0.4, 1.1, 0.01)



    axes.plot(x, slope*x+intercept, color=color)

ncols=1
nrows=1

# Create a figure with plot areas
fig, axes = plt.subplots(ncols=ncols, nrows=nrows)

# Plot
plot(axes)
axes.legend([
"B&H",
"With algorithm",
"EMS"],loc="upper right")

plt.subplots_adjust(left=0.03, right=0.97, bottom=0.04, top=0.91, wspace=0.32)
# plt.show()
fig = plt.gcf()
DPI = fig.get_dpi()
fig.set_size_inches(1536.0/float(DPI),768.0/float(DPI))
plt.savefig("imgs/alldiff.png")

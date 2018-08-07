# Libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import kde
from matplotlib.colors import ListedColormap

from database.dbGet import *

def plot(ncol, nrow, axes, sector, nbins, qDate):
    data = DbGet().getCompanyToPlotCurrencyByQDiff(sector, qDate)
    plot_data(ncol, nrow, axes, sector, nbins[0], qDate, data, LinearSegmentedColormap('BlueRed1', {
        'red':     ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'green': ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0))
        }))

def plot_data(ncol, nrow, axes, sector, nbins, qDate, data, cmap):
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

qDates = ["2017-07-01", "2017-04-01", "2017-01-01", "2016-10-01", "2016-07-01", "2016-04-01", "2016-01-01", "2015-10-01", "2015-07-01", "2015-04-01", "2015-01-01", "2014-10-01", "2014-07-01", "2014-04-01", "2014-01-01"]

for qDate in qDates:
    # Create a figure with plot areas
    fig, axes = plt.subplots(ncols=ncols, nrows=nrows)

    # Plot
    currencies = ["USD", "JPY", "EUR", "CAD", "AUD", "HKD", "INR", "GBX", "CNY"]
    nbins = [
        [[200, 200000], [200, 300]], #USD
        [[90, 90], [1, 1]], #JPY
        [[200, 2000], [40, 40]], #EUR
        [[100, 1000], [20, 20]], #CAD
        [[200, 3000], [50, 50]], #AUD
        [[200, 500], [10, 10]], #HKD
        [[100, 200], [5, 5]], #INR
        [[100, 100], [100, 1000]], #GBX
        [[70, 70], [10, 10]], #CNY
    ]

    k=0
    for j in range(nrows):
        for i in range(ncols):
            plot(j, i, axes, currencies[k], nbins[k], qDate)
            k+=1

    #Date title
    qDateSplit=qDate.split("-")
    quarters={
        "10": "4",
        "07": "3",
        "04": "2",
        "01": "1",
    }
    title=qDateSplit[0]+"Q"+quarters[qDateSplit[1]]
    plt.suptitle(title)
    plt.subplots_adjust(left=0.03, right=0.97, bottom=0.04, top=0.91, wspace=0.32)
    # plt.show()
    fig = plt.gcf()
    DPI = fig.get_dpi()
    fig.set_size_inches(1536.0/float(DPI),768.0/float(DPI))
    plt.savefig("imgs/"+title+'.png')

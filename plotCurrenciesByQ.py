# Libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import kde

from database.dbGet import *


def plot(ncol, nrow, axes, sector, nbins, qDate):
    data = DbGet().getCompanyToPlotCurrencyByQ(sector, qDate)

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


ncols=3
nrows=3

qDates = ["2017-07-01", "2017-04-01", "2017-01-01", "2016-10-01", "2016-07-01", "2016-04-01", "2016-01-01", "2015-10-01", "2015-07-01", "2015-04-01", "2015-01-01", "2014-10-01", "2014-07-01", "2014-04-01", "2014-01-01"]

for qDate in qDates:
    # Create a figure with plot areas
    fig, axes = plt.subplots(ncols=ncols, nrows=nrows)

    # Plot
    currencies = ["USD", "JPY", "EUR", "CAD", "AUD", "HKD", "INR", "GBX", "CNY"]
    nbins = [105, 71, 95, 95, 90, 75, 75, 90, 40]

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

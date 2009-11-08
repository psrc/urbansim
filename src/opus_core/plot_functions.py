#
# Opus software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from numpy import arange
from scipy.ndimage import histogram

def create_histogram(values, main="", xlabel="", bins=None):
    """Plot a histogram of values which is a numpy array.
    """
    from matplotlib.pylab import text
    mini = values.min()
    maxi = values.max()
    if bins == None:
        bins = int(maxi - mini)
    hist = histogram(values, mini, maxi+0.00001, bins)
    create_barchart(hist, bins, mini, maxi, main)
    text(maxi/2.0,-(hist.max()-hist.min())/20.0,s=xlabel,horizontalalignment='center',verticalalignment='top')

def plot_histogram(values, main="", xlabel="", bins=None):
    create_histogram(values, main, xlabel, bins)
    show_plots()

def create_barchart(values, bins=None, mini=None, maxi=None, main='', color='g'):
    """Create a bar chart of values."""
    from matplotlib.pylab import bar, xticks, title, axis
    if mini is None:
        mini = 0
    if maxi is None:
        maxi = values.size
    if bins is None:
        bins = values.size
    width_par = (maxi-mini)/bins
    bar(arange(mini, maxi, step = (maxi-mini)/bins), values, width=width_par, color='g')
    xticks(arange(mini, maxi, step = (maxi-mini)/bins).tolist())
    title(main)
    Axis = axis()

def plot_barchart(values, main='', labels=None):
    """Plot a bar chart and put labels (list) on the x-axis"""
    from matplotlib.pylab import text
    create_barchart(values, main=main)
    if labels is not None:
        for ilabel in range(1, len(labels)+1):
            text(ilabel-0.5,-0.5,s=labels[ilabel-1],horizontalalignment='center',verticalalignment='top',
                 rotation='vertical')
    show_plots()

def create_matplot(matrix, xlabels=None, ylabels=None, main=''):
    """Creates a image from a matrix."""
    from matplotlib.pylab import matshow, xticks, text, title, normalize, setp, gca, colorbar
    norm = normalize(matrix.min(), matrix.max())
    image = matshow(matrix, norm=norm)
    nrows, ncols = matrix.shape
    if xlabels is not None:
        #xticks(arange(ncols)+0.5, xlabels)
        setp(gca(), xticks=[])
        for icol in range(ncols):
            text(icol+0.5, -0.5, xlabels[icol], horizontalalignment='right', rotation='vertical')
    if ylabels is not None:
        setp(gca(), yticks=[])
        for irow in range(nrows):
            text(-0.5, irow+0.5, ylabels[irow], horizontalalignment='right')
    tickfmt='%1.4f'
    colorbar(format=tickfmt)
    title(main)

def plot_matplot(*args, **kwargs):
    create_matplot(*args, **kwargs)
    show_plots()

def show_plots():
    from matplotlib.pylab import show
    show()
# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

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

def plot_scatter(x, y, x_label=None, y_label=None, main = "", **kwargs):
    from matplotlib.pylab import scatter, xlabel, ylabel, title
    scatter(x,y, **kwargs)
    if x_label is not None:
        xlabel(x_label)
    if y_label is not None:
        ylabel(y_label)
    title(main)
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
    width_par = 1.*(maxi-mini)/bins
    bar(arange(mini, maxi, step = 1.*(maxi-mini)/bins), values, width=width_par, color='g')
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
    
def plot_values_as_boxplot_r(values_dict, filename=None, logy=False, device='png'):
    """Create a set of boxplots (using R), one plot per variable in values_dict (dictionary of 
    varible name and values (1- or 2-D array)), one box per row.
    If filename is given, the plot goes into that file as pdf. If 'logy' is  True, the y-axis
    is plotted on the log scale.
    """
    import rpy2.robjects as robjects

    r = robjects.r
    
    logstring = ''
    if logy:
        logstring='y'
        
    if filename:
        rcode = '%s("%s")' % (device, filename)
        r(rcode)
    else:
        r.X11()
        
    for var, values in values_dict.iteritems():
        plot_one_boxplot_r(values, var, logstring)

    if filename:
        r['dev.off']()
            
def plot_one_boxplot_r(values, main="", logstring=""):
    import rpy2.robjects as robjects
    import rpy2.robjects.numpy2ri # this turns on an automatic conversion from numpy to rpy2 objects
    from numpy import array

    r = robjects.r
    if values.ndim == 1:
        v = resize(values, (1, values.size))
    else:
        v = values
    r.boxplot(v[0,:], xlim=array([0,v.shape[0]+1]), ylim=array([values.min(), values.max()]), range=0, log=logstring,
              main=main)
    for i in range(1, v.shape[0]):
        r.boxplot(v[i,:], at=i, add=True, range=0, log=logstring)
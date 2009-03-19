# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from scipy.ndimage import histogram
from numpy import reshape, arange, where
from opus_core.misc import DebugPrinter
from opus_core.resources import Resources
from opus_core.logger import logger

class upc_sequence(object):
    """
        Invokes computation of utilities, probabilities and choices.
    """
    def __init__(self, utility_class=None, probability_class=None, choice_class=None, resources=None, debuglevel=0):
        """utility_class, probability_class, choice_class are objects of the corresponding classes.
            They must have a method 'run'.
        """
        self.utility_class = utility_class
        self.probability_class = probability_class
        self.choice_class = choice_class
        self.resources = resources
        if self.resources == None:
            self.resources = Resources()
        self.utilities = None
        self.probabilities = None
        self.choices = None
        self.debug = DebugPrinter(debuglevel)

    def run(self, data=None, coefficients=None, resources=None):
        local_resources = Resources()
        if resources:
            local_resources.merge(resources)
        last_result = self.compute_utilities(data, coefficients, local_resources)
        this_result = self.compute_probabilities(local_resources)
        if this_result <> None:
            last_result = this_result
        this_result = self.compute_choices(local_resources)
        if this_result <> None:
            last_result = this_result
        return last_result

    def compute_utilities(self, data=None, coefficients=None, resources=None):
        if self.utility_class is None:
            self.debug.print_debug("No utilities class given.",10)
            return None
        self.debug.print_debug("compute_utilities ...",3)
        self.utilities = self.utility_class.run(data, coefficients, resources)
        return self.utilities

    def compute_probabilities(self, resources=None):
        if self.probability_class is None:
            self.debug.print_debug("No probabilities class given.",10)
            return None
        self.debug.print_debug("compute_probabilities ...",3)
        self.probabilities = self.probability_class.run(self.utilities, resources)
        return self.probabilities

    def compute_choices(self, resources=None):
        if self.choice_class is None:
            self.debug.print_debug("No choices class given.",10)
            return None
        self.debug.print_debug("compute_choices ...",3)
        self.choices = self.choice_class.run(self.probabilities, resources)
        return self.choices

    def get_utilities(self):
        return self.utilities

    def get_probabilities(self):
        return self.probabilities

    def write_probability_sums(self):
        self.probability_class.check_sum(self.probabilities)

    def get_choices(self):
        return self.choices

    def get_choice_histogram(self, min=None, max=None, bins=None):
        """Give an array that represents a histogram of choices."""
        if max == None:
            max = self.choices.max()+1
        if min == None:
            min = self.choices.min()
        if bins == None:
            bins = max-min
        return histogram(self.get_choices(),min,max,bins)

    def get_probabilities_sum(self):
        """Return probabilities sum along the first axis.
        """
        probs = self.get_probabilities()
        if probs.ndim < 2:
            return probs.sum()
        return reshape(sum(probs,0),probs.shape[1])

    def plot_choice_histograms(self, capacity, main=""):
        self.plot_histogram(numrows=2)
        self.plot_histogram_with_capacity(capacity)

    def plot_histogram(self, main="", numrows=1, numcols=1, fignum=1):
        """Plot a histogram of choices and probability sums. Expects probabilities as (at least) a 2D array.
        """
        from matplotlib.pylab import bar, xticks,yticks,title,text,axis,figure,subplot

        probabilities = self.get_probabilities()
        if probabilities.ndim < 2:
            raise StandardError, "probabilities must have at least 2 dimensions."
        alts = probabilities.shape[1]
        width_par = (1/alts+1)/2.0
        choice_counts = self.get_choice_histogram(0, alts)
        sum_probs = self.get_probabilities_sum()

        subplot(numrows, numcols, fignum)
        bar(arange(alts),choice_counts,width=width_par)
        bar(arange(alts)+width_par,sum_probs,width=width_par,color='g')
        xticks(arange(alts))
        title(main)
        Axis = axis()
        text(alts+.5,-.1,"\nchoices histogram (blue),\nprobabilities sum (green)",horizontalalignment='right',verticalalignment='top')

    def plot_histogram_with_capacity(self, capacity, main=""):
        """Plot histogram of choices and capacities. The number of alternatives is determined
        from the second dimension of probabilities.
        """
        from matplotlib.pylab import bar, xticks,yticks,title,text,axis,figure,subplot

        probabilities = self.get_probabilities()
        if probabilities.ndim < 2:
            raise StandardError, "probabilities must have at least 2 dimensions."
        alts = self.probabilities.shape[1]
        width_par = (1/alts+1)/2.0
        choice_counts = self.get_choice_histogram(0, alts)
        sum_probs = self.get_probabilities_sum()

        subplot(212)
        bar(arange(alts),choice_counts,width=width_par)
        bar(arange(alts)+width_par,capacity,width=width_par,color='r')
        xticks(arange(alts))
        title(main)
        Axis = axis()
        text(alts+.5,-.1,"\nchoices histogram (blue),\ncapacities (red)",horizontalalignment='right',verticalalignment='top')

    def show_plots(self, file=None):
        """Render the plots that have been generated.
        This method should be the last method called in the script, since it hands control to
        matplotlib's rendering backend.
        """
        from matplotlib.pylab import show, savefig
        if file is not None:
            savefig(file)
        else:
            show()

    def summary(self):
        logger.log_status("utilities")
        logger.log_status(self.get_utilities())
        logger.log_status("probabilities")
        logger.log_status(self.get_probabilities())
        logger.log_status("probabilities sums")
        self.write_probability_sums()
        logger.log_status("choices")
        logger.log_status(self.get_choices())

    def get_excess_demand(self,capacity):
        demand = self.get_probabilities_sum()
        return where(demand>capacity,demand-capacity,0)

    def get_dependent_datasets(self):
        result = []
        if self.utility_class is not None:
            try:
                result = result + self.utility_class.get_dependent_datasets()
            except:
                pass
        if self.probability_class is not None:
            try:
                result = result + self.probability_class.get_dependent_datasets()
            except:
                pass
        if self.choice_class is not None:
            try:
                result = result + self.choice_class.get_dependent_datasets()
            except:
                pass
        return result
# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.choices import Choices
from opus_core.random_choices import random_choices
from opus_core.misc import take_choices

class random_choices_from_index(Choices):
    """ Like random_choices, but uses an index (see docs for the compute method)."""

    def run(self, probability, resources=None):
        """ Compute choices according to given probability, where the choices are indices
        that correspond to an index-array given in resources["index"] (1D or 2D array).
        'probability' is a 2D numpy array (nobservation x nequations).
        The returned value is a 1D array of choice indices [0, nequations-1] of length nobservations.
        If the entry 'index' is missing, the returned value is the returned value of 'random_choices'.
        """
        choice_idx = random_choices().run(probability, resources)
        index = resources.get("index", None)
        if index <> None:
            return take_choices(index, choice_idx) # transfer random choices to indices
        return choice_idx

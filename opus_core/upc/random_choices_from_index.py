# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.choices import Choices
from opus_core.random_choices import random_choices
from opus_core.misc import take_choices
from numpy import where

class random_choices_from_index(Choices):
    """ Like random_choices, but uses an index (see docs for the compute method)."""

    def run(self, probability, resources=None):
        """ Compute choices according to given probability, where the choices are indices
        that correspond to an index-array given in resources["index"] (1D or 2D array).
        'probability' is a 2D numpy array (nobservation x nequations).
        The returned value is a 1D array of choice indices [0, nequations-1] of length nobservations.
        If the entry 'index' is missing, the returned value is the returned value of 'random_choices'.
        """
        allow_no_choice_availability = resources.get("allow_no_choice_availability", True)
        if allow_no_choice_availability:
            zero_prob_sum = where(probability.sum(axis=1)==0)[0]
            if zero_prob_sum.size > 0:            # agents with no availability of choices
                probability[zero_prob_sum, 0] = 1 # to pass the random choices call
 
        choice_idx = random_choices().run(probability, resources)
        index = resources.get("index", None)
        if index <> None:
            choice_idx = take_choices(index, choice_idx) # transfer random choices to indices
        if allow_no_choice_availability and zero_prob_sum.size > 0:
            choice_idx[zero_prob_sum] = resources.get("choice_value_for_no_availability", -1)
        return choice_idx

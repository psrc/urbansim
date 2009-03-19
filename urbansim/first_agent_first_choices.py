# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from numpy import array, ones, arange, argsort
from urbansim.lottery_choices import lottery_choices
from scipy.ndimage import sum as ndimage_sum

class first_agent_first_choices(lottery_choices):
    """The same as lottery_choices but only one agent per choice is allowed.
    In conflict cases only the first agent can keep its choice, all others must choose again.
    """

    def get_choice_histogram(self, units_to_occupy, choices, nchoices):
        """Counts the number of agents that decided for each choice.
        """
        return array(ndimage_sum(ones((choices.size,)), labels=choices+1, index=arange(nchoices)+1))

    def get_choice_capacity_difference(self, hist, capacity):
        is_capacity = (capacity>0).astype("int8")
        return is_capacity - hist

    def sample_agents_for_new_choice(self, ialt, idx, units, capacity):
        return idx[1:idx.size]

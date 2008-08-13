#
# Opus software. Copyright (C) 2005-2008 University of Washington
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

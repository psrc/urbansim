# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.choices import Choices
from numpy import where, array, compress, arange, logical_not
from numpy import ndarray, zeros, sometrue, ones, concatenate
from opus_core.ndimage import sum as ndimage_sum
from numpy import ma
from opus_core.random_choices_from_index import random_choices_from_index
from opus_core.misc import unique
from opus_core.logger import logger
from numpy.random import permutation


class lottery_choices(Choices):
    def run(self, probability, resources=None):
        """ Compute choices according to given probability -- Lottery procedure.
        'probability' is a 2D numpy array (nobservation x nequations).
        The returned value is a 1D array of choice indices [0, nequations-1] of the length nobservations.
        The argument 'resources' must contain an entry 'capacity'. It is 1D array whose number of elements
        corresponds to the number of choices.
        Each agent has a certain number of units to occupy the location. This information
        can be passed in an entry 'agent_units' of 'resources' which is a 1D array
        of the length of nobservations. If it is missing or is None, it is assumed that all agents occupy
        1 unit per location.
        Optional entry 'index' (1D or 2D array) gives indices of the choices.
        """
        if probability.ndim < 2:
            raise StandardError, "Argument 'probability' must be a 2D numpy array."

        resources.check_obligatory_keys(["capacity"])
        capacity = resources["capacity"]
        if not isinstance(capacity, ndarray):
            capacity = array(capacity)
        ncap = capacity.size
        neqs = probability.shape[1]
        nobs = probability.shape[0]
        units = resources.get("agent_units", None)
        if units is None:
            units = ones((nobs,))
        if not isinstance(units, ndarray):
            units = array(units)
        if nobs <> units.size:
            raise StandardError, "Mismatch in shape of probability and length of agent_units."
        index = resources.get("index", None)
        if index is None:
            index = arange(ncap)
        unique_index = unique(index.ravel())

        if index.ndim <= 1:
            index = index.reshape((1,index.size))
            index = index.repeat(repeats=nobs, axis=0)
        resources.merge({"index":index})
        choices = random_choices_from_index().run(probability, resources)
        hist = self.get_choice_histogram(units, choices, ncap)
        choice_capacity_diff = self.get_choice_capacity_difference(hist, capacity)
        fullarray = (choice_capacity_diff <= 0).astype("int8")
        full = compress(fullarray[unique_index], arange(unique_index.size))
        over = where(choice_capacity_diff < 0)[0]

        maxiter = resources.get("lottery_max_iterations",  3)
        iter=1
        while (full.size <= unique_index.size) and (over.size > 0):
            iter += 1
            fullmatrix = fullarray[index] # matrix of size index where 1 on spots that have no vacancy, 0 otherwise
            choose_again = array([], dtype='int32')
            for ialt in over: #determine which agents need to choose again
                idx = where(choices == ialt)[0]
                draw = self.sample_agents_for_new_choice(ialt, idx, units, capacity)
                choose_again = concatenate((choose_again, draw)) #randomly drawn
            if choose_again.size <= 0:
                iter = iter-1
                break
            choices[choose_again] = -1
            if iter > maxiter:
                iter = iter-1
                break
            new_probability = ma.masked_array(probability,
                                              mask = fullmatrix.reshape(probability.shape))
            sizes = ma.count(new_probability, axis=1)
            choosers_out = zeros((choose_again.size,))
            out = (sometrue(ma.filled(new_probability,0.0), axis=1) == 0).astype("int8")
            choosers_out = where((sizes[choose_again] <= 0) + out[choose_again],1,choosers_out)
            choosers_out_idx = compress(choosers_out, arange(choosers_out.size))
            if choosers_out_idx.size > 0: # choosers whose choices are all full
                choose_again = compress(logical_not(choosers_out), choose_again)

            new_probability = ma.filled(new_probability,0.0)
            out = where(sometrue(ma.filled(new_probability,0.0), axis=1) == 0)[0]
            new_probability[out,0] = 1.0 # in order not to have all probs 0.

            new_choice = random_choices_from_index().run(new_probability, resources)
            choices[choose_again] = new_choice[choose_again]
            hist = self.get_choice_histogram(units, choices, ncap)
            choice_capacity_diff = self.get_choice_capacity_difference(hist, capacity)
            fullarray = (choice_capacity_diff <= 0).astype("int8") # what alts are full
            full = compress(fullarray[unique_index], arange(unique_index.size))
            over = where(choice_capacity_diff < 0)[0]
        logger.log_status("Number of unplaced agents: " + str(where(choices < 0)[0].size) + " (in " + str(iter) + " iterations)")
        return choices

    def get_choice_histogram(self, units_to_occupy, choices, nchoices):
        """Return a histogram of agent choices, where each agents occupy number of units given
        in 'units_to_occupy'. 'choices' are the agent choices of a location (as an index).
        'nchoices' is a number of unique values for possible choices.
        """
        return array(ndimage_sum(units_to_occupy, labels=choices+1, index=arange(nchoices)+1))

    def get_choice_capacity_difference(self, hist, capacity):
        return capacity-hist

    def sample_agents_for_new_choice(self, ialt, idx, units, capacity):
        permutate = array(permutation(idx.size).tolist(), dtype="int32")
        csum = units[idx[permutate]].cumsum()
        draw = idx[permutate[where(csum > capacity[ialt])]]
        return draw

from opus_core.tests import opus_unittest
from opus_core.resources import Resources
from opus_core.tests.stochastic_test_case import StochasticTestCase

class Tests(StochasticTestCase):
    def setUp(self):
        pass
    def test_lottery_choices_without_index_no_capacity_constrains_equal_units(self):
        probabilities = array(10*[[0.3, 0.2, 0.1, 0.4]] +
                               10*[[0.25, 0.25, 0.25, 0.25]] +
                               10*[[0.7, 0.1, 0.1, 0.1]]
                                    )
        capacity = array([100000, 100000, 100000, 100000])
        units = array(30*[1], dtype="int32")
        resources = Resources({"capacity": capacity, "agents_units": units})

        def run():
            lottery = lottery_choices()
            choices = lottery.run(probabilities, resources=resources)
            return lottery.get_choice_histogram(units, choices, capacity.size)

        self.run_stochastic_test(__file__, run, array([3+2.5+7, 2+2.5+1, 1+2.5+1, 4+2.5+1]), 10)

    def test_lottery_choices_without_index_with_capacity_constrains_equal_units(self):
        probabilities = array(10*[[0.3, 0.2, 0.1, 0.4]] +
                               10*[[0.25, 0.25, 0.25, 0.25]] +
                               10*[[0.7, 0.1, 0.1, 0.1]]
                                    )
        capacity = array([10, 3, 5, 100000])
        units = array(30*[1], dtype="int32")
        resources = Resources({"capacity": capacity, "agents_units": units})

        def run():
            lottery = lottery_choices()
            choices = lottery.run(probabilities, resources=resources)
            return lottery.get_choice_histogram(units, choices, capacity.size)

        for i in range(10):
            result = run()
            self.assertEqual(ma.allequal(result <= array([10, 3, 5, 100000]),
                                         array([True, True, True, True])), True,
                             msg = "Error in lottery_choices when capacity constrains.")

if __name__=='__main__':
    opus_unittest.main()
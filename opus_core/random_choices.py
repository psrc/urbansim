# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.choices import Choices
from opus_core.sampling_toolbox import sample_choice
from numpy import concatenate
from numpy import reshape


class random_choices(Choices):
    def run(self, probability, resources=None):
        """ Compute choices according to given probability.
        'probability' is a 2D numpy array (nobservations x nequations).
        The returned value is a 1D array of choice indices [0, nequations-1] of length nobservations.
        """
        if probability.ndim == 1: # if 1d array, add column of 1-probability
            probability = reshape(probability, (probability.size,1))
            probability = concatenate((1.0-probability, probability), axis=1)

        if probability.ndim < 2:
            raise StandardError, "Argument 'probability' must be a 2D numpy array."

        prob = probability/reshape(probability.sum(axis=1),(probability.shape[0],1))
        return sample_choice(prob)[1]


from opus_core.tests import opus_unittest

from numpy import array, zeros

from opus_core.tests.stochastic_test_case import StochasticTestCase


class RandomChoicesTests(StochasticTestCase):
    def test_random_choices(self):
        """Setup probabilities for 4 alternatives and 4 agents. Run random_choices 100 times
        and count how many times each alternative was selected for each agent. The counts
        should be proportional to the probabilities.
        """
        probs = array([
            [0,0,0.5,0.5],
            [0.25,0.25,0.25,0.25],
            [1,0,0,0],
            [0.6,0.3,0.1,0]
            ])
            
        def run_model():
            result = zeros((4,4), dtype="int32")
            
            for i in range(100):
                choices = random_choices().run(probs)
                for j in range(len(choices)):
                    result[j,choices[j]] += 1
                    
            return result.ravel()

        expected_results = array([ 0,  0, 50, 50, 25, 25, 25, 25, 100, 0, 0, 0, 60, 30, 10, 0])
        self.run_stochastic_test(__file__, run_model, expected_results, 10)


if __name__ == '__main__':
    opus_unittest.main()
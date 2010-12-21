# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import ones, zeros, where, compress
from opus_core.linear_utilities import linear_utilities

class hierarchical_linear_utilities(linear_utilities):
    """    
    Class for computing linear utilities in hierarchical models with multiple nests.
    """
    def run(self, data, coefficients, resources=None):
        """
        'data' is a 4D numpy array (nobservations x nequations x ncoefficients x number of nests) 
        and it can be created by InteractionDataset.create_logit_data(...). 
        'coefficients' is either a 1D array (ncoefficients + number of nests) used 
        for estimating, or a 3D array (nequations x nvariables x number of nests) used for simulating.
        In the former case, the additional elements (number of nests) contain additional parameters
        (not used in the utility computation, such as scaling parameters). In the latter case, 
        the additional parameters are extracted from the array. They correspond to variables called '__logsum'.
        The method returns a tuple (u, mu) where u is
        a 2D array of utilities (nobservations x number of elemental alternatives). 
        mu is an array of additional parameters from the coefficient arrays not used in the utility 
        computation.
        The method calls its parent's run method (class lineear_utilities) for each nest.
        The class can be paired with the probabilities class opus_core.nl_probabilities.
        """
        nobs, nalts, nvars, M = data.shape
        result = zeros((nobs, nalts))
        addpar = zeros(M)
        if coefficients.ndim > 2:
            coef_object = resources.get('specified_coefficients', None)
                          
        for nest in range(M):
            d=data[:,:,:,nest]  
            if coefficients.ndim == 1:
                coef = coefficients[0:nvars]
                addpar[nest] = coefficients[nvars+nest]
            elif coefficients.ndim == 3:
                idx_logsum = where(array(coef_object.get_variable_names()) == '__logsum')[0]
                coef = coefficients[:,:,nest]
                filter = ones(coef.shape[1], dtype='bool8')
                filter[idx_logsum]= False
                coef = coef.compress(filter, axis=1)
                d = d.compress(filter, axis=2)
                addpar[nest] = coefficients[:,idx_logsum, nest].sum()
            else:
                raise StandardError, "Coefficients have wrong dimension."
            u = linear_utilities.run(self, d, coef, resources)
            result = result+u
            
        return (result, addpar) 

from opus_core.tests import opus_unittest
from numpy import array, repeat, reshape
from numpy import ma

class HierarchicalLinearUtilitiesTests(opus_unittest.OpusTestCase):
    def test_hierarchical_linear_utilities_coef_1D(self):

        data = array([[[[3,0], [5,0], [6,0], [5,0]], [[2,0], [1,0], [0,0], [0,0]], [[7,0], [2,0], [3,0], [5,0]]] + \
                      [[[0,3], [0,5], [0,6], [0,5]], [[0,2], [0,1], [0,0], [0,0]], [[0,7], [0,2], [0,3], [0,5]]],
                      [[[5,0], [1,0], [5,0], [2,0]], [[4,0], [7,0], [9,0], [2,0]], [[7,0], [2,0], [3,0], [5,0]]] + \
                      [[[0,5], [0,1], [0,5], [0,2]], [[0,4], [0,7], [0,9], [0,2]], [[0,7], [0,2], [0,1], [0,3]]]])                                               
                                                      
                            
        #data = repeat(reshape(data, list(data.shape)+[1]), repeats=2, axis=3)
        
        coefficients = array([2.5, 1.2, 4, 9, 0, 1])
        
        utilities, mu = hierarchical_linear_utilities().run(data, coefficients)

        should_be1 = array([[ 82.5,  6.2,  76.9, 82.5,   6.2,  76.9],
                            [ 51.7,  72.4, 76.9, 51.7,  72.4,  50.9]])
        
        should_be2 = (array([0, 1]))
        self.assertEqual(ma.allclose(utilities, should_be1, rtol=1e-05),
                             True, msg = "Error in test_hierarchical_linear_utilities_2d_tree_structure (1)")
        self.assertEqual(mu.size == should_be2.size,
                             True, msg = "Error in test_hierarchical_linear_utilities_2d_tree_structure (2)")
        self.assertEqual(ma.allclose(mu, should_be2, rtol=1e-05),
                             True, msg = "Error in test_hierarchical_linear_utilities_2d_tree_structure (3)")

        
                                                                                   
if __name__ == '__main__':
    opus_unittest.main()
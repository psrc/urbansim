# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

#
from numpy import exp, reshape, where, arange, sum, zeros, log, ones, inf, isnan
from opus_core.misc import unique
from opus_core.ndimage import sum as ndimage_sum
from opus_core.probabilities import Probabilities
from opus_core.logger import logger

class nl_probabilities(Probabilities):
    """Compute probabilities of a nested logit model from the given utilities.
    Currently works only for a two-level model.
    
    Implemented as UMNL (McFadden's utility maximizing nested logit) defined in:
    Koppelman, Wen (1998): Alternative Nested Logit Models: Structure, Properties and Estimation
    
    It has the ability to correct for sampling bias.
    """
    _computable_range = (-87.0, 87.0)   # float32 (the value is exponantiated)
#    computable_range = (-703.0, 703.0) # float64

    def run(self, utilities, resources=None):
        """ 
        'utilities' is a tuple (u, mu) where u is
        a 2D array of utilities (nobservations x number of elemental alternatives). 
        The indexing of the alternatives corresponds to the membership in nests (see below). 
        mu is an array of scaling parameters for each nest.
        The return value is a 2D array (nobservations x nalternatives).
        'resources' should contain an entry 'membership_in_nests' which is a dictionary containing 
        information about the membership of alternatives in nests. It should have as many elements
        as the nested logit model has levels minus one (i.e. two-level model has one element). The value 
        of each element is a 2D array of size (number of nests x number of children (branches)).
        It can have a third dimension for the observations which becomes the first dimension.
        It contains 1 where child belongs to a nest, 0 otherwise.
        If 'membership_in_nests' is missing, all alternatives are considered to be in one nest.
        'resources' can contain an entry 'correct_for_sampling' (logical) which determines if
        sampling correction should be applied. If it is the case, 'sampling_rate' must be provided 
        in 'resources' which is an array of size number_of_nests, with sampling rate for each nest.
        Both entries are set automatically in HierarchicalChoiceModel.
        The module can be paired with the Utilities class opus_core.hierarchical_linear_utilities.
        """
        utils, mu = utilities
        nalts = utils.shape[1]
        if (resources is None) or (resources.get('membership_in_nests', None) is None):
            M = 1
            leaves = ones((M, nalts))
        else:
            leaves = resources.get('membership_in_nests')[0]
            if leaves.ndim < 3:
                M = leaves.shape[0] # number of nests
            else:
                M = leaves.shape[1]
            
        N = utilities[0].shape[0] # number of observations
        
        util_min = utils.min()
        util_max = utils.max()
        if (util_min < self._computable_range[0]) or (util_max > self._computable_range[1]):
            # shift utilities to zero (maximum is at zero)
            to_be_transformed=where((utils < self._computable_range[0]) + (utils > self._computable_range[1]))
            to_be_transformed=unique(to_be_transformed[0])
            for idx in arange(to_be_transformed.size):
                i = to_be_transformed[idx]
                this_max = utils[i,:].max()
                utils[i,:]=utils[i,:]-this_max
        
        correct_for_sampling = resources.get('correct_for_sampling', False)
        sampling_rate = resources.get('sampling_rate', None)
        if correct_for_sampling and sampling_rate is None:
            raise StandardError, "If correct_for_sampling is True, sampling_rate must be given."
        availability = resources.get('availability', None)
        # compute logsum and conditional probability
        logsum = zeros((N,M), dtype="float64")
        Pnm = zeros((utils.shape), dtype="float64")
        if leaves.ndim < 3:
            for nest in range(M):
                altsidx = where(leaves[nest,:])[0]
                exponentiated_utility = exp(utils[:,altsidx]/mu[nest])
                if availability is not None:
                    exponentiated_utility = exponentiated_utility *(availability[:,altsidx]).astype('b')
                sum_exponentiated_utility = sum(exponentiated_utility, axis=1, dtype="float64")
                #if any(sum_exponentiated_utility<=0) or any(sum_exponentiated_utility == inf):
                #    return zeros(utils.shape)
                if correct_for_sampling:
                    if 0 in altsidx: # chosen alternative belongs to this nest (it is assumed that chosen alternative is at position 0)
                        exponentiated_utility_logsum = exponentiated_utility.copy()
                        exponentiated_utility_logsum[:,1:] = exponentiated_utility[:,1:]/sampling_rate[nest]
                        sum_exponentiated_utility_logsum = sum(exponentiated_utility_logsum, axis=1, dtype="float64")
                    else:
                        sum_exponentiated_utility_logsum = sum_exponentiated_utility/sampling_rate[nest]
                else:
                    sum_exponentiated_utility_logsum = sum_exponentiated_utility
                logsum[:,nest] = log(sum_exponentiated_utility_logsum)
                Pnm[:, altsidx] = exponentiated_utility/reshape(sum_exponentiated_utility,(N, 1))
        else: # for 3D tree structure the index is handled differently
            for nest in range(M):
                altsidx = where(leaves[:,nest,:])
                neleminnest = where(leaves[0,nest,:])[0].size
                exponentiated_utility = reshape(exp(utils[altsidx]/mu[nest]), (N, neleminnest))
                if availability is not None:
                    exponentiated_utility = exponentiated_utility *(availability[:,altsidx]).astype('b')
                sum_exponentiated_utility = sum(exponentiated_utility, axis=1, dtype="float64")
                if any(sum_exponentiated_utility<=0) or any(sum_exponentiated_utility == inf):
                    return zeros(utils.shape)
                if correct_for_sampling:
                    where_chosen_alt_in_this_nest = where(altsidx[1] == 0)[0] #it is assumed that chosen alternative is at position 0
                    where_chosen_alt_not_in_this_nest = where(altsidx[1] <> 0)[0]
                    exponentiated_utility_logsum = exponentiated_utility.copy()
                    for j in where_chosen_alt_in_this_nest:
                        exponentiated_utility_logsum[altsidx[0][j],1:] = exponentiated_utility[altsidx[0][j],1:]/sampling_rate[nest]
                    agent_idx_where_chosen_alt_not_in_this_nest = unique(altsidx[0][where_chosen_alt_not_in_this_nest])
                    exponentiated_utility_logsum[agent_idx_where_chosen_alt_not_in_this_nest,:] = exponentiated_utility[agent_idx_where_chosen_alt_not_in_this_nest,:]/sampling_rate[nest]
                    sum_exponentiated_utility_logsum = sum(exponentiated_utility_logsum, axis=1, dtype="float64")
                else:
                    sum_exponentiated_utility_logsum = sum_exponentiated_utility
                logsum[:,nest] = log(sum_exponentiated_utility_logsum)
                Pnm[altsidx] = (exponentiated_utility/reshape(sum_exponentiated_utility,(N, 1))).flat
        nanidx_logsum = isnan(logsum)
        nanidxPnm = isnan(Pnm)
        if nanidx_logsum.any() or nanidxPnm.any():
            logger.log_warning("Some nests not available to some agents (logsum is zero or infinity).")
            logsum[where(nanidx_logsum)] = 0
            Pnm[where(nanidxPnm)] = 0
                
        # compute marginal probability
        nomin = exp(mu*logsum)
        denomin = sum(nomin, axis=1, dtype="float64")
        Pm = nomin/reshape(denomin, (N,1))
        
        # compute the joint probability
        Pn = zeros(utils.shape, dtype="float64")
        if leaves.ndim < 3:
            for nest in range(M):
                altsidx = where(leaves[nest,:])[0]
                Pn[:,altsidx] = Pnm[:,altsidx] * reshape(Pm[:,nest], (N,1))
        else:
            for nest in range(M):
                altsidx = where(leaves[:,nest,:])
                Pn[altsidx] = (reshape(Pnm[altsidx], (N, neleminnest)) * reshape(Pm[:,nest], (N,1))).flat
            
        return Pn/reshape(sum(Pn, axis=1, dtype="float64"), (N,1))
    
from opus_core.tests import opus_unittest
from numpy import array
from numpy import ma
class NLProbabilitiesTests(opus_unittest.OpusTestCase):
    def test_nl_probabilities(self):
        utilities = (array([[ 82.5,   4,  32.9, 82.5,   6.2,  76.9],   # utilities for agent 1
                            [ 51.7,  53,  32.9, 51.7,  72.4,  76.9]]), # utilities for agent 2
                     array([0.5, 0.8]) # scaling parameters
                     )
        resources = {'membership_in_nests': {0:  #         nest 1          nest 2  (applies to both agents)
                                                 array([[0,0,0,1,1,1], [1,1,1,0,0,0]])}}
        result = nl_probabilities().run(utilities, resources=resources)
        # check the first agent
        nom1 = exp(array([82.5,   6.2,  76.9])/0.5)
        nom2 = exp(array([82.5,   4,  32.9])/0.8)
        denom1 = nom1.sum()
        denom2 = nom2.sum()
        logsum1 = log(denom1)
        logsum2 = log(denom2)
        nomm1 = exp(0.5*logsum1)
        nomm2 = exp(0.8*logsum2)
        denomm = nomm1+nomm2
        should_be = array([nom2[0]/denom2 * nomm2/denomm, nom2[1]/denom2 * nomm2/denomm, nom2[2]/denom2 * nomm2/denomm,
                    nom1[0]/denom1 * nomm1/denomm, nom1[1]/denom1 * nomm1/denomm, nom1[2]/denom1 * nomm1/denomm])
        self.assertEqual(ma.allclose(result[0,:], should_be, atol=min(1e-8, should_be.min())), True)

        # test for a 3d structure of 'membership_in_nests', i.e. each agent has different structure of the nests
        resources = {'membership_in_nests': {0: #            nest 1        nest 2
                                                 array([[[0,0,0,1,1,1], [1,1,1,0,0,0]],   # agent 1
                                                        [[0,0,1,0,1,1], [1,1,0,1,0,0]]]   # agent 2
                                                       )}}
        result = nl_probabilities().run(utilities, resources=resources)

        # check the second agent
        nom1 = exp(array([32.9,   72.4,  76.9])/0.5)
        nom2 = exp(array([51.7,   53,  51.7])/0.8)
        denom1 = nom1.sum()
        denom2 = nom2.sum()
        logsum1 = log(denom1)
        logsum2 = log(denom2)
        nomm1 = exp(0.5*logsum1)
        nomm2 = exp(0.8*logsum2)
        denomm = nomm1+nomm2
        should_be = array([nom2[0]/denom2 * nomm2/denomm, nom2[1]/denom2 * nomm2/denomm, nom1[0]/denom1 * nomm1/denomm,
                    nom2[2]/denom2 * nomm2/denomm, nom1[1]/denom1 * nomm1/denomm, nom1[2]/denom1 * nomm1/denomm])
        self.assertEqual(ma.allclose(result[1,:], should_be, atol=min(1e-8, should_be.min())), True)
        
    def test_nl_probabilities_with_sampling(self):
        utilities = (array([[ 7.3,   4,  10.9, 5.5,   6.2,  1.6], # utilities for agent 1
                            [ 0.3,  1.9,  4.8, 9.1,  5.3,    0]]),# utilities for agent 2
                     array([0.5, 0.8]) # scaling parameters
                     )
        resources = {'membership_in_nests': {0: #         nest 1          nest 2  (applies to both agents)
                                                 array([[0,0,0,1,1,1],  [1,1,1,0,0,0]])},
                     'correct_for_sampling': True,
                     'sampling_rate':  #  nest 1  nest 2
                                     array([0.02, 0.05])                                 
                                                       }
        result = nl_probabilities().run(utilities, resources=resources)
        # check the first agent
        nom1 = exp(array([5.5,   6.2,  1.6])/0.5)
        nom2 = exp(array([7.3,   4,  10.9])/0.8)
        denom1 = nom1.sum()
        denom2 = nom2.sum()
        logsum1 = log(denom1/0.02)
        corr_nom2 = array([exp(7.3/0.8), exp(4/0.8)/0.05, exp(10.9/0.8)/0.05])
        logsum2 = log(corr_nom2.sum())
        nomm1 = exp(0.5*logsum1)
        nomm2 = exp(0.8*logsum2)
        denomm = nomm1+nomm2
        should_be = array([nom2[0]/denom2 * nomm2/denomm, nom2[1]/denom2 * nomm2/denomm, nom2[2]/denom2 * nomm2/denomm,
                    nom1[0]/denom1 * nomm1/denomm, nom1[1]/denom1 * nomm1/denomm, nom1[2]/denom1 * nomm1/denomm])

        self.assertEqual(ma.allclose(result[0,:], should_be, atol=min(1e-8, should_be.min())), True)

        # test for a 3d structure of 'membership_in_nests', i.e. each agent has different structure of the nests
        resources['membership_in_nests'] = {0: #            nest 1        nest 2
                                                array([[[0,0,0,1,1,1], [1,1,1,0,0,0]],  # agent 1
                                                       [[1,0,0,0,1,1], [0,1,1,1,0,0]]])}# agent 2
        result = nl_probabilities().run(utilities, resources=resources)

        # check the second agent
        nom1 = exp(array([0.3,  5.3,  0])/0.5)
        nom2 = exp(array([ 1.9, 4.8,  9.1])/0.8)
        denom1 = nom1.sum()
        denom2 = nom2.sum()
        corr_nom1 = array([exp(0.3/0.5), exp(5.3/0.5)/0.02, exp(0)/0.02])
        logsum1 = log(corr_nom1.sum())
        logsum2 = log(denom2/0.05)
        nomm1 = exp(0.5*logsum1)
        nomm2 = exp(0.8*logsum2)
        denomm = nomm1+nomm2
        should_be = array([nom1[0]/denom1 * nomm1/denomm, nom2[0]/denom2 * nomm2/denomm, nom2[1]/denom2 * nomm2/denomm,
                    nom2[2]/denom2 * nomm2/denomm, nom1[1]/denom1 * nomm1/denomm, nom1[2]/denom1 * nomm1/denomm])
        self.assertEqual(ma.allclose(result[1,:], should_be, atol=min(1e-8, should_be.min()), rtol=1e-4), True)
        
if __name__ == '__main__':
    opus_unittest.main()
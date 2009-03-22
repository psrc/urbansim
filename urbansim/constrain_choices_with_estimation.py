# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import ndarray, arange, array, reshape, zeros, where, repeat
from numpy import ma
from scipy.ndimage import sum as ndimage_sum
from opus_core.misc import unique_values
from urbansim.lottery_choices import lottery_choices
from opus_core.logger import logger

class constrain_choices(object):
    def run(self, probability, resources=None):
        """ Compute choices according to given probability -- Constrain Location Choice procedure.
        'probability' is a 2D numpy array (nobservation x nequations).
        The returned value is a 1D array of choice indices [0, nequations-1] of the length nobservations).
        The argument 'resources' must contain an entry 'capacity'. It is 1D array whose number of elements
        corresponds to the number of choices. 
        Optional entry 'index' (1D or 2D array) gives indices of the choices.
        """
        if probability.ndim < 2:
            raise StandardError, "Argument 'probability' must be a 2D numpy array."
            
        resources.check_obligatory_keys(["capacity"])
        supply = resources["capacity"]
        if not isinstance(supply, ndarray):
            supply = array(supply)
        nsupply = supply.size
#        logger.log_status('Supply.shape:',supply.shape)
#        logger.log_status('supply.sum:', supply.sum())
        max_iter = resources.get("max_iterations", None)
        if max_iter == None:
            max_iter = 100 # default
        
        
        index = resources.get("index", None)
        if index == None:
            index = arange(nsupply)
#        logger.log_status('index.shape:',index.shape)

        neqs = probability.shape[1]
        nobs = probability.shape[0]

        if supply.sum < nobs:
            raise StandardError, "Aggregate Supply Must be Greater than Aggregate Demand."


        if index.ndim <= 1:
            index = repeat(reshape(index, (1,index.shape[0])), nobs)        
        resources.merge({"index":index})
#        logger.log_status('index.shape:',index.shape)


        flat_index = index.ravel()
        unique_index = unique_values(flat_index)
#        logger.log_status('flat_index.shape:',flat_index.shape)
#        logger.log_status('unique_index.shape',unique_index.shape)
#        logger.log_status(unique_index)
        l = flat_index + 1
        demand = array(ndimage_sum(probability.ravel(), labels=l, index=arange(nsupply)+1))
#        logger.log_status('demand.shape:',demand.shape)
#        logger.log_status('demand.sum:', demand.sum())
#        logger.log_status('probability.sum:',probability.sum())
        #initial calculations
        
        sdratio = ma.filled(supply/ma.masked_where(demand==0, demand),1.0)
#        logger.log_status('sdratio.shape:',sdratio.shape)
        constrained_locations = where(sdratio<1,1,0)
        unconstrained_locations = 1-constrained_locations
        
        # Compute the iteration zero omegas
        
        sdratio_matrix = sdratio[index]
        constrained_locations_matrix = constrained_locations[index]
        unconstrained_locations_matrix = unconstrained_locations[index]
        prob_sum = 1-(probability*constrained_locations_matrix).sum(axis=1)
        omega = (1-(probability*constrained_locations_matrix*sdratio_matrix).sum(axis=1))/ \
                ma.masked_where(prob_sum ==0, prob_sum)
        pi = sdratio_matrix / ma.resize(omega, (nobs,1)) * constrained_locations_matrix + unconstrained_locations_matrix
        average_omega = ma.filled((ma.resize(omega,(nobs,1))*probability).sum(axis=0)/\
                      ma.masked_where(demand[index]==0, demand[index]),0.0)
        number_constrained_locations=zeros((max_iter,))
            # Iterative Constrained Location Procedure
        for i in range(max_iter):
            logger.log_status('Iteration ',i+1, 'Average Omega:',average_omega[0:4])
            # Recompute the constrained locations using iteration zero value of Omega
            constrained_locations_matrix = where(supply[index]<(average_omega*demand[index]),1,0)
            unconstrained_locations_matrix = 1-constrained_locations_matrix
            # Update values of Omega using new Constrained Locations
            prob_sum = 1-(probability*constrained_locations_matrix).sum(axis=1)
            omega = (1-(probability*constrained_locations_matrix*sdratio_matrix).sum(axis=1))/\
                    ma.masked_where(prob_sum ==0, prob_sum)
#            pi = sdratio_matrix / ma.resize(omega, (nobs,1)) * constrained_locations_matrix + unconstrained_locations_matrix       
#            logger.log_status('sdratio_matrix',sdratio_matrix.shape)
#            logger.log_status('constrained_locations_matrix',constrained_locations_matrix.shape)
#            logger.log_status('omega',omega.shape)
#            logger.log_status('unconstrained_locations_matrix',unconstrained_locations_matrix.shape)
#            pi_ta = (sdratio_matrix*constrained_locations_matrix)
#            logger.log_status('pi+ta',pi_ta.shape)
#            pi_tb = ma.resize(omega,(nobs,neqs))*unconstrained_locations_matrix
#            logger.log_status('pi_tb',pi_tb.shape)
            pi_t = (sdratio_matrix*constrained_locations_matrix)+ma.resize(omega,(nobs,neqs))*unconstrained_locations_matrix
#            logger.log_status('pi_tilde:',pi_t.shape)
            # Update the values of average Omegas per alternative
            average_omega = ma.filled((ma.resize(omega,(nobs,1))*probability).sum(axis=0)/
                          ma.masked_where(demand[index]==0, demand[index]),0.0)
            number_constrained_locations[i]= constrained_locations_matrix.sum()
            # Test for Convergence and if Reached, Exit
            if i > 0:
                if number_constrained_locations[i] == number_constrained_locations[i-1]:
                    break
          
        # update probabilities
#        new_probability = ma.filled(probability*ma.resize(omega,(nobs,1))*pi,0.0)
        new_probability = ma.filled(probability*pi_t,0.0)
        choices = lottery_choices().run(new_probability, resources)
        return choices
        
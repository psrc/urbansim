# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
from numpy import ndarray, arange, array, reshape, zeros, where, repeat, logical_and
from numpy import ma
from opus_core.ndimage import sum as ndimage_sum
from opus_core.logger import logger
from opus_core.mnl_probabilities import mnl_probabilities
from opus_core.probabilities import Probabilities

class constrain_probabilities(Probabilities):
    def run(self, utilities, resources=None):
        """ Compute choices according to given probability -- Constrain Location Choice procedure.
        'probability' is a 2D numpy array (nobservation x nequations).
        The returned value is a 1D array of choice indices [0, nequations-1] of the length nobservations).
        The argument 'resources' must contain an entry 'capacity'. It is 1D array whose number of elements
        corresponds to the number of choices.
        Optional entry 'index' (1D or 2D array) gives indices of the choices.
        """
        probability = mnl_probabilities().compute(utilities,resources)

        if probability.ndim < 2:
            raise StandardError, "Argument 'probability' must be a 2D numpy array."

        resources.check_obligatory_keys(["capacity"])

        #supply = self.compute_supply(resources)
        supply = resources["capacity"]

        if not isinstance(supply, ndarray):
            supply = array(supply)
        nsupply = supply.size

        max_iter = resources.get("max_iterations", None)
        if max_iter == None:
            max_iter = 100 # default

        index = resources.get("index", None)
        if index == None:
            index = arange(nsupply)

        neqs = probability.shape[1]
        nobs = probability.shape[0]

        if index.ndim <= 1:
            index = repeat(reshape(index, (1,index.shape[0])), nobs)
        resources.merge({"index":index})

        demand = self.get_demand(index, probability, nsupply)

        #initial calculations
        sdratio = ma.filled(supply/ma.masked_where(demand==0, demand),2.0)
        constrained_locations = logical_and(sdratio<1,demand-supply>0.1).astype("int8")
        unconstrained_locations = 1-constrained_locations
        excess_demand = (demand-supply)*constrained_locations
        global_excess_demand = excess_demand.sum()

        # Compute the iteration zero omegas

        sdratio_matrix = sdratio[index]
        constrained_locations_matrix = constrained_locations[index]
# Would like to include following print statements in debug printing
#        logger.log_status('Total demand:',demand.sum())
#        logger.log_status('Total supply:',supply.sum())
        logger.log_status('Global excess demand:',global_excess_demand)
#        logger.log_status('Constrained locations:',constrained_locations.sum())
        unconstrained_locations_matrix = unconstrained_locations[index]

        omega = self.get_omega(probability, constrained_locations_matrix, unconstrained_locations_matrix, sdratio_matrix)

# Debug print statements
#        logger.log_status('Minimum omega',minimum(omega))
#        logger.log_status('Maximum omega',maximum(omega))
#        logger.log_status('Median omega',median(omega))
#        logger.log_status('Omega < 0',(where(omega<0,1,0)).sum())
#        logger.log_status('Omega < 1',(where(omega<1,1,0)).sum())
#        logger.log_status('Omega > 30',(where(omega>30,1,0)).sum())
#        logger.log_status('Omega > 100',(where(omega>100,1,0)).sum())
#        logger.log_status('Omega histogram:',histogram(omega,0,30,30))
#        logger.log_status('Excess demand max:',maximum(excess_demand))
#        logger.log_status('Excess demand 0-1000:',histogram(excess_demand,0,1000,20))
#        logger.log_status('Excess demand 0-10:',histogram(excess_demand,0,10,20))

        pi = self.get_pi(sdratio_matrix, omega, constrained_locations_matrix, unconstrained_locations_matrix, nobs)

        average_omega = self.get_average_omega(omega, probability, index, nsupply, nobs, demand)


#        logger.log_status('Total demand:',new_demand.sum())
#        logger.log_status('Excess demand:',excess_demand)

        number_constrained_locations=zeros((max_iter,))
        # Iterative Constrained Location Procedure
        for i in range(max_iter):
            logger.log_status()
            logger.log_status('Constrained location choice iteration ',i+1)
            # Recompute the constrained locations using preceding iteration value of Omega
            constrained_locations = where((average_omega*demand-supply>0.1),1,0)
            unconstrained_locations = 1-constrained_locations
            constrained_locations_matrix = constrained_locations[index]
            unconstrained_locations_matrix = unconstrained_locations[index]
#            logger.log_status('supply.shape,average_omega.shape,demand.shape',supply.shape,average_omega.shape,demand.shape)
#            logger.log_status('constrained_locations_matrix',constrained_locations_matrix)
#            logger.log_status('constrained_locations_matrix.shape',constrained_locations_matrix.shape)
#            logger.log_status('unconstrained_locations_matrix',unconstrained_locations_matrix)
            # Update values of Omega using new Constrained Locations
            prob_sum = 1-(probability*constrained_locations_matrix).sum(axis=1)
            prob_sum = where(prob_sum==0,-1,prob_sum)
            omega = (1-(probability*constrained_locations_matrix*sdratio_matrix).sum()(axis=1))/prob_sum
            omega = where(omega>5,5,omega)
            omega = where(omega<.5,5,omega)
            omega = where(prob_sum<0,5,omega)
            pi = sdratio_matrix / ma.resize(omega, (nobs,1)) * constrained_locations_matrix + unconstrained_locations_matrix
            # Update the values of average Omegas per alternative
            omega_prob = ma.filled(ma.resize(omega,(nobs,1)), 1.0)*probability
            average_omega_num = array(ndimage_sum(omega_prob, labels=index+1, index=arange(nsupply)+1))

            average_omega = ma.filled(average_omega_num/
                      ma.masked_where(demand==0, demand), 0.0)

            number_constrained_locations[i] = constrained_locations.sum()
            new_probability = ma.filled(probability*ma.resize(omega,(nobs,1))*pi,0.0)
            new_demand = self.get_demand(index, new_probability, nsupply)
            excess_demand = (new_demand-supply)*constrained_locations
            global_excess_demand = excess_demand.sum()
#            logger.log_status('Total demand:',new_demand.sum())
            logger.log_status('Global excess demand:',global_excess_demand)
#            logger.log_status('Constrained locations:', number_constrained_locations[i])
#            logger.log_status('Minimum omega',minimum(omega))
#            logger.log_status('Maximum omega',maximum(omega))
#            logger.log_status('Median omega',median(omega))
#            logger.log_status('Omega < 0',(where(omega<0,1,0)).sum())
#            logger.log_status('Omega < 1',(where(omega<1,1,0)).sum())
#            logger.log_status('Omega > 30',(where(omega>30,1,0)).sum())
#            logger.log_status('Omega > 100',(where(omega>100,1,0)).sum())
#            logger.log_status('Omega histogram:',histogram(omega,0,30,30))
#            logger.log_status('Excess demand max:',maximum(excess_demand))
#            logger.log_status('Excess demand 0-5:',histogram(excess_demand,0,5,20))
#            logger.log_status('Excess demand 0-1:',histogram(excess_demand,0,1,20))
            # Test for Convergence and if Reached, Exit
            if i > 0:
                if number_constrained_locations[i] == number_constrained_locations[i-1]:
                    logger.log_status()
                    logger.log_status('Constrained choices converged.')
                    break

        # update probabilities
        new_probability = ma.filled(probability*ma.resize(omega,(nobs,1))*pi,0.0)
        return new_probability

#    def compute_supply(self,resources):
#        return resources["capacity"]

    def get_demand(self, index, probability, nsupply):
        flat_index = index.ravel()
        l = flat_index + 1
        demand = array(ndimage_sum(probability.ravel(), labels=l, index=arange(nsupply)+1))
        return demand

    def get_omega(self, probability, constrained_locations_matrix, unconstrained_locations_matrix, sdratio_matrix):

        prob_sum = 1-(probability*constrained_locations_matrix).sum(axis=1)

        # The recoding of prob_sum and omega are to handle extreme values of omega and zero divide problems
        # A complete solution involves stratifying the choice set in the initialization to ensure that
        # there are always a mixture of constrained and unconstrained alternatives in each choice set.

        prob_sum = where(prob_sum==0,-1,prob_sum)
        omega = (1-(probability*constrained_locations_matrix*sdratio_matrix).sum(axis=1))/prob_sum

#        omega_g5 = sum(where(omega>5,1,0))
#        omega_l0_5 = sum(where(omega<.5,1,0)
#        omega_l_0 = sum(where(prob_sum<0,1,0))
#        print 'omega_g5',omega_g5
#        print 'omega_l0_5',omega_l0_5
#        print 'omega_l0',omega_l0

        omega = where(omega>5,5,omega)
        omega = where(omega<.5,5,omega)
        omega = where(prob_sum<0,5,omega)

        return omega

    def get_pi(self, sdratio_matrix, omega, constrained_locations_matrix, unconstrained_locations_matrix, nobs):
        pi = sdratio_matrix / ma.resize(omega, (nobs,1)) * constrained_locations_matrix + unconstrained_locations_matrix
        return pi

    def get_average_omega(self, omega, probability, index, nsupply, nobs, demand):
        omega_prob = ma.filled(ma.resize(omega,(nobs,1))*probability,0.0)
        average_omega_nom = array(ndimage_sum(omega_prob, labels=index+1, index=arange(nsupply)+1))

        average_omega = ma.filled(average_omega_nom / ma.masked_where(demand==0, demand), 0.0)
        return average_omega
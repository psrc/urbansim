# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.logger import logger
from numpy import ndarray,float32
from numpy import where,reshape
from numpy import concatenate,logical_and, ones, any, arange, repeat
from numpy import array, ma
from opus_core.ndimage import standard_deviation
from numpy.mlab import mean,median,min
from opus_core.variables.variable import ln
from opus_core.bhhh_mnl_estimation import bhhh_mnl_estimation
from opus_core.upc_factory import UPCFactory
from opus_core.estimation_procedure import EstimationProcedure

class constrain_estimation_bhhh(EstimationProcedure):
    def run(self, data, upc_sequence, resources=None):
        CLOSE = 0.01

        self.mnl_probabilities=upc_sequence.probability_class
        self.bhhh_estimation = bhhh_mnl_estimation()

        modified_upc_sequence = UPCFactory().get_model(
            utilities=None, probabilities="opus_core.mnl_probabilities", choices=None)
        modified_upc_sequence.utility_class = upc_sequence.utility_class

        result = self.bhhh_estimation.run(data, modified_upc_sequence, resources)
        probability = modified_upc_sequence.get_probabilities()
        probability_0 = probability

        resources.check_obligatory_keys(["capacity"])

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

        # WARNING: THE SCALING OF DEMAND IS HARD CODED AND NEEDS TO BE MADE AN ARGUMENT
        # scale demand to represent 100% from a 0.2% sample
        demand = self.mnl_probabilities.get_demand(index, probability, nsupply)*50

        #initial calculations
        sdratio = ma.filled(supply/ma.masked_where(demand==0, demand),2.0)
        sdratio = _round(sdratio, 1.0, atol=CLOSE)
        constrained_locations = logical_and(sdratio<1.0,demand-supply>CLOSE).astype("int8")
        unconstrained_locations = 1-constrained_locations
        excess_demand = (demand-supply)*constrained_locations
        global_excess_demand = excess_demand.sum()

        sdratio_matrix = sdratio[index]
        constrained_locations_matrix = constrained_locations[index]
        constrained_ex_ante = constrained_locations_matrix
# Would like to include following print statements in debug printing
#        logger.log_status('Total demand:',demand.sum())
#        logger.log_status('Total supply:',supply.sum())
        logger.log_status('Global excess demand:',global_excess_demand)
#        logger.log_status('Constrained locations:',constrained_locations.sum())
        unconstrained_locations_matrix = unconstrained_locations[index]

#        omega = ones(nobs,type=float32)
#        pi = self.constrain_probabilities.get_pi(sdratio_matrix, omega, constrained_locations_matrix, unconstrained_locations_matrix, nobs)

        omega = self.mnl_probabilities.get_omega(probability, constrained_locations_matrix, unconstrained_locations_matrix, sdratio_matrix)
        omega = _round(omega, 1.0, CLOSE)

        print 'Num of constrainted locations: ', constrained_locations.sum()
        print 'Num of unconstrainted locations: ', unconstrained_locations.sum()
        print 'Min Ex Ante Constraints:',min(constrained_ex_ante.sum(axis=1))
        print 'Max Ex Ante Constraints:',max(constrained_ex_ante.sum(axis=1))
        #print 'Omega shape',omega.shape
        #print 'Omega histogram',histogram(omega,0,4,40)
        print 'Minimum Omega',min(omega)
        print 'Maximum Omega',max(omega)
        print 'Mean Omega:',mean(omega)
        print 'Median Omega:',median(omega)
        print 'Sum Omega:',omega.sum()
        print 'Standard Deviation Omega:',standard_deviation(omega)
        print 'Count of Negative Omega',(where(omega<0,1,0).sum())
        print 'Count of Omega < 1',(where(omega<1,1,0).sum())
        print 'Count of Omega > 2',(where(omega>2,1,0).sum())
        print 'Count of Omega > 4',(where(omega>4,1,0).sum())

        average_omega = self.mnl_probabilities.get_average_omega(omega, probability, index, nsupply, nobs, demand)
        average_omega=_round(average_omega, 1.0, CLOSE)

        coef_names = resources.get("coefficient_names", None)

        if coef_names is not None:
            coef_names = array(coef_names.tolist()+["ln_pi"])
            resources.merge({"coefficient_names":coef_names})

        data=concatenate((data,ones((nobs,neqs,1),dtype=float32)), axis=2)

        prev_omega = omega
        prev_constrained_locations_matrix = constrained_locations_matrix

        for i in range(max_iter):
            print
            print 'Iteration',i
            pi = self.mnl_probabilities.get_pi(sdratio_matrix, omega, constrained_locations_matrix, unconstrained_locations_matrix, nobs)
            #print 'pi shape',pi.shape
            #print 'data shape', data.shape
            #print 'min_pi',min(pi,axis=1)
            #print 'max_pi',max(pi,axis=1)
            #print 'min_data',min(data,axis=1)
            #print 'max_data',max(data,axis=1)
            data[:,:,-1] = ln(pi)
            #data = concatenate((data,(pi[:,:,newaxis])),axis=-1)

            #print 'data shape after contatenating pi', data.shape
            result = self.bhhh_estimation.run(data, modified_upc_sequence, resources)
            #print
            #print 'result',result
            probability = modified_upc_sequence.get_probabilities()
            prob_hat = ma.filled(probability / pi, 0.0)


            # HARD CODED
            # scale new_demand from 0.2% to 100%
            demand_new = self.mnl_probabilities.get_demand(index, prob_hat, nsupply)*50
            ##update supply-demand ratio
            sdratio = ma.filled(supply/ma.masked_where(demand_new==0, demand_new),2.0)
            sdratio = _round(sdratio, 1.0, CLOSE)
            sdratio_matrix = sdratio[index]

            constrained_locations = where(((average_omega*demand_new - supply) > CLOSE),1,0)
            unconstrained_locations = 1-constrained_locations
            constrained_locations_matrix = constrained_locations[index]
            unconstrained_locations_matrix = unconstrained_locations[index]
            constrained_ex_post = constrained_locations_matrix
            constrained_ex_post_not_ex_ante = where((constrained_ex_post - constrained_ex_ante)==1,1,0)
            constrained_ex_ante_not_ex_post = where((constrained_ex_post - constrained_ex_ante)==-1,1,0)

            #Assumption 5: if j belongs to constrained ex post and unconstrained ex ante, then p^i_j <= D_j / S_j
            print 'Number of individual violating Assumption 5: ', where((probability > 1 / sdratio_matrix)*constrained_ex_post_not_ex_ante)[0].size

            #Assumption 6: pi of constrained locations should be less than 1
            print 'Number of individual violating Assumption 6: ', where((probability * constrained_ex_post).sum(axis=1) >
                                                                         (prob_hat * constrained_ex_post).sum(axis=1))[0].size
            ##OR ?
            #print 'Assumption 6: ', where(pi[where(constrained_locations_matrix)] > 1)[0].size

            print 'number of constrainted locations: ', constrained_locations.sum()
            print 'number of unconstrainted locations: ', unconstrained_locations.sum()
            print 'Min Ex Post Constraints:',min(constrained_ex_post.sum(axis=1))
            print 'Max Ex Post Constraints:',max(constrained_ex_post.sum(axis=1))
            print 'At Least 1 Constrained Ex Ante Not Ex Post*:',where(constrained_ex_ante_not_ex_post.sum(axis=1))[0].size
            print 'At Least 1 Constrained Ex Post Not Ex Ante:',where(constrained_ex_post_not_ex_ante.sum(axis=1))[0].size

            omega = self.mnl_probabilities.get_omega(prob_hat, constrained_locations_matrix, unconstrained_locations_matrix, sdratio_matrix)
            omega = _round(omega, 1.0, CLOSE)
            #print 'Omega histogram',histogram(omega,0,4,40)
            print 'Minimum Omega',min(omega)
            print 'Maximum Omega',max(omega)
            print 'Mean Omega:',mean(omega)
            print 'Median Omega:',median(omega)
            print 'Sum Omega:',omega.sum()
            print 'Standard Deviation Omega:',standard_deviation(omega)
            print 'Count of Negative Omega',(where(omega<0,1,0).sum())
            print 'Count of Omega < 1: ',(where(omega<1,1,0).sum())
            print 'Count of Omega > 2: ',(where(omega>2,1,0).sum())
            print 'Count of Omega > 4: ',(where(omega>4,1,0).sum())

            average_omega = self.mnl_probabilities.get_average_omega(omega, prob_hat, index, nsupply, nobs, demand_new)
            average_omega = _round(average_omega, 1.0, CLOSE)
            excess_demand = (demand_new-supply)*constrained_locations
            global_excess_demand = excess_demand.sum()
            #print 'Omega [i], [i-1]',prev_omega, omega,
            #print 'Constrained locations [i], [i-1]',constrained_locations_matrix, prev_constrained_locations_matrix
            print 'Global Excess Demand',global_excess_demand
            if ma.allclose(omega, prev_omega, atol=1e-3) or not any(constrained_locations_matrix - prev_constrained_ex_ante):
                print 'omega or constrained ex post unchanged: Convergence criterion achieved'
                break

            #if global_excess_demand < 1:
                #print 'Global excess demand < 1: Convergence criterion achieved'
                #break

        return result

def _round(x,  y, rtol=1e-5, atol=1e-8):
    return where(abs(x - y) <= atol + rtol * abs(y), y, x)
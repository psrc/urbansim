# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.logger import logger
from numpy import zeros,float32,where,reshape,newaxis,absolute
from numpy import concatenate, ones, any, arange, repeat
from numpy import array, ma, mean, median, min
from opus_core.ndimage import standard_deviation
from opus_core.misc import corr, unique, safe_array_divide
from opus_core.session_configuration import SessionConfiguration
from opus_core.variables.variable import ln
from opus_core.bhhh_mnl_estimation import bhhh_mnl_estimation
from opus_core.upc_factory import UPCFactory
from opus_core.sampling_toolbox import normalize
from opus_core.estimation_procedure import EstimationProcedure
from gc import collect

class constrain_estimation_bhhh_two_loops(EstimationProcedure):

    def run(self, data, upc_sequence, resources=None):

        self.mnl_probabilities=upc_sequence.probability_class
        self.bhhh_estimation = bhhh_mnl_estimation()

        modified_upc_sequence = UPCFactory().get_model(
            utilities=None, probabilities="opus_core.mnl_probabilities", choices=None)
        modified_upc_sequence.utility_class = upc_sequence.utility_class

        N, neqs, V = data.shape

        max_iter = resources.get("max_iterations", 100)  # default
        sc = SessionConfiguration()
        dataset_pool = sc.get_dataset_pool()
        sample_rate = dataset_pool.get_dataset("sample_rate")
        
        CLOSE = sc["CLOSE"]
        info_filename = sc["info_file"]
        info_filename = os.path.join('.', info_filename)
        info_file = open(info_filename, "a")
        constraint_dict = {1:'constrained', 0:'unconstrained'}
        swing_cases_fix = 0  #set swing alternatives to constrained (1) or unconstrained (0)
        prob_correlation = None
        
        choice_set = resources['_model_'].choice_set
        J = choice_set.size()
        alt_id = choice_set.get_id_attribute()
        movers = choice_set.get_attribute('movers')

        resources.check_obligatory_keys(["capacity_string"])
        supply = choice_set.get_attribute(resources["capacity_string"])

        index = resources.get("index", None)
        if index is None: # no sampling case, alternative set is the full choice_set
            index = arange(J)
        if index.ndim <= 1:
            index = repeat(index[newaxis,:], N, axis=0)

        if resources.get('aggregate_to_dataset', None):
            aggregate_dataset = dataset_pool.get_dataset(resources.get('aggregate_to_dataset'))
            choice_set_aggregate_id = choice_set.get_attribute(aggregate_dataset.get_id_name()[0])
            index = aggregate_dataset.get_id_index(choice_set_aggregate_id[index].ravel()).reshape(index.shape)

            supply = aggregate_dataset.get_attribute(resources["capacity_string"])
            J = aggregate_dataset.size()

            movers = aggregate_dataset.get_attribute("movers")

        demand_history = movers[:, newaxis]
        resources.merge({"index":index})
        
        pi = ones(index.shape, dtype=float32)  #initialize pi
        #average_omega = ones(J,dtype=float32)  #initialize average_omega
        logger.start_block('Outer Loop')
        for i in range(max_iter):
            logger.log_status('Outer Loop Iteration %s' % i)

            result = self.bhhh_estimation.run(data, modified_upc_sequence, resources)
            del self.bhhh_estimation; collect()
            self.bhhh_estimation = bhhh_mnl_estimation()

            probability = modified_upc_sequence.get_probabilities()
            if data.shape[2] == V:  #insert a placeholder for ln(pi) in data
                data = concatenate((data,ones((N,neqs,1),dtype=float32)), axis=2)
                coef_names = resources.get("coefficient_names")
                coef_names = concatenate( (coef_names, array(["ln_pi"])) )
                resources.merge({"coefficient_names":coef_names})
            else:
                beta_ln_pi = result['estimators'][where(coef_names == 'ln_pi')][0]
                logger.log_status("mu = 1/%s = %s" % (beta_ln_pi, 1/beta_ln_pi))
                
                prob_hat = safe_array_divide(probability, pi ** beta_ln_pi)
                #prob_hat = safe_array_divide(probability, pi)
                prob_hat_sum = prob_hat.sum(axis=1, dtype=float32)
                if not ma.allclose(prob_hat_sum, 1.0):
                    logger.log_status("probability doesn't sum up to 1, with minimum %s, and maximum %s" %
                                      (prob_hat_sum.min(), prob_hat_sum.max()))
                    
                    probability = normalize(prob_hat)

            demand = self.mnl_probabilities.get_demand(index, probability, J) * 1 / sample_rate
            demand_history = concatenate((demand_history,
                                          demand[:, newaxis]),
                                          axis=1)

            sdratio = safe_array_divide(supply, demand, return_value_if_denominator_is_zero=2.0)
            sdratio_matrix = sdratio[index]
            ## debug info
            from numpy import histogram 
            from opus_core.misc import unique
            cc = histogram(index.ravel(), unique(index.ravel()))[0]
            logger.log_status( "=================================================================")
            logger.log_status( "Probability min: %s, max: %s" % (probability.min(), probability.max()) )
            logger.log_status( "Demand min: %s, max: %s" % (demand.min(), demand.max()) )
            logger.log_status( "sdratio min: %s, max: %s" % (sdratio.min(), sdratio.max()) )
            logger.log_status( "demand[sdratio==sdratio.min()]=%s" % demand[sdratio==sdratio.min()] )
            logger.log_status( "demand[sdratio==sdratio.max()]=%s" % demand[sdratio==sdratio.max()] )
            logger.log_status( "Counts of unique submarkets in alternatives min: %s, max: %s" % (cc.min(), cc.max()) )
            logger.log_status( "=================================================================")

            constrained_locations_matrix, omega, info = self.inner_loop(supply, demand, probability,
                                                                        index, sdratio_matrix,
                                                                        J, max_iteration=max_iter)

            inner_iterations, constrained_locations_history, swing_index, average_omega_history = info
    
            for idx in swing_index:
                logger.log_status("swinging alt with id %s set to %s" % (alt_id[idx], constraint_dict[swing_cases_fix]))
                constrained_locations_matrix[index==idx] = swing_cases_fix
    
            if swing_index.size > 0:    
                info_file.write("swing of constraints found with id %s \n" % alt_id[swing_index])
                info_file.write("outer_iteration, %i, " % i + ", ".join([str(i)]*(len(inner_iterations))) + "\n")
                info_file.write("inner_iteration, , " + ", ".join(inner_iterations) + "\n")
                info_file.write("id, sdratio, " + ", ".join(["avg_omega"]*len(inner_iterations)) + "\n")
                for idx in swing_index:
                    line = str(alt_id[idx]) + ','
                    line += str(sdratio[idx]) + ','
                    line += ",".join([str(x) for x in average_omega_history[idx,]])
                    line += "\n"
                    info_file.write(line)
    
                info_file.write("\n")
                info_file.flush()

            outer_iterations = [str(i)] * len(inner_iterations)
            prob_min = [str(probability.min())] * len(inner_iterations)
            prob_max = [str(probability.max())] * len(inner_iterations)

            pi_new = self.mnl_probabilities.get_pi(sdratio_matrix, omega, constrained_locations_matrix)

            data[:,:,-1] = ln(pi_new)
            #diagnostic output
            
            if not ma.allclose(pi, pi_new, atol=CLOSE):
                if i > 0:  #don't print this for the first iteration
                    logger.log_status("min of abs(pi(l+1) - pi(l)): %s" % absolute(pi_new - pi).min())
                    logger.log_status("max of abs(pi(l+1) - pi(l)): %s" % absolute(pi_new - pi).max())
                    logger.log_status("mean of pi(l+1) - pi(l): %s" % (pi_new - pi).mean())
                    logger.log_status('Standard Deviation pi(l+1) - pi(l): %s' % standard_deviation(pi_new - pi))
                    logger.log_status('correlation of pi(l+1) and pi(l): %s' % corr(pi_new.ravel(), pi.ravel())[0,1])

                pi = pi_new
                probability_old = probability   # keep probability of the previous loop, for statistics computation only    
            else:   #convergence criterion achieved, quiting outer loop
                logger.log_status("pi(l) == pi(l+1): Convergence criterion achieved")
    
                info_file.write("\nConstrained Locations History:\n")
                info_file.write("outer_iteration," + ",".join(outer_iterations) + "\n")
                info_file.write("inner_iteration," + ",".join(inner_iterations) + "\n")
                info_file.write("minimum_probability," + ",".join(prob_min) + "\n")
                info_file.write("maximum_probability," + ",".join(prob_max) + "\n")
                for row in range(J):
                    line = [str(x) for x in constrained_locations_history[row,]]
                    info_file.write(str(alt_id[row]) + "," + ",".join(line) + "\n")

                info_file.flush()

                info_file.write("\nDemand History:\n")
                i_str = [str(x) for x in range(i)]
                info_file.write("outer_iteration, (movers)," + ",".join(i_str) + "\n")
                #info_file.write(", ,\n")
                for row in range(J):
                    line = [str(x) for x in demand_history[row,]]
                    info_file.write(str(alt_id[row]) + "," + ",".join(line) + "\n")

                demand_history_info_criteria = [500, 100, 50, 20]
                for criterion in demand_history_info_criteria:
                    com_rows_index = where(movers <= criterion)[0]
                    info_file.write("\nDemand History for alternatives with less than or equal to %s movers in 1998:\n" % criterion)
                    i_str = [str(x) for x in range(i)]
                    info_file.write("outer_iteration, (movers)," + ",".join(i_str) + "\n")
                    #info_file.write(", movers,\n")
                    for row in com_rows_index:
                        line = [str(x) for x in demand_history[row,]]
                        info_file.write(str(alt_id[row]) + "," + ",".join(line) + "\n")

                #import pdb; pdb.set_trace()
                #export prob correlation history
                correlation_indices, prob_correlation = self.compute_prob_correlation(probability_old, probability, prob_hat, index, resources)

                info_file.write("\nCorrelation of Probabilities:\n")
                c_name = ['corr(p_ij p~_ij)', 'corr(p_ij p^_ij)', 'corr(p_ij dummy)', 'corr(p~_ij p^_ij)', 'corr(p~_ij dummy)', 'corr(p^_ij dummy)']

                info_file.write("com_id, " + ",".join(c_name) + "\n")

                #info_file.write(", ,\n")
                for row in range(correlation_indices.size):
                    line = [str(x) for x in prob_correlation[row,]]
                    info_file.write(str(alt_id[correlation_indices[row]]) + "," + ",".join(line) + "\n")

                info_file.close()

                result['pi'] = pi
                return result

        logger.end_block()
        try:info_file.close()
        except:pass

        raise RuntimeError, "max iteration reached without convergence."

    def inner_loop(self, supply, demand, probability, index, sdratio_matrix, J,
                   max_iteration=100):
        #vacancy_rate = SessionConfiguration().get_dataset_from_pool("vacancy_rate")
        CLOSE = SessionConfiguration()["CLOSE"]

        average_omega = ones(J, dtype=float32)
        inner_iterations=None; constrained_locations_history = None
        swing_index=array([]); average_omega_history=average_omega[:, newaxis];
        N = probability.shape[0]
        constrained_ex_ante = zeros(probability.shape) - 1
        logger.start_block('Inner Loop')

        try:
            for i in range(1, max_iteration+1):
                logger.log_status('Inner Loop Iteration %s' % i)
    
                #initial calculations
                constrained_locations = where(((average_omega * demand - supply) > CLOSE),1,0)    
                constrained_locations_matrix = constrained_locations[index]
    
                omega = self.mnl_probabilities.get_omega(probability, constrained_locations_matrix, sdratio_matrix)
                #omega = _round(omega, 1.0, CLOSE)
    
                logger.log_status('Num of constrainted locations: %s' % constrained_locations.sum())
                logger.log_status('Num of unconstrainted locations: %s' % (constrained_locations.size - constrained_locations.sum()))
                logger.log_status('Min Ex Ante Constraints: %s' % min(constrained_locations_matrix.sum(axis=1)))
                logger.log_status('Max Ex Ante Constraints: %s' % max(constrained_locations_matrix.sum(axis=1)))
                logger.log_status('Minimum Omega: %s' % min(omega))
                logger.log_status('Maximum Omega: %s' % max(omega))
                logger.log_status('Mean Omega: %s' % mean(omega))
                logger.log_status('Median Omega: %s' % median(omega))
                logger.log_status('Sum Omega: %s' % omega.sum())
                logger.log_status('Standard Deviation Omega: %s' % standard_deviation(omega))
                logger.log_status('Count of Negative Omega: %s' % (where(omega<0,1,0)).sum())
                logger.log_status('Count of Omega < 1: %s' % (where(omega<1,1,0)).sum())
                logger.log_status('Count of Omega > 2: %s' % (where(omega>2,1,0)).sum())
                logger.log_status('Count of Omega > 4: %s' % (where(omega>4,1,0)).sum())
    
                average_omega = self.mnl_probabilities.get_average_omega(omega, probability, index, J, demand)
    
                #average_omega=_round(average_omega, 1.0, CLOSE)
                logger.log_status('Minimum average_omega: %s' % min(average_omega))
                logger.log_status('Maximum average_omega: %s' % max(average_omega))
                logger.log_status('Mean average_omega: %s' % mean(average_omega))
                logger.log_status('Median average_omega: %s' % median(average_omega))
                logger.log_status('Sum average_omega: %s' % average_omega.sum())
                logger.log_status('Standard Deviation average_omega: %s' % standard_deviation(average_omega))
    
                logger.log_status(' ')
                if not any(constrained_ex_ante - constrained_locations_matrix):
                    return constrained_locations_matrix, omega, (inner_iterations, constrained_locations_history,swing_index, average_omega_history)
                else:
                    constrained_ex_ante = constrained_locations_matrix
    
                if constrained_locations_history is None:
                    inner_iterations = [str(i)]
                    constrained_locations_history = constrained_locations[:,newaxis]
                else:
                    inner_iterations += [str(i)]
                    constrained_locations_history = concatenate((constrained_locations_history,
                                                                constrained_locations[:, newaxis]),
                                                                axis=1)
                    average_omega_history = concatenate((average_omega_history, average_omega[:, newaxis]), axis=1)
    
                    if i > 2 and ma.allclose(constrained_locations_history[:,i-1], constrained_locations_history[:,i-3]):
                        swing_index = where((constrained_locations_history[:,i-1] - constrained_locations_history[:,i-2]) <> 0)[0]
                        logger.log_warning("swing of constraints found in %s alternatives" % swing_index.size)
                        return constrained_locations_matrix, omega, (inner_iterations, constrained_locations_history,swing_index, average_omega_history)
        finally:
            logger.end_block()
        logger.log_error("max iteration reached without convergence.")
        raise RuntimeError, "max iteration reached without convergence."

    def compute_prob_correlation(self, pij, ptij, phij, index, resources):
        chosen_choice_dummy = resources['chosen_choice']
        indices = unique(index.ravel())
        correlation = None
        for j in indices:
            w = where(index == j)
            pj = pij[w]
            ptj = ptij[w]
            phj = phij[w]
            sj = chosen_choice_dummy[w]
            #import pdb; pdb.set_trace()
            cor = corr(pj, ptj, phj, sj)[([0,0,0,1,1,2],[1,2,3,2,3,3])][newaxis,:] #take the upper triangle
            if correlation is None:
                correlation = cor
            else:
                correlation = concatenate((correlation, cor), axis=0)

        return (indices, correlation)

def _round(x,  y, rtol=1e-5, atol=1e-8):
    return where(absolute(x - y) <= atol + rtol * absolute(y), y, x)

# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.resources import Resources
from opus_core.choice_model import ChoiceModel
from numpy import array, arange, where, ones, concatenate, logical_and, zeros, cumsum, searchsorted
from numpy.random import random, uniform, randint
from opus_core.logger import logger

class HouseholdWorkersInitChoiceModel(ChoiceModel):
    """
    Predicts number of workers in households with newly-created household_id
    """
    model_name = "Household Workers Initialization Choice Model"
    model_short_name = "HWICM"

    def run(self, specification, coefficients, agent_set, agents_index=None, **kwargs):
        hh_to_init_workers = agent_set.compute_variables("_hh_to_init = ((household.workers)==-1)")
        idx_to_init = where(hh_to_init_workers)[0]
        if idx_to_init.size > 0:
            results = ChoiceModel.run(self, specification, coefficients, agent_set, agents_index=idx_to_init, **kwargs)
            agent_set.modify_attribute('workers', results, idx_to_init)
        #Ensure that predicted workers does not exceed # persons who are eligible to work
        workeligible = agent_set.compute_variables('_work_eligible = household.aggregate(person.age>15)')
        agent_set.add_attribute(name='work_eligible', data=agent_set.compute_variables('household.aggregate(person.age>15)'))
        workers_exceeds_eligible = agent_set.compute_variables("_overpredict_workers = ((household.workers) > _work_eligible)")
        idx_excess_workers = where(logical_and(workers_exceeds_eligible,hh_to_init_workers))[0]
        if idx_excess_workers.size > 0:
            agent_set.modify_attribute('workers', workeligible[idx_excess_workers], idx_excess_workers)
        #When a household with 4+ eligible workers is assigned "3+ workers", a more specific number of workers needs to be assigned
        #When household with 4 eligible workers is predicted to have 3+ workers, the household can be assigned 3 workers or 4 workers
        four_eligible_three_predicted = agent_set.compute_variables('_four_eligible_three_predicted = (_work_eligible==4)*((household.workers)==3)')
        idx_four_elig = where(logical_and(four_eligible_three_predicted,hh_to_init_workers))[0]
        if idx_four_elig.size > 0:
            four_numworker_prob = ([.62,.38]) #probabilities from crosstab of base-year workers vs. base-year persons eligible to work
            four_cum_prob = cumsum(four_numworker_prob)
            for hh in idx_four_elig:
                r = uniform(0,1)
                agent_set['workers'][hh] = searchsorted(four_cum_prob, r) + 3
        #When household with 5 eligible workers is predicted to have 3+ workers, the household can be assigned 3, 4, or 5 workers
        five_eligible_three_predicted = agent_set.compute_variables('_five_eligible_three_predicted = (_work_eligible==5)*((household.workers)==3)')
        idx_five_elig = where(logical_and(five_eligible_three_predicted,hh_to_init_workers))[0]
        if idx_five_elig.size > 0:
            five_numworker_prob = ([.44,.33,.23])
            five_cum_prob = cumsum(five_numworker_prob)
            for hh in idx_five_elig:
                r = uniform(0,1)
                agent_set['workers'][hh] = searchsorted(five_cum_prob, r) + 3
        #When household with 6 eligible workers is predicted to have 3+ workers, the household can be assigned 3, 4, 5, or 6 workers
        six_eligible_three_predicted = agent_set.compute_variables('_six_eligible_three_predicted = (_work_eligible==6)*((household.workers)==3)')
        idx_six_elig = where(logical_and(six_eligible_three_predicted,hh_to_init_workers))[0]
        if idx_six_elig.size > 0:
            six_numworker_prob = ([.32,.23,.24,.21])
            six_cum_prob = cumsum(six_numworker_prob)
            for hh in idx_six_elig:
                r = uniform(0,1)
                agent_set['workers'][hh] = searchsorted(six_cum_prob, r) + 3
        #When household with 7+ eligible workers is predicted to have 3+ workers, the household is randomly asssigned a number of workers no less than 3 and no greater than the number of persons eligible to work
        many_eligible_three_predicted = agent_set.compute_variables('_many_eligible_three_predicted = (_work_eligible>6)*((household.workers)==3)')
        idx_many_elig = where(logical_and(many_eligible_three_predicted,hh_to_init_workers))[0]
        if idx_many_elig.size > 0:
            for hh in idx_many_elig:
                agent_set['workers'][hh] = randint(3, ((agent_set['work_eligible'][hh])+1))
        if 'numworker_id' in agent_set.get_primary_attribute_names():
            agent_set.delete_one_attribute('numworker_id')
        agent_set.delete_one_attribute('work_eligible')
# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.rate_based_model import RateBasedModel
from opus_core.logger import logger
from numpy import where, arange, array, logical_and, zeros, ones, cumsum, searchsorted, exp, sqrt
from numpy.random import random, uniform, randint, shuffle

class ChildLeavingHomeModel(RateBasedModel):
    """
    """
    model_name = "Child Leaving Home Model"

    def run(self, person_set, household_set, resources=None):
        person_ds_name, person_id_name = person_set.get_dataset_name(), person_set.get_id_name()[0]
        hh_ds_name, hh_id_name = household_set.get_dataset_name(), household_set.get_id_name()[0]
        person_set.add_attribute(name='much_younger_than_head', data=person_set.compute_variables('(person.age) < ((person.disaggregate(household.age_of_head))-18)'))
        person_set.add_attribute(name='same_race_as_head', data=person_set.compute_variables('(person.race) ==(person.disaggregate(household.aggregate(person.head_of_hh * person.race)))'))
        index = RateBasedModel.run(self, person_set, resources=resources)
        logger.log_status("%s children will be leaving their homes" % (index.size) )

        max_hh_id = household_set.get_attribute(hh_id_name).max() + 1
        new_hh_id = arange(max_hh_id, max_hh_id+index.size)
        person_set.modify_attribute(hh_id_name, new_hh_id, index=index)
        household_set.add_elements({hh_id_name:new_hh_id}, require_all_attributes=False) 

        person_set.delete_one_attribute('much_younger_than_head')
        person_set.delete_one_attribute('same_race_as_head') 

        ##Update the household table's persons attribute
        if 'persons' in household_set.get_primary_attribute_names():
            persons = household_set.compute_variables('_persons = household.number_of_agents(person)')
            household_set.modify_attribute('persons', persons)
        ##Update the household table's children attribute
        if 'children' in household_set.get_primary_attribute_names():
            children = household_set.compute_variables('_children = household.aggregate(person.age<18)')
            household_set.modify_attribute('children', children)
        ##Update the household table's workers attribute
        if 'workers' in household_set.get_primary_attribute_names():
            #init new household_ids with workers = -1.  To be initialized by the household workers initialization model.
            new_household_ids = household_set.compute_variables('(household.household_id > %s)' % (max_hh_id))
            initialize_workers = where(new_household_ids == 1)[0]
            if initialize_workers.size > 0:
                household_set.modify_attribute('workers', array(initialize_workers.size*[-1]), initialize_workers)
        ##Assign "head of the household" status
        if 'head_of_hh' in person_set.get_primary_attribute_names():
            person_set.add_attribute(name='head_score', data=person_set.compute_variables('(person.age)*1.0 + 3.0*(person.education) + exp(-sqrt(sqrt(sqrt(.5*(person.person_id)))))'))
            highest_score = person_set.compute_variables('_high_score = (person.disaggregate(household.aggregate(person.head_score, function=maximum)))*1')
            head_of_hh = person_set.compute_variables('_head_of_hh = (person.head_score == _high_score)*1')
            person_set.modify_attribute('head_of_hh', head_of_hh)
            person_set.delete_one_attribute('head_score')    
        ##Update the age_of_head attribute in the household table to reflect the age of new heads of the household
        if 'age_of_head' in household_set.get_primary_attribute_names():
            age_of_head = household_set.compute_variables('_age_of_head = household.aggregate(person.head_of_hh * person.age)')
            household_set.modify_attribute('age_of_head', age_of_head)
        ##Initialize income of households with newly-assigned household_ids (should be only 1-person male households) as -1
        if 'income' in household_set.get_primary_attribute_names():
            new_household_ids = household_set.compute_variables('(household.household_id > %s)' % (max_hh_id))
            initialize_income = where(new_household_ids == 1)[0]
            if initialize_income.size > 0:
                household_set.modify_attribute('income', array(initialize_income.size*[-1]), initialize_income)
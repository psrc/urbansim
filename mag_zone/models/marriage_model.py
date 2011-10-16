# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.agent_relocation_model import AgentRelocationModel
from opus_core.logger import logger
from numpy import array, zeros, ones, where, logical_and, arange, exp, sqrt, cumsum, searchsorted
from numpy.random import random, uniform
from urbansim.lottery_choices import lottery_choices
from opus_core.resources import Resources

class MarriageEligibilityModel(AgentRelocationModel):
    """
    """
    model_name = "Marriage Eligibility Model"

    def run(self, person_set, household_set, resources=None):
        index = AgentRelocationModel.run(self, person_set, resources=resources)
        logger.log_status("%s persons are in the marriage market." % (index.size) )

        person_ds_name, person_id_name = person_set.get_dataset_name(), person_set.get_id_name()[0]
        hh_ds_name, hh_id_name = household_set.get_dataset_name(), household_set.get_id_name()[0]

        #Flag the pool of individuals that are eligible to get married
        person_set.add_attribute(name='marriage_eligible', data=zeros(person_set.size(), dtype='b'))
        person_set['marriage_eligible'][index] = True

        #Separate the males from the females
        if 'gender' in person_set.get_primary_attribute_names():
            index_eligible_males = where(logical_and(person_set['marriage_eligible'], person_set['gender']==1))[0]
            index_eligible_females = where(logical_and(person_set['marriage_eligible'], person_set['gender']==2))[0]
        if 'sex' in person_set.get_primary_attribute_names():
            index_eligible_males = where(logical_and(person_set['marriage_eligible'], person_set['sex']==1))[0]
            index_eligible_females = where(logical_and(person_set['marriage_eligible'], person_set['sex']==2))[0]
        logger.log_status("There are %s eligible males and %s eligible females." % (index_eligible_males.size,index_eligible_females.size) )
        logger.log_status("%s new households will be formed." % (array([index_eligible_females.size,index_eligible_males.size]).min()))

        max_hh_id = household_set.get_attribute(hh_id_name).max() + 1
        if (index_eligible_males.size > 0) and (index_eligible_females.size > 0):
            #When males>females, females choose mate.  When females>=males, males choose mate.
            if index_eligible_males.size > index_eligible_females.size:
                #Create the new household IDs and assign them to the mate choosers (the mate they choose will take on this same household ID)
                new_hh_id = arange(max_hh_id, max_hh_id+index_eligible_females.size)
                person_set.modify_attribute('household_id', new_hh_id, index=index_eligible_females)
                self.mate_match(index_eligible_females, index_eligible_males, person_set)
            else:
                new_hh_id = arange(max_hh_id, max_hh_id+index_eligible_males.size)
                person_set.modify_attribute('household_id', new_hh_id, index=index_eligible_males)
                self.mate_match(index_eligible_males, index_eligible_females, person_set)
                        
        person_set.delete_one_attribute('marriage_eligible')
        #Remove records from household_set that have no persons left
        persons = household_set.compute_variables("%s.number_of_agents(%s)" % (hh_ds_name, person_ds_name), resources=resources)
        index_hh0persons = where(persons==0)[0]
        if index_hh0persons.size > 0:
            logger.log_status("Removing %s records without %s from %s dataset" % (index_hh0persons.size, person_ds_name, hh_ds_name) )
            household_set.remove_elements(index_hh0persons)

    def mate_match(self, choosers, available_mates, person_set):
        available_mates_age = array([(person_set['age'][available_mates]),]*choosers.size)
        choosers_age = array([(person_set['age'][choosers]),]*available_mates.size).transpose()
        available_mates_edu = array([(person_set['education'][available_mates]),]*choosers.size) #TODO: calc education in terms of years instead of level
        choosers_edu = array([(person_set['education'][choosers]),]*available_mates.size).transpose()
        age_diffs = available_mates_age - choosers_age
        edu_diffs = available_mates_edu - choosers_edu
        match_scores = exp((sqrt((age_diffs**2) + (edu_diffs**2)))*(-.5))
        row_sums = match_scores.sum(axis=1)
        probabilities = (match_scores) / (array([(row_sums),]*available_mates.size).transpose())
        #Select mates according to 'lottery choices' so that capacity can be taken into account (each person can only be chosen once)
        resources = Resources({"capacity":ones(available_mates.size),"lottery_max_iterations":50})
        choices = lottery_choices().run(probabilities, resources=resources)
        #Set each chosen person's household_id to equal the household_id of the chooser
        counter = 0
        for choice in choices:
            person_set['household_id'][available_mates[choice]] = person_set['household_id'][choosers[counter]]
            counter += 1
        logger.log_status("Mate matching complete.")
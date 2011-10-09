# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.agent_relocation_model import AgentRelocationModel
from opus_core.logger import logger
from numpy import array, zeros, ones, where, logical_and, arange, exp, sqrt, cumsum, searchsorted
from numpy.random import random, uniform

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
        person_set.add_attribute(name='unmatched', data=ones(person_set.size(), dtype='b'))
        if (index_eligible_males.size > 0) and (index_eligible_females.size > 0):
            #When males>females, females choose mate.  When females>=males, males choose mate.
            if index_eligible_males.size > index_eligible_females.size:
                gender_that_chooses = 'female'
                #Create the new household IDs and assign them to the mate choosers (the mate they choose will take on this same household ID)
                new_hh_id = arange(max_hh_id, max_hh_id+index_eligible_females.size)
                person_set.modify_attribute('household_id', new_hh_id, index=index_eligible_females)
                self.mate_match(index_eligible_females, index_eligible_males, person_set, gender_that_chooses)
            else:
                gender_that_chooses = 'male'
                new_hh_id = arange(max_hh_id, max_hh_id+index_eligible_males.size)
                person_set.modify_attribute('household_id', new_hh_id, index=index_eligible_males)
                self.mate_match(index_eligible_males, index_eligible_females, person_set, gender_that_chooses)
                        
        person_set.delete_one_attribute('marriage_eligible')
        person_set.delete_one_attribute('unmatched')        
        #Remove records from household_set that have no persons left
        persons = household_set.compute_variables("%s.number_of_agents(%s)" % (hh_ds_name, person_ds_name), resources=resources)
        index_hh0persons = where(persons==0)[0]
        if index_hh0persons.size > 0:
            logger.log_status("Removing %s records without %s from %s dataset" % (index_hh0persons.size, person_ds_name, hh_ds_name) )
            household_set.remove_elements(index_hh0persons)

    def mate_match(self, choosers, available_mates, person_set, gender_that_chooses):
        available_mates_age = person_set['age'][available_mates]
        available_mates_edu = person_set['education'][available_mates]#TODO: calc education in terms of years instead of level
        for chooser in choosers:
            chooser_age = person_set['age'][chooser]
            chooser_edu = person_set['education'][chooser]
            age_diffs = available_mates_age - chooser_age
            edu_diffs = available_mates_edu - chooser_edu
            match_score = exp((sqrt((age_diffs**2) + (edu_diffs**2)))*(-.5))
            cum_match_prob = cumsum(match_score / match_score.sum())
            r = uniform(0,1)
            the_lucky_person = searchsorted(cum_match_prob, r)

            if person_set['unmatched'][available_mates[the_lucky_person]] > 0:
                person_set['household_id'][available_mates[the_lucky_person]] = person_set['household_id'][chooser]
                person_set['unmatched'][available_mates[the_lucky_person]] = False
                person_set['unmatched'][chooser] = False

        #If there are unmatched males and unmatched females that remain (due to 'ties'), then match these unmatched persons with each other
        if (person_set['unmatched'][available_mates].sum() > 0) and (person_set['unmatched'][choosers].sum() > 0):
            #Recreate indexes for the eligible males and eligible females that remain
            if gender_that_chooses == 'female':
                if 'gender' in person_set.get_primary_attribute_names():
                    available_mates = where(logical_and(person_set['marriage_eligible'], ((person_set['gender']) * (person_set['unmatched'])) ==1))[0]
                    choosers = where(logical_and(person_set['marriage_eligible'], ((person_set['gender']) * (person_set['unmatched'])) ==2))[0]
                if 'sex' in person_set.get_primary_attribute_names():
                    available_mates = where(logical_and(person_set['marriage_eligible'], ((person_set['sex']) * (person_set['unmatched'])) ==1))[0]
                    choosers = where(logical_and(person_set['marriage_eligible'], ((person_set['sex']) * (person_set['unmatched'])) ==2))[0]
            if gender_that_chooses == 'male':
                if 'gender' in person_set.get_primary_attribute_names():
                    choosers = where(logical_and(person_set['marriage_eligible'], ((person_set['gender']) * (person_set['unmatched'])) ==1))[0]
                    available_mates = where(logical_and(person_set['marriage_eligible'], ((person_set['gender']) * (person_set['unmatched'])) ==2))[0]
                if 'sex' in person_set.get_primary_attribute_names():
                    choosers = where(logical_and(person_set['marriage_eligible'], ((person_set['sex']) * (person_set['unmatched'])) ==1))[0]
                    available_mates = where(logical_and(person_set['marriage_eligible'], ((person_set['sex']) * (person_set['unmatched'])) ==2))[0]

            self.mate_match(choosers, available_mates, person_set, gender_that_chooses)
        else:
            logger.log_status("Mate matching complete.")
# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.rate_based_model import RateBasedModel
from opus_core.logger import logger
from numpy import array, zeros, ones, where, logical_and, arange, exp, sqrt, cumsum, searchsorted
from numpy.random import random, uniform, shuffle

class MarriageModel(RateBasedModel):
    """
    """
    model_name = "Marriage Model"

    def run(self, person_set, household_set, resources=None):
        index = RateBasedModel.run(self, person_set, resources=resources)
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
        logger.log_status("%s new married couple households will be formed." % (index_eligible_females.size))

        max_hh_id = household_set.get_attribute(hh_id_name).max() + 1
        person_set.add_attribute(name='unmatched', data=ones(person_set.size(), dtype='b'))
        person_set.add_attribute(name='one_person_hh', data=person_set.compute_variables('person.disaggregate((household.number_of_agents(person)) == 1)'))
        person_set.add_attribute(name='single_parent', data=person_set.compute_variables('person.disaggregate(((household.aggregate(person.age > 17)) == 1)*((household.aggregate(person.age < 18)) > 0))'))
        #Create max # of new household IDs that may be needed (not all will be used because of re-use of existing household_ids)
        new_hh_id = arange(max_hh_id, max_hh_id+index_eligible_females.size)
        new_hh_id_counter = 0
        self.mate_match(index_eligible_females, index_eligible_males, person_set, household_set, new_hh_id, new_hh_id_counter, hh_id_name, max_hh_id)
                        
        person_set.delete_one_attribute('single_parent')
        person_set.delete_one_attribute('one_person_hh') 
        person_set.delete_one_attribute('marriage_eligible')
        person_set.delete_one_attribute('unmatched')        
        #Remove records from household_set that have no persons left
        persons = household_set.compute_variables("%s.number_of_agents(%s)" % (hh_ds_name, person_ds_name), resources=resources)
        index_hh0persons = where(persons==0)[0]
        if index_hh0persons.size > 0:
            logger.log_status("Removing %s records without %s from %s dataset" % (index_hh0persons.size, person_ds_name, hh_ds_name) )
            household_set.remove_elements(index_hh0persons)
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
        ##Initialize income of households with newly-assigned household_ids (should be only 2-person households) as -2
        if 'income' in household_set.get_primary_attribute_names():
            new_household_ids = household_set.compute_variables('(household.household_id > %s)' % (max_hh_id))
            initialize_income = where(new_household_ids == 1)[0]
            if initialize_income.size > 0:
                household_set.modify_attribute('income', array(initialize_income.size*[-2]), initialize_income)

    def mate_match(self, choosers, available_mates, person_set, household_set, new_hh_id, new_hh_id_counter, hh_id_name, max_hh_id):
        shuffle(choosers)
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
                person_set['unmatched'][available_mates[the_lucky_person]] = False
                person_set['unmatched'][chooser] = False
                #Designate the couple as married
                person_set['marriage_status'][available_mates[the_lucky_person]] = 1
                person_set['marriage_status'][chooser] = 1
                #if both persons are in a 1 person hh, assign the man the woman's household_id
                if ((person_set['one_person_hh'][available_mates[the_lucky_person]]) > 0) and ((person_set['one_person_hh'][chooser]) > 0):
                    person_set['household_id'][available_mates[the_lucky_person]] = person_set['household_id'][chooser]
                #if woman single_parent, but the man is not, assign the man the woman's household_id
                elif ((person_set['single_parent'][available_mates[the_lucky_person]]) == 0) and ((person_set['single_parent'][chooser]) > 0):
                    person_set['household_id'][available_mates[the_lucky_person]] = person_set['household_id'][chooser]
                #if man single_parent, but the woman is not, assign the woman the man's household_id
                elif ((person_set['single_parent'][available_mates[the_lucky_person]]) > 0) and ((person_set['single_parent'][chooser]) == 0):
                    person_set['household_id'][chooser] = person_set['household_id'][available_mates[the_lucky_person]]
                #if both are single_parents, assign all individuals in the man's household the woman's household_id.
                elif ((person_set['single_parent'][available_mates[the_lucky_person]]) > 0) and ((person_set['single_parent'][chooser]) > 0):
                    available_mate_hh_id = person_set['household_id'][available_mates[the_lucky_person]]
                    hh_id_to_change = where(person_set['household_id'] == available_mate_hh_id)
                    for hh_person in hh_id_to_change:
                        person_set['household_id'][hh_person] = person_set['household_id'][chooser]
                #if woman is in a 1 person hh, but man is not, assign the man the woman's household_id
                elif ((person_set['one_person_hh'][available_mates[the_lucky_person]]) == 0) and ((person_set['one_person_hh'][chooser]) > 0):
                    person_set['household_id'][available_mates[the_lucky_person]] = person_set['household_id'][chooser]
                #if man is in a 1 person hh, but woman is not, assign the woman the man's household_id
                elif ((person_set['one_person_hh'][available_mates[the_lucky_person]]) > 0) and ((person_set['one_person_hh'][chooser]) == 0):
                    person_set['household_id'][chooser] = person_set['household_id'][available_mates[the_lucky_person]] 
                #else if both have other adults living in their household:
                else:
                    person_set['household_id'][chooser] = new_hh_id[new_hh_id_counter]
                    person_set['household_id'][available_mates[the_lucky_person]] = new_hh_id[new_hh_id_counter]
                    new_hh_id_counter += 1

        #If there are unmatched males and unmatched females that remain, then match these unmatched persons with each other
        if (person_set['unmatched'][available_mates].sum() > 0) and (person_set['unmatched'][choosers].sum() > 0):
            #Recreate indexes for the eligible males and eligible females that remain
            if 'gender' in person_set.get_primary_attribute_names():
                available_mates = where(logical_and(person_set['marriage_eligible'], ((person_set['gender']) * (person_set['unmatched'])) ==1))[0]
                choosers = where(logical_and(person_set['marriage_eligible'], ((person_set['gender']) * (person_set['unmatched'])) ==2))[0]
            if 'sex' in person_set.get_primary_attribute_names():
                available_mates = where(logical_and(person_set['marriage_eligible'], ((person_set['sex']) * (person_set['unmatched'])) ==1))[0]
                choosers = where(logical_and(person_set['marriage_eligible'], ((person_set['sex']) * (person_set['unmatched'])) ==2))[0]

            self.mate_match(choosers, available_mates, person_set, household_set, new_hh_id, new_hh_id_counter, hh_id_name, max_hh_id)
        else:
            new_hh_id = arange(max_hh_id, max_hh_id+new_hh_id_counter+1)
            household_set.add_elements({hh_id_name:new_hh_id}, require_all_attributes=False)
            logger.log_status("Mate matching complete.")
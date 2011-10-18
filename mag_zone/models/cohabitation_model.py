# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.agent_relocation_model import AgentRelocationModel
from opus_core.logger import logger
from numpy import array, zeros, ones, where, logical_and, arange, exp, sqrt, cumsum, searchsorted
from numpy.random import random, uniform, shuffle

class CohabitationModel(AgentRelocationModel):
    """
    """
    model_name = "Cohabitation Model"

    def run(self, person_set, household_set, resources=None):
        index = AgentRelocationModel.run(self, person_set, resources=resources)
        logger.log_status("%s persons are in the cohabitation market." % (index.size) )

        person_ds_name, person_id_name = person_set.get_dataset_name(), person_set.get_id_name()[0]
        hh_ds_name, hh_id_name = household_set.get_dataset_name(), household_set.get_id_name()[0]

        #Flag the pool of individuals that are eligible to cohabitate
        person_set.add_attribute(name='cohabitation_eligible', data=zeros(person_set.size(), dtype='b'))
        person_set['cohabitation_eligible'][index] = True


        #Separate the males from the females
        if 'gender' in person_set.get_primary_attribute_names():
            index_eligible_males = where(logical_and(person_set['cohabitation_eligible'], person_set['gender']==1))[0]
            index_eligible_females = where(logical_and(person_set['cohabitation_eligible'], person_set['gender']==2))[0]
        if 'sex' in person_set.get_primary_attribute_names():
            index_eligible_males = where(logical_and(person_set['cohabitation_eligible'], person_set['sex']==1))[0]
            index_eligible_females = where(logical_and(person_set['cohabitation_eligible'], person_set['sex']==2))[0]
        logger.log_status("There are %s eligible males and %s eligible females." % (index_eligible_males.size,index_eligible_females.size) )
        logger.log_status("%s new cohabitating households will be formed." % (index_eligible_females.size))

        max_hh_id = household_set.get_attribute(hh_id_name).max() + 1
        person_set.add_attribute(name='unmatched', data=ones(person_set.size(), dtype='b'))
        person_set.add_attribute(name='one_person_hh', data=person_set.compute_variables('person.disaggregate((household.number_of_agents(person)) == 1)'))
        person_set.add_attribute(name='single_parent', data=person_set.compute_variables('person.disaggregate(((household.aggregate(person.age > 17)) == 1)*((household.aggregate(person.age < 18)) > 0))'))
        #Create max # of new household IDs that may be needed (not all will be used because of re-use of existing household_ids)
        new_hh_id = arange(max_hh_id, max_hh_id+index_eligible_females.size)
        new_hh_id_counter = 0
        self.mate_match(index_eligible_females, index_eligible_males, person_set, household_set, new_hh_id, new_hh_id_counter)
                        
        person_set.delete_one_attribute('single_parent')
        person_set.delete_one_attribute('one_person_hh') 
        person_set.delete_one_attribute('cohabitation_eligible')
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
        ##For MAG, each person's work_status is coded according to the ESR variable in the 2000 PUMS. 1: employed, at work. 2: employed with a job but not at work. 4: armed forces, at work.  5: armed forces, with a job but not at work
        ##Note that the WIF variable in the 2000 PUMS (which is the source for the household table's workers attribute), only applies to workers in families and the variable is top-coded so that families with 3+ workers get a value 3.
        if 'workers' in household_set.get_primary_attribute_names():
            workers = household_set.compute_variables('_workers = household.aggregate(person.work_status == 1) + household.aggregate(person.work_status == 2) +  household.aggregate(person.work_status == 4) + household.aggregate(person.work_status == 5)')
            household_set.modify_attribute('workers', workers)
        ##Assign "head of the household" status to the person with the lowest person_id (who will often, but not always, be the oldest).
        ##In the base-year data, the lowest person_id in each household is always the household head.
        ##Since the fertility model assigns person_id's in order of birth, people who are born later in the simulation will have higher person_ids.
        if 'head_of_hh' in person_set.get_primary_attribute_names():
            head_of_hh = person_set.compute_variables('_head_of_hh = (person.person_id == person.disaggregate(household.aggregate(person.person_id, function=minimum)))*1')
            person_set.modify_attribute('head_of_hh', head_of_hh)
        ##Update the age_of_head attribute in the household table to reflect the age of new heads of the household
        if 'age_of_head' in household_set.get_primary_attribute_names():
            age_of_head = household_set.compute_variables('_age_of_head = household.aggregate(person.head_of_hh * person.age)')
            household_set.modify_attribute('age_of_head', age_of_head)
        ##How to update the household table's building_id attribute?  Assign building IDs the same way we're assigning household id's? (moves in with female, in most circumstances)
        ##TODO:  person_no in new household needs to be dealt with.  Order by age?

    def mate_match(self, choosers, available_mates, person_set, household_set, new_hh_id, new_hh_id_counter):
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
                #Designate the couple as cohabitating.  Existing marriage_status variable takes values 1 through 6 and does not have a cohabitation category.  I designate cohabitators with marriage_status of 7.    
                person_set['marriage_status'][available_mates[the_lucky_person]] = 7
                person_set['marriage_status'][chooser] = 7
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
                available_mates = where(logical_and(person_set['cohabitation_eligible'], ((person_set['gender']) * (person_set['unmatched'])) ==1))[0]
                choosers = where(logical_and(person_set['cohabitation_eligible'], ((person_set['gender']) * (person_set['unmatched'])) ==2))[0]
            if 'sex' in person_set.get_primary_attribute_names():
                available_mates = where(logical_and(person_set['cohabitation_eligible'], ((person_set['sex']) * (person_set['unmatched'])) ==1))[0]
                choosers = where(logical_and(person_set['cohabitation_eligible'], ((person_set['sex']) * (person_set['unmatched'])) ==2))[0]

            self.mate_match(choosers, available_mates, person_set, household_set, new_hh_id, new_hh_id_counter)
        else:
            logger.log_status("Mate matching complete.")
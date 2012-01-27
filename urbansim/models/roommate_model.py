# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.rate_based_model import RateBasedModel
from opus_core.logger import logger
from numpy import where, arange, array, logical_and, zeros, ones, cumsum, searchsorted, exp, sqrt
from numpy.random import random, uniform, randint, shuffle

class RoommateModel(RateBasedModel):
    """
    """
    model_name = "Roommate Model"

    def run(self, person_set, household_set, resources=None):
        person_ds_name, person_id_name = person_set.get_dataset_name(), person_set.get_id_name()[0]
        hh_ds_name, hh_id_name = household_set.get_dataset_name(), household_set.get_id_name()[0]
        #identify nonfamily households
        household_set.compute_variables('contains_children = (household.aggregate(person.age < 18) > 0)')
        household_set.compute_variables('contains_married = (household.aggregate(person.marriage_status == 1) > 0)')
        nonfamily_hh = household_set.compute_variables("_nonfamily_hh = numpy.logical_and(household.contains_children == 0, " + 
                                                                                                       "household.contains_married == 0)")
        idx_nonfamily = where(nonfamily_hh)[0]
        one_person_nonfam_hh = where(logical_and(nonfamily_hh==1, household_set.compute_variables('household.number_of_agents(person) == 1')))[0]
        proportion_nonfamhh_1person = ((one_person_nonfam_hh.size)*1.0)/((idx_nonfamily.size)*1.0)
        #Proceed with room-mate household creation if the proportion of nonfamily households that are single-person households exceeds .66, which is the base-year proportion
        if proportion_nonfamhh_1person < .66 :
            logger.log_status("No need for room-mate model")
        else:
            logger.log_status("ahhhh!  need to group 1-person hh's into room-mates!!")
            proportion_to_group = (proportion_nonfamhh_1person - .66)/(proportion_nonfamhh_1person)
            logger.log_status("%s is the proportion of 1-person hh's to group"% (proportion_to_group))
            persons_in_nonfamhh1 = where(logical_and(person_set.compute_variables('person.disaggregate(household._nonfamily_hh)'),person_set.compute_variables('person.disaggregate(household.number_of_agents(person) == 1)')))[0]
            logger.log_status("%s persons in nonfam 1-person hh's"% ( persons_in_nonfamhh1.size))
            person_set.add_attribute(name='persons_to_group', data=zeros(person_set.size(), dtype='int32'))
            prob_to_group = ([(1-proportion_to_group),proportion_to_group])
            cumprob_to_group = cumsum(prob_to_group)
            for person in persons_in_nonfamhh1:
                r = uniform(0,1)
                person_set['persons_to_group'][person] = searchsorted(cumprob_to_group, r)
            logger.log_status("%s persons to group"% (person_set['persons_to_group'].sum()))
            idx_moving_out_age_18_20 = where(person_set.compute_variables('(person.persons_to_group)*((person.age>17)*(person.age<21))'))[0]
            idx_moving_out_age_21_25 = where(person_set.compute_variables('(person.persons_to_group)*((person.age>20)*(person.age<26))'))[0]
            idx_moving_out_age_26_30 = where(person_set.compute_variables('(person.persons_to_group)*((person.age>25)*(person.age<31))'))[0]
            idx_moving_out_age_31_35 = where(person_set.compute_variables('(person.persons_to_group)*((person.age>30)*(person.age<36))'))[0]
            idx_moving_out_age_36_up = where(person_set.compute_variables('(person.persons_to_group)*(person.age>35)'))[0]
            if idx_moving_out_age_18_20.size > 0:
                hhsize_prob = ([.52,.33,.12,.03])
                hhsize_cum_prob = cumsum(hhsize_prob)
                for person in idx_moving_out_age_18_20:
                    r = uniform(0,1)
                    person_set['persons_to_group'][person] = searchsorted(hhsize_cum_prob, r)+2
            if idx_moving_out_age_21_25.size > 0:
                hhsize_prob = ([.59,.28,.12,.01])
                hhsize_cum_prob = cumsum(hhsize_prob)
                for person in idx_moving_out_age_21_25:
                    r = uniform(0,1)
                    person_set['persons_to_group'][person] = searchsorted(hhsize_cum_prob, r)+2
            if idx_moving_out_age_26_30.size > 0:
                hhsize_prob = ([.69,.23,.06,.02])
                hhsize_cum_prob = cumsum(hhsize_prob)
                for person in idx_moving_out_age_26_30:
                    r = uniform(0,1)
                    person_set['persons_to_group'][person] = searchsorted(hhsize_cum_prob, r)+2
            if idx_moving_out_age_31_35.size > 0:
                hhsize_prob = ([.79,.18,.02,.01])
                hhsize_cum_prob = cumsum(hhsize_prob)
                for person in idx_moving_out_age_31_35:
                    r = uniform(0,1)
                    person_set['persons_to_group'][person] = searchsorted(hhsize_cum_prob, r)+2
            if idx_moving_out_age_36_up.size > 0:
                hhsize_prob = ([.80,.15,.05])
                hhsize_cum_prob = cumsum(hhsize_prob)
                for person in idx_moving_out_age_36_up:
                    r = uniform(0,1)
                    person_set['persons_to_group'][person] = searchsorted(hhsize_cum_prob, r)+2
            if 'sex' in person_set.get_primary_attribute_names():     
                person_set.add_attribute(name='hhsize2males', data=person_set.compute_variables('(person.persons_to_group==2)*(person.sex==1)')) 
                hhsize2male = person_set.compute_variables('(person.persons_to_group==2)*(person.sex==1)')
                person_set.add_attribute(name='hhsize3males', data=person_set.compute_variables('(person.persons_to_group==3)*(person.sex==1)'))
                hhsize3male = person_set.compute_variables('(person.persons_to_group==3)*(person.sex==1)')
                person_set.add_attribute(name='hhsize4males', data=person_set.compute_variables('(person.persons_to_group==4)*(person.sex==1)'))
                hhsize4male = person_set.compute_variables('(person.persons_to_group==4)*(person.sex==1)')
                person_set.add_attribute(name='hhsize5males', data=person_set.compute_variables('(person.persons_to_group==5)*(person.sex==1)'))
                hhsize5male = person_set.compute_variables('(person.persons_to_group==5)*(person.sex==1)')
                person_set.add_attribute(name='hhsize2females', data=person_set.compute_variables('(person.persons_to_group==2)*(person.sex==2)'))
                hhsize2female = person_set.compute_variables('(person.persons_to_group==2)*(person.sex==2)')
                person_set.add_attribute(name='hhsize3females', data=person_set.compute_variables('(person.persons_to_group==3)*(person.sex==2)'))
                hhsize3female = person_set.compute_variables('(person.persons_to_group==3)*(person.sex==2)')
                person_set.add_attribute(name='hhsize4females', data=person_set.compute_variables('(person.persons_to_group==4)*(person.sex==2)'))
                hhsize4female = person_set.compute_variables('(person.persons_to_group==4)*(person.sex==2)')
                person_set.add_attribute(name='hhsize5females', data=person_set.compute_variables('(person.persons_to_group==5)*(person.sex==2)'))
                hhsize5female = person_set.compute_variables('(person.persons_to_group==5)*(person.sex==2)')
            if 'gender' in person_set.get_primary_attribute_names():
                person_set.add_attribute(name='hhsize2males', data=person_set.compute_variables('(person.persons_to_group==2)*(person.gender==1)')) 
                hhsize2male = person_set.compute_variables('(person.persons_to_group==2)*(person.gender==1)')
                person_set.add_attribute(name='hhsize3males', data=person_set.compute_variables('(person.persons_to_group==3)*(person.gender==1)'))
                hhsize3male = person_set.compute_variables('(person.persons_to_group==3)*(person.gender==1)')
                person_set.add_attribute(name='hhsize4males', data=person_set.compute_variables('(person.persons_to_group==4)*(person.gender==1)'))
                hhsize4male = person_set.compute_variables('(person.persons_to_group==4)*(person.gender==1)')
                person_set.add_attribute(name='hhsize5males', data=person_set.compute_variables('(person.persons_to_group==5)*(person.gender==1)'))
                hhsize5male = person_set.compute_variables('(person.persons_to_group==5)*(person.gender==1)')
                person_set.add_attribute(name='hhsize2females', data=person_set.compute_variables('(person.persons_to_group==2)*(person.gender==2)'))
                hhsize2female = person_set.compute_variables('(person.persons_to_group==2)*(person.gender==2)')
                person_set.add_attribute(name='hhsize3females', data=person_set.compute_variables('(person.persons_to_group==3)*(person.gender==2)'))
                hhsize3female = person_set.compute_variables('(person.persons_to_group==3)*(person.gender==2)')
                person_set.add_attribute(name='hhsize4females', data=person_set.compute_variables('(person.persons_to_group==4)*(person.gender==2)'))
                hhsize4female = person_set.compute_variables('(person.persons_to_group==4)*(person.gender==2)')
                person_set.add_attribute(name='hhsize5females', data=person_set.compute_variables('(person.persons_to_group==5)*(person.gender==2)'))
                hhsize5female = person_set.compute_variables('(person.persons_to_group==5)*(person.gender==2)')
            max_hh_id1 = household_set.get_attribute(hh_id_name).max() + 1
            person_set.add_attribute(name='chooser', data=randint(1, 3, person_set.size()))
            person_set.add_attribute(name='unmatched', data=ones(person_set.size(), dtype='b'))
            #male 2-person hh
            index_choosers = where(logical_and(person_set['chooser']==1, hhsize2male==1))[0]
            index_roommates = where(logical_and(person_set['chooser']==2, hhsize2male==1))[0]
            max_hh_id = household_set.get_attribute(hh_id_name).max() + 1
            new_hh_id = arange(max_hh_id, max_hh_id+index_choosers.size)
            person_set.modify_attribute(hh_id_name, new_hh_id, index=index_choosers)
            household_set.add_elements({hh_id_name:new_hh_id}, require_all_attributes=False)
            self.mate_match(index_choosers, index_roommates, person_set, household_set, 'hhsize2males')
            person_set.delete_one_attribute('hhsize2males') 
            #female 2-person hh
            index_choosers = where(logical_and(person_set['chooser']==1, hhsize2female==1))[0]
            index_roommates = where(logical_and(person_set['chooser']==2, hhsize2female==1))[0]
            max_hh_id = household_set.get_attribute(hh_id_name).max() + 1
            new_hh_id = arange(max_hh_id, max_hh_id+index_choosers.size)
            person_set.modify_attribute(hh_id_name, new_hh_id, index=index_choosers)
            household_set.add_elements({hh_id_name:new_hh_id}, require_all_attributes=False)
            self.mate_match(index_choosers, index_roommates, person_set, household_set, 'hhsize2females')
            person_set.delete_one_attribute('hhsize2females')
            #male 3-person hh
            person_set.delete_one_attribute('chooser')
            person_set.add_attribute(name='chooser', data=randint(1, 4, person_set.size()))
            index_choosers = where(logical_and(person_set['chooser']==1, hhsize3male==1))[0]
            index_roommates = where(logical_and(person_set['chooser'] > 1, hhsize3male==1))[0]
            max_hh_id = household_set.get_attribute(hh_id_name).max() + 1
            new_hh_id = arange(max_hh_id, max_hh_id+index_choosers.size)
            person_set.modify_attribute(hh_id_name, new_hh_id, index=index_choosers)
            household_set.add_elements({hh_id_name:new_hh_id}, require_all_attributes=False)
            person_set.add_attribute(name='roommate_counter', data=zeros(person_set.size(), dtype='int32'))
            person_set['roommate_counter'][index_choosers] = 1
            self.mate_match_multi(index_choosers, index_roommates, person_set, household_set, 'hhsize3males', 3)
            person_set.delete_one_attribute('roommate_counter')
            person_set.delete_one_attribute('hhsize3males')
            #female 3-person hh
            index_choosers = where(logical_and(person_set['chooser']==1, hhsize3female==1))[0]
            index_roommates = where(logical_and(person_set['chooser'] > 1, hhsize3female==1))[0]
            max_hh_id = household_set.get_attribute(hh_id_name).max() + 1
            new_hh_id = arange(max_hh_id, max_hh_id+index_choosers.size)
            person_set.modify_attribute(hh_id_name, new_hh_id, index=index_choosers)
            household_set.add_elements({hh_id_name:new_hh_id}, require_all_attributes=False)
            person_set.add_attribute(name='roommate_counter', data=zeros(person_set.size(), dtype='int32'))
            person_set['roommate_counter'][index_choosers] = 1
            self.mate_match_multi(index_choosers, index_roommates, person_set, household_set, 'hhsize3females', 3)
            person_set.delete_one_attribute('roommate_counter')
            person_set.delete_one_attribute('hhsize3females')
            #male 4-person hh
            person_set.delete_one_attribute('chooser')
            person_set.add_attribute(name='chooser', data=randint(1, 5, person_set.size()))
            index_choosers = where(logical_and(person_set['chooser']==1, hhsize4male==1))[0]
            index_roommates = where(logical_and(person_set['chooser'] > 1, hhsize4male==1))[0]
            max_hh_id = household_set.get_attribute(hh_id_name).max() + 1
            new_hh_id = arange(max_hh_id, max_hh_id+index_choosers.size)
            person_set.modify_attribute(hh_id_name, new_hh_id, index=index_choosers)
            household_set.add_elements({hh_id_name:new_hh_id}, require_all_attributes=False)
            person_set.add_attribute(name='roommate_counter', data=zeros(person_set.size(), dtype='int32'))
            person_set['roommate_counter'][index_choosers] = 1
            self.mate_match_multi(index_choosers, index_roommates, person_set, household_set, 'hhsize4males', 4)
            person_set.delete_one_attribute('roommate_counter')
            person_set.delete_one_attribute('hhsize4males')
            #female 4-person hh
            index_choosers = where(logical_and(person_set['chooser']==1, hhsize4female==1))[0]
            index_roommates = where(logical_and(person_set['chooser'] > 1, hhsize4female==1))[0]
            max_hh_id = household_set.get_attribute(hh_id_name).max() + 1
            new_hh_id = arange(max_hh_id, max_hh_id+index_choosers.size)
            person_set.modify_attribute(hh_id_name, new_hh_id, index=index_choosers)
            household_set.add_elements({hh_id_name:new_hh_id}, require_all_attributes=False)
            person_set.add_attribute(name='roommate_counter', data=zeros(person_set.size(), dtype='int32'))
            person_set['roommate_counter'][index_choosers] = 1
            self.mate_match_multi(index_choosers, index_roommates, person_set, household_set, 'hhsize4females', 4)
            person_set.delete_one_attribute('roommate_counter')
            person_set.delete_one_attribute('hhsize4females')
            #male 5-person hh
            person_set.delete_one_attribute('chooser')
            person_set.add_attribute(name='chooser', data=randint(1, 6, person_set.size()))
            index_choosers = where(logical_and(person_set['chooser']==1, hhsize5male==1))[0]
            index_roommates = where(logical_and(person_set['chooser'] > 1, hhsize5male==1))[0]
            max_hh_id = household_set.get_attribute(hh_id_name).max() + 1
            new_hh_id = arange(max_hh_id, max_hh_id+index_choosers.size)
            person_set.modify_attribute(hh_id_name, new_hh_id, index=index_choosers)
            household_set.add_elements({hh_id_name:new_hh_id}, require_all_attributes=False)
            person_set.add_attribute(name='roommate_counter', data=zeros(person_set.size(), dtype='int32'))
            person_set['roommate_counter'][index_choosers] = 1
            self.mate_match_multi(index_choosers, index_roommates, person_set, household_set, 'hhsize5males', 5)
            person_set.delete_one_attribute('roommate_counter')
            person_set.delete_one_attribute('hhsize5males')
            #female 5-person hh
            index_choosers = where(logical_and(person_set['chooser']==1, hhsize5female==1))[0]
            index_roommates = where(logical_and(person_set['chooser'] > 1, hhsize5female==1))[0]
            max_hh_id = household_set.get_attribute(hh_id_name).max() + 1
            new_hh_id = arange(max_hh_id, max_hh_id+index_choosers.size)
            person_set.modify_attribute(hh_id_name, new_hh_id, index=index_choosers)
            household_set.add_elements({hh_id_name:new_hh_id}, require_all_attributes=False)
            person_set.add_attribute(name='roommate_counter', data=zeros(person_set.size(), dtype='int32'))
            person_set['roommate_counter'][index_choosers] = 1
            self.mate_match_multi(index_choosers, index_roommates, person_set, household_set, 'hhsize5females', 5)
            person_set.delete_one_attribute('roommate_counter')
            person_set.delete_one_attribute('hhsize5females')

            ##Remove records from household_set that have no persons left
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
                new_household_ids = household_set.compute_variables('(household.household_id > %s)' % (max_hh_id1))
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
            ##Initialize income of households with newly-assigned household_ids (should be only 1-person households) as -1
            if 'income' in household_set.get_primary_attribute_names():
                new_hhsize1_ids = household_set.compute_variables('(household.household_id > %s)*(household.persons==1)' % (max_hh_id1))
                initialize_income_hhsize1 = where(new_hhsize1_ids == 1)[0]
                if initialize_income_hhsize1.size > 0:
                    household_set.modify_attribute('income', array(initialize_income_hhsize1.size*[-1]), initialize_income_hhsize1)
                new_hhsize2_ids = household_set.compute_variables('(household.household_id > %s)*(household.persons==2)' % (max_hh_id1))
                initialize_income_hhsize2 = where(new_hhsize2_ids == 1)[0]
                if initialize_income_hhsize2.size > 0:
                    household_set.modify_attribute('income', array(initialize_income_hhsize2.size*[-2]), initialize_income_hhsize2)
                new_hhsize3_ids = household_set.compute_variables('(household.household_id > %s)*(household.persons==3)' % (max_hh_id1))
                initialize_income_hhsize3 = where(new_hhsize3_ids == 1)[0]
                if initialize_income_hhsize3.size > 0:
                    household_set.modify_attribute('income', array(initialize_income_hhsize3.size*[-3]), initialize_income_hhsize3)
                new_hhsize4_ids = household_set.compute_variables('(household.household_id > %s)*(household.persons==4)' % (max_hh_id1))
                initialize_income_hhsize4 = where(new_hhsize4_ids == 1)[0]
                if initialize_income_hhsize4.size > 0:
                    household_set.modify_attribute('income', array(initialize_income_hhsize4.size*[-4]), initialize_income_hhsize4)
                new_hhsize5_ids = household_set.compute_variables('(household.household_id > %s)*(household.persons==5)' % (max_hh_id1))
                initialize_income_hhsize5 = where(new_hhsize5_ids == 1)[0]
                if initialize_income_hhsize5.size > 0:
                    household_set.modify_attribute('income', array(initialize_income_hhsize5.size*[-5]), initialize_income_hhsize5)

            person_set.delete_one_attribute('much_younger_than_head')
            person_set.delete_one_attribute('same_race_as_head') 
            person_set.delete_one_attribute('chooser') 
            person_set.delete_one_attribute('unmatched')
            person_set.delete_one_attribute('persons_to_group')

    def mate_match(self, choosers, available_mates, person_set, household_set, hhsize_gender):
        shuffle(choosers)
        available_mates_age = person_set['age'][available_mates]
        available_mates_edu = person_set['education'][available_mates]
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
                person_set['household_id'][available_mates[the_lucky_person]] = person_set['household_id'][chooser]
        #If there are unmatched persons that remain, then match these unmatched persons with each other
        if (person_set['unmatched'][available_mates].sum() > 0) and (person_set['unmatched'][choosers].sum() > 0):
            #Recreate indexes for the eligible choosers and eligible roommates that remain
            index_choosers = where(logical_and(person_set['chooser']==1, ((person_set[hhsize_gender]) * (person_set['unmatched'])) ==1))[0]
            index_roommates = where(logical_and(person_set['chooser']==2, ((person_set[hhsize_gender]) * (person_set['unmatched'])) ==1))[0]
            self.mate_match(index_choosers, index_roommates, person_set, household_set, hhsize_gender)
        else:
            logger.log_status("Room-mate matching complete.")

    def mate_match_multi(self, choosers, available_mates, person_set, household_set, hhsize_gender, max_hh_size):
        #shuffle(choosers)
        available_mates_age = person_set['age'][available_mates]
        available_mates_edu = person_set['education'][available_mates]
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
                person_set['roommate_counter'][chooser] += 1
                if person_set['roommate_counter'][chooser] == max_hh_size:
                    person_set['unmatched'][chooser] = False
                person_set['household_id'][available_mates[the_lucky_person]] = person_set['household_id'][chooser]
        #If there are unmatched persons that remain, then match these unmatched persons with each other
        if (person_set['unmatched'][available_mates].sum() > 0) and (person_set['unmatched'][choosers].sum() > 0):
            #Recreate indexes for the eligible choosers and eligible roommates that remain
            index_choosers = where(logical_and(person_set['chooser']==1, ((person_set[hhsize_gender]) * (person_set['unmatched'])) ==1))[0]
            index_roommates = where(logical_and(person_set['chooser']>1, ((person_set[hhsize_gender]) * (person_set['unmatched'])) ==1))[0]
            self.mate_match_multi(index_choosers, index_roommates, person_set, household_set, hhsize_gender, max_hh_size)
        else:
            logger.log_status("Room-mate matching complete.")
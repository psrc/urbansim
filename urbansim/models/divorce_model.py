# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.rate_based_model import RateBasedModel
from opus_core.logger import logger
from numpy import array, zeros, ones, where, logical_and, arange, exp, sqrt, cumsum, searchsorted
from numpy.random import random, uniform, shuffle

class DivorceModel(RateBasedModel):
    """
    """
    model_name = "Divorce Model"

    def run(self, person_set, household_set, resources=None):
        index = RateBasedModel.run(self, person_set, resources=resources)

        person_ds_name, person_id_name = person_set.get_dataset_name(), person_set.get_id_name()[0]
        hh_ds_name, hh_id_name = household_set.get_dataset_name(), household_set.get_id_name()[0]

        #Identify married women that will seek a divorce
        person_set.add_attribute(name='divorce_seeking', data=zeros(person_set.size(), dtype='b'))
        person_set['divorce_seeking'][index] = True
        if 'gender' in person_set.get_primary_attribute_names():
            index_divorcing_females = where(logical_and(person_set['divorce_seeking'], person_set['gender']==2))[0]
        if 'sex' in person_set.get_primary_attribute_names():
            index_divorcing_females = where(logical_and(person_set['divorce_seeking'], person_set['sex']==2))[0]
        logger.log_status("%s women will seek a divorce." % (index_divorcing_females.size) )

        #Identify men that will be divorced in the simplest case where there is only 1 married man in the household
        #Assign new household id's to these men.  The woman keeps the house and retains custody of any children.
        if 'gender' in person_set.get_primary_attribute_names():
            married_man = person_set.compute_variables("_married_man = (person.marriage_status == 1)*(person.gender == 1)")
            num_married_men_in_hh = person_set.compute_variables("_num_married_men = person.disaggregate(household.aggregate(person._married_man))")
            only_married_man_in_hh = person_set.compute_variables("_only_married_man = (person._num_married_men == 1) * (person.gender == 1) * (person.marriage_status == 1)")
            woman_getting_divorce = person_set.compute_variables("_woman_getting_divorce = (person.divorce_seeking)*(person.gender==2)*(person.marriage_status == 1)")
        if 'sex' in person_set.get_primary_attribute_names():
            married_man = person_set.compute_variables("_married_man = (person.marriage_status == 1)*(person.sex == 1)")
            num_married_men_in_hh = person_set.compute_variables("_num_married_men = person.disaggregate(household.aggregate(person._married_man))")
            only_married_man_in_hh = person_set.compute_variables("_only_married_man = (person._num_married_men == 1) * (person.sex == 1) * (person.marriage_status == 1)")
            woman_getting_divorce = person_set.compute_variables("_woman_getting_divorce = (person.divorce_seeking)*(person.sex==2)*(person.marriage_status == 1)")
        num_divorces_in_hh = person_set.compute_variables("_num_divorces = person.disaggregate(household.aggregate(person._woman_getting_divorce))")
        man1_to_divorce = person_set.compute_variables("(person._only_married_man) * (person._num_divorces > 0)")
        index_man1_divorce = where(man1_to_divorce == 1)[0]
        max_hh_id = household_set.get_attribute(hh_id_name).max() + 1
        new_hh_id = arange(max_hh_id, max_hh_id+index_man1_divorce.size)
        person_set.modify_attribute('household_id', new_hh_id, index=index_man1_divorce)
        household_set.add_elements({hh_id_name:new_hh_id}, require_all_attributes=False)
        person_set.modify_attribute('marriage_status', array(index_man1_divorce.size*[4]), index_man1_divorce)

        #Identify men that will be divorced when there is more than 1 married man in the household
        must_pick_man_to_divorce = where(logical_and(woman_getting_divorce > 0, num_married_men_in_hh > 1))[0]
        person_set.add_attribute(name='not_divorced', data=ones(person_set.size(), dtype='b'))
        max_hh_id2 = household_set.get_attribute(hh_id_name).max() + 1
        new_hh_id = arange(max_hh_id2, max_hh_id2+must_pick_man_to_divorce.size)
        household_set.add_elements({hh_id_name:new_hh_id}, require_all_attributes=False)
        new_hh_id_counter = 0
        self.pick_man_to_divorce(must_pick_man_to_divorce, married_man, num_married_men_in_hh, person_set, new_hh_id, new_hh_id_counter)

        #Set the marriage_status of all divorcing females to divorced.  Note that # divorcing females will exceed the number of divorced males in this model, because not all divorcing females lived in the same household as husband (female has marriage_status=2 or there can simply be no male in the household with marriage_status=1)
        person_set.modify_attribute('marriage_status', array(index_divorcing_females.size*[4]), index_divorcing_females)
        logger.log_status("Divorces completed")

        person_set.delete_one_attribute('divorce_seeking')
        person_set.delete_one_attribute('not_divorced') 
        #Remove records from household_set that have no persons left
        persons = household_set.compute_variables("%s.number_of_agents(%s)" % (hh_ds_name, person_ds_name), resources=resources)
        index_hh0persons = where(persons==0)[0]
        if index_hh0persons.size > 0:
            logger.log_status("Removing %s records without %s from %s dataset" % (index_hh0persons.size, person_ds_name, hh_ds_name) )
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

    def pick_man_to_divorce(self, must_pick_man_to_divorce, married_man, num_married_men_in_hh, person_set, new_hh_id, new_hh_id_counter):
        for woman in must_pick_man_to_divorce:
            woman_hh_id = person_set['household_id'][woman]
            married_men_in_hh = where(logical_and(person_set['household_id'] == woman_hh_id, married_man == 1))[0]
            married_men_age = person_set['age'][married_men_in_hh]
            married_men_edu = person_set['education'][married_men_in_hh]  #calc education in terms of years instead of level?
            woman_age = person_set['age'][woman]
            woman_edu = person_set['education'][woman]
            age_diffs = married_men_age - woman_age
            edu_diffs = married_men_edu - woman_edu
            match_score = exp((sqrt((age_diffs**2) + (edu_diffs**2)))*(-.5))
            cum_match_prob = cumsum(match_score / match_score.sum())
            r = uniform(0,1)
            man_to_divorce = searchsorted(cum_match_prob, r)
            if person_set['not_divorced'][married_men_in_hh[man_to_divorce]] > 0:
                person_set['not_divorced'][married_men_in_hh[man_to_divorce]] = False
                person_set['not_divorced'][woman] = False
                person_set['marriage_status'][married_men_in_hh[man_to_divorce]] = 4
                person_set['household_id'][married_men_in_hh[man_to_divorce]] = new_hh_id[new_hh_id_counter]
                new_hh_id_counter += 1


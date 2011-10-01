# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.agent_relocation_model import AgentRelocationModel
from opus_core.logger import logger
from numpy import where, array
from numpy.random import random

class MortalityModel(AgentRelocationModel):
    """
    """
    model_name = "Mortality Model"

    def run(self, person_set, household_set, resources=None):
        person_ds_name = person_set.get_dataset_name()
        hh_ds_name = household_set.get_dataset_name()
        index = AgentRelocationModel.run(self, person_set, resources=resources)

        #avoid orphaning children before we handle them in an adoption model
        person_set.add_attribute('mortality_flag', data=zeros(person_set.size(), dtype='b'))
        person_set['mortality_flag'][index] = True

        #identify such households
        adult_mortality = household_set.compute_variables("full_adult_mortality=household.aggregate(person.mortality_flag) == household.aggregate(person.age>17)")
        children_remain = household_set.compute_variables("children_remain=household.aggregate(numpy.logical_not(person.mortality_flag) * person.age <= 17) > 0 ")
        hh_at_risk = household_set.compute_variables("at_risk = household.full_adult_mortality * household.children_remain")
        if any(household["orphan_at_risk"]):
            #sample 1 adult per household to keep for households with children at risk 
            p_at_risk = where( household.compute_variables("person.disaggregate(household.at_risk)") )[0]
            adult_mortality = person_set.compute_variables("adult_mortality = (person.mortality_flag * (person.age>17)).astype('f')")
            prob_to_keep = person.compute_variables("safe_array_divide(person.adult_mortality, person.disaggregate(household.aggregate(person.adult_mortality)))")

            for idx_hh in where(hh_at_risk)[0]:
                hh_id = household['household_id'][idx_hh]
                ps_of_this_hh = where( person['household_id'] == hh_id )[0]
                r = random(0, 1); cumprob = cumsum(prob_to_keep[p_of_this_hh])
                idx_adlult_to_keep = searchsorted(cumprob, r)
                person_set['mortality_flag'][p_of_this_hh[idx_adult_to_keep]] = False

        idx = where( person_set['mortality_flag'] )[0]
        person_set.delete_attribute('mortality_flag')

        logger.log_status("Removing %s records from %s dataset" % (idx.size, person_set.get_dataset_name()) )
        person_set.remove_elements(idx)
        
        ##remove records from household_set that have no persons left
        persons = household_set.compute_variables("%s.number_of_agents(%s)" % (hh_ds_name, person_ds_name), resources=resources)
        index_hh0persons = where(persons==0)[0]
        if index_hh0persons.size > 0:
            logger.log_status("Removing %s records without %s from %s dataset" % (index_hh0persons.size, person_ds_name, hh_ds_name) )
            household_set.remove_elements(index_hh0persons)

        ## it would work better to convert them to computed variables
        ##Update the household table's persons attribute to account for deaths
        if 'persons' in household_set.get_primary_attribute_names():
            persons = household_set.compute_variables('_persons = household.number_of_agents(person)')
            household_set.modify_attribute('persons', persons)
        ##Update the household table's children attribute to account for child deaths
        if 'children' in household_set.get_primary_attribute_names():
            children = household_set.compute_variables('_children = household.aggregate(person.age<18)')
            household_set.modify_attribute('children', children)

        ##Update the household table's workers attribute to account for worker deaths
        ##For MAG, each person's work_status is coded according to the ESR variable in the 2000 PUMS. 1: employed, at work. 2: employed with a job but not at work. 4: armed forces, at work.  5: armed forces, with a job but not at work
        ##Note that the WIF variable in the 2000 PUMS (which is the source for the household table's workers attribute), only applies to workers in families and the variable is top-coded so that families with 3+ workers get a value 3.
        if 'workers' in household_set.get_primary_attribute_names():
            workers = household_set.compute_variables('_workers = household.aggregate(person.work_status == 1) + household.aggregate(person.work_status == 2) +  household.aggregate(person.work_status == 4) + household.aggregate(person.work_status == 5)')
            household_set.modify_attribute('workers', workers)
        ##If the head of the household dies, assign "head of the household" status to the person with the next lowest person_id (who will often, but not always, be the next oldest).
        ##In the base-year data, the lowest person_id in each household is always the household head.
        ##Since the fertility model assigns person_id's in order of birth, people who are born later in the simulation will have higher person_ids.
        if 'head_of_hh' in person_set.get_primary_attribute_names():
            head_of_hh = person_set.compute_variables('_head_of_hh = (person.person_id == person.disaggregate(household.aggregate(person.person_id, function=minimum)))*1')
            person_set.modify_attribute('head_of_hh', head_of_hh)
        ##Update the age_of_head attribute in the household table to reflect the age of new heads of the household and to reflect the aging of existing heads of household.
        if 'age_of_head' in household_set.get_primary_attribute_names():
            age_of_head = household_set.compute_variables('_age_of_head = household.aggregate(person.head_of_hh * person.age)')
            household_set.modify_attribute('age_of_head', age_of_head)
        ##When a person's spouse dies, change the person's marriage_status from married to widowed. (This has implications for the household formation model)
        ##Note that a marriage_status=1 is supposed to indicate being married to a spouse who resides in the same household.  In the case of marriage_status=2, which indicates married to a spouse who does not live in the household, we cannot tell when someone's spouse dies.  Widowed (marriage_status = 3) includes men.
        if 'marriage_status' in person_set.get_primary_attribute_names():
            widowed = person_set.compute_variables('_last_spouse = (((person.disaggregate(household.aggregate(person.marriage_status == 1)))==1)*1) * ((person.marriage_status == 1)*1)')
            index_widow = where(widowed==1)[0]
            if index_widow.size > 0:
                person_set.modify_attribute('marriage_status', array(index_widow.size*[3]), index_widow)


from opus_core.tests import opus_unittest
from opus_core.misc import ismember
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.resources import Resources
from numpy import array, logical_and, int32, int8, ma, all, allclose
from scipy import histogram
from opus_core.datasets.dataset import Dataset
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.datasets.person_dataset import PersonDataset
from opus_core.storage_factory import StorageFactory
from itertools.chain import from_iterable

class Tests(opus_unittest.OpusTestCase):

    def setUp(self):
        households_data = {
            "household_id":arange(33)+1,
            "age_of_head" array(),
            "persons": array(6*[2] + 2*[3] + 3*[1] + 4*[6] + 2*[1] + 5*[4] +
                                3*[1]+ 8*[5], dtype=int8),
            }
        
        total_persons = households_data['persons'].sum()
        persons_data = {
            "person_id":arange(total_persons)+1,
            "household_id": array( list(from_iterable([[i] * p for i,p in zip(households_data['household_id'], households_data['persons'])])) ),
            "member_id": array( list(from_iterable([range(1,p+1) for p in households_data['persons']])) ),
            "age": array( list(from_iterable([a]+list(randint(0, a, size=p-1)) for a,p in zip(households_data['age_of_head'], households_data['persons'])])) ),
            "job_id": zeros(total_persons)
            }

        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='hh_set', table_data=households_data)
        self.hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')
        storage.write_table(table_name='person_set', table_data=persons_data)
        self.persons_set = PersonDataset(in_storage=storage, in_table_name='person_set')

    def test_mortality_model_avoids_orhpans(elf):

        mortality_rates = {
            "year": array([2000, 2000, 2001, 2001]),
            "age_min": array([ 50,  0,  50,  0]),
            "age_max": array([100, 49, 100, 49]),
            "mortality_rate": arange(0.5, 0.5, .8, .8),
            }

        dataset_pool = DatasetPool(package_order=['urbansim', 'opus_core'],
                           datasets_dict={'household':self.hh_set,
                                          'person':self.person_set
                                         })
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='mortality_rate', table_data=mortality_rates)
        model = MortalityModel()
        model.prepare_for_run(rate_dataset_name='mortality_rate', rate_storage=storage)
        model.run(self.person_set, 
                  self.hh_set,
                  resources=dataset_pool
                  )
        
